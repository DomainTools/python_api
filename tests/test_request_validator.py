import pytest
from unittest.mock import patch, MagicMock

# Assuming your class is in api_core.py
from domaintools.request_validator import RequestValidator


class TestRequestValidator:

    # =========================================================================
    # 1. QUERY PARAMETER TESTS (GET)
    # =========================================================================

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_validate_query_param_success(self, mock_get_details):
        """Test that correct query parameters pass validation."""
        # Setup the "Rules"
        mock_get_details.return_value = {
            "query_params": [
                {"name": "page", "required": True, "type": "integer"},
                {"name": "sort", "required": False, "type": "string"},
            ],
            "request_body": None,
            "responses": [],
        }

        # Case 1: All valid
        RequestValidator.validate(
            spec={}, path="/test", method="GET", parameters={"page": 1, "sort": "asc"}
        )

        # Case 2: Optional missing (should still pass)
        RequestValidator.validate(spec={}, path="/test", method="GET", parameters={"page": 5})

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_validate_query_param_missing_required(self, mock_get_details):
        """Test failure when a required query param is missing."""
        mock_get_details.return_value = {
            "query_params": [{"name": "id", "required": True, "type": "integer"}],
            "request_body": None,
        }

        with pytest.raises(ValueError) as exc:
            RequestValidator.validate(
                spec={}, path="/test", method="GET", parameters={}  # 'id' is missing
            )
        assert "Missing required query parameter: 'id'" in str(exc.value)

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_validate_query_param_wrong_type(self, mock_get_details):
        """Test failure when query param has wrong python type."""
        mock_get_details.return_value = {
            "query_params": [{"name": "limit", "required": True, "type": "integer"}],
            "request_body": None,
        }

        with pytest.raises(ValueError) as exc:
            RequestValidator.validate(
                spec={},
                path="/test",
                method="GET",
                parameters={"limit": "10"},  # String instead of Int
            )
        assert "Invalid type for 'query.limit'" in str(exc.value)
        assert "Expected integer" in str(exc.value)

    # =========================================================================
    # 2. REQUEST BODY TESTS (POST/PUT/PATCH)
    # =========================================================================

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_validate_body_success(self, mock_get_details):
        """Test that a valid body passes."""
        mock_get_details.return_value = {
            "query_params": [],
            "request_body": {
                "required": True,
                "type": "UserRequest",
                "properties": [
                    {"name": "username", "type": "string"},
                    {"name": "age", "type": "integer"},
                ],
            },
        }

        RequestValidator.validate(
            spec={}, path="/users", method="POST", parameters={"username": "alice", "age": 30}
        )

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_validate_body_missing_required_body(self, mock_get_details):
        """Test failure when the entire body is required but missing."""
        mock_get_details.return_value = {
            "query_params": [],
            "request_body": {"required": True, "properties": []},  # <--- Body is required
        }

        with pytest.raises(ValueError) as exc:
            RequestValidator.validate(
                spec={}, path="/users", method="POST", parameters=None  # User sent nothing
            )
        assert "Missing required request body" in str(exc.value)

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_validate_body_property_wrong_type(self, mock_get_details):
        """Test failure when a specific body property has the wrong type."""
        mock_get_details.return_value = {
            "query_params": [],
            "request_body": {
                "required": True,
                "properties": [{"name": "is_active", "type": "boolean"}],
            },
        }

        with pytest.raises(ValueError) as exc:
            RequestValidator.validate(
                spec={},
                path="/users",
                method="POST",
                parameters={"is_active": "yes"},  # String instead of Bool
            )
        assert "Invalid type for 'body.is_active'" in str(exc.value)
        assert "Expected boolean" in str(exc.value)

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_validate_body_extra_fields_allowed(self, mock_get_details):
        """
        Test that extra fields in the body NOT defined in spec are ignored
        (standard behavior unless additionalProperties: false is strictly enforced).
        """
        mock_get_details.return_value = {
            "query_params": [],
            "request_body": {"required": True, "properties": [{"name": "name", "type": "string"}]},
        }

        # User sends 'name' AND 'extra_field'
        RequestValidator.validate(
            spec={}, path="/users", method="POST", parameters={"name": "Alice", "extra_field": 123}
        )

    # =========================================================================
    # 3. TYPE CHECKING EDGE CASES
    # =========================================================================

    @pytest.mark.parametrize(
        "openapi_type, valid_value, invalid_value",
        [
            ("integer", 10, "10"),
            ("string", "hello", 123),
            ("boolean", True, "True"),
            ("number", 10.5, "10.5"),  # number allows float or int
            ("number", 10, "10"),
            ("array", [1, 2], {"a": 1}),
            ("object", {"a": 1}, [1, 2]),
            ("array[string]", ["a", "b"], "a string"),  # simplified array check
        ],
    )
    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_all_data_types(self, mock_get_details, openapi_type, valid_value, invalid_value):
        """
        Parametrized test to cover all supported primitive types in _check_type.
        """
        mock_get_details.return_value = {
            "query_params": [],
            "request_body": {
                "required": True,
                "properties": [{"name": "test_field", "type": openapi_type}],
            },
        }

        # 1. Test Valid Value
        RequestValidator.validate(
            spec={}, path="/", method="POST", parameters={"test_field": valid_value}
        )

        # 2. Test Invalid Value
        with pytest.raises(ValueError) as exc:
            RequestValidator.validate(
                spec={}, path="/", method="POST", parameters={"test_field": invalid_value}
            )
        assert f"Invalid type for 'body.test_field'" in str(exc.value)

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_unknown_or_complex_types_skipped(self, mock_get_details):
        """
        Test that if the type is complex (e.g., 'User') or unknown,
        validation is skipped (does not raise error).
        """
        mock_get_details.return_value = {
            "query_params": [],
            "request_body": {
                "required": True,
                "properties": [
                    {"name": "complex_obj", "type": "UserDefinition"},  # Not a primitive
                ],
            },
        }

        # Should pass regardless of what we put in (since we can't validate "UserDefinition" easily)
        RequestValidator.validate(
            spec={}, path="/", method="POST", parameters={"complex_obj": {"any": "structure"}}
        )

    # =========================================================================
    # 4. METHOD ORCHESTRATION
    # =========================================================================

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_ignore_body_on_get(self, mock_get_details):
        """Test that body data is ignored if method is GET."""
        # Setup: GET request defined, but no body info
        mock_get_details.return_value = {
            "query_params": [],
            "request_body": None,  # Spec says no body
        }

        # We send body data anyway
        RequestValidator.validate(
            spec={}, path="/", method="GET", parameters={"should": "be_ignored"}
        )
        # Should pass without error

    @patch("domaintools.docstring_patcher.DocstringPatcher.get_operation_details")
    def test_ignore_query_on_post(self, mock_get_details):
        """Test that query params are ignored (not validated) if method is POST."""
        # Spec says 'id' is required if we were looking at query params
        mock_get_details.return_value = {
            "query_params": [{"name": "id", "required": True, "type": "integer"}],
            "request_body": None,
        }

        # We call POST, passing NO query params.
        # Since POST logic only checks body, this should NOT complain about missing 'id'.
        RequestValidator.validate(spec={}, path="/", method="POST", parameters={})
