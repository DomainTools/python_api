import pytest
from unittest.mock import Mock, patch
from domaintools.decorators import api_endpoint


@pytest.fixture
def api_specs():
    """
    A fixture that acts as a central registry for all test OpenAPI specs.
    """
    return {
        # --- Spec V1: Standard ---
        "v1": {
            "openapi": "3.0.0",
            "info": {"title": "Standard Spec", "version": "1.0.0"},
            "paths": {
                "/users": {
                    "get": {
                        "parameters": [
                            {
                                "name": "status",
                                "in": "query",
                                "required": True,
                                "schema": {"type": "string"},
                            }
                        ]
                    },
                    "post": {
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "age": {"type": "integer"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        # --- Spec V3: Complex Lookup (Matches parameter name in components) ---
        "v3_complex": {
            "openapi": "3.0.0",
            "info": {"title": "Complex Lookup Spec", "version": "3.0.0"},
            "components": {
                "parameters": {
                    "LimitParam": {
                        "name": "limit",
                        "in": "query",
                        "description": "Max number of items.",
                        "schema": {"type": "integer"},
                    }
                },
                "schemas": {
                    "UserRequestParameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                # The validator/patcher should match this name to 'LimitParam' above
                                "$ref:": "#/components/schemas/IgnoredRef",
                            },
                        },
                    },
                },
                "requestBodies": {
                    "UserBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserRequestParameters"},
                            },
                        },
                    }
                },
            },
            "paths": {
                "/users": {
                    "post": {
                        "requestBody": {"$ref": "#/components/requestBodies/UserBody"},
                    },
                },
            },
        },
    }


@pytest.fixture
def mock_client(api_specs):
    """
    Creates a mock API client that is pre-patched with the specs defined above.
    """
    client = Mock()
    client.specs = api_specs
    return client


class TestApiEndpointDecorator:

    def test_metadata_preservation(self, mock_client):
        """
        Ensure decorator copies metadata for DocstringPatcher.
        """

        @api_endpoint(spec_name="v1", path="/users", methods="GET")
        def get_users():
            """Original Docstring"""
            pass

        bound_method = get_users.__get__(mock_client, Mock)

        assert bound_method._api_spec_name == "v1"
        assert bound_method._api_path == "/users"
        assert bound_method._api_methods == ["GET"]
        assert bound_method.__doc__ == "Original Docstring"

    def test_valid_post_request(self, mock_client):
        """
        Test a valid POST request against 'v1' spec.
        """

        @api_endpoint(spec_name="v1", path="/users", methods="POST")
        def create_user(request_body=None):
            return "Created"

        # Mocking validate to ensure arguments are passed correctly,
        # but we could also let it run against the real logic if we wanted integration tests.
        with patch("domaintools.request_validator.RequestValidator.validate") as mock_validate:
            result = create_user(mock_client, request_body={"name": "Alice", "age": 30})

            assert result == "Created"

            # Check arguments passed to validator
            call_kwargs = mock_validate.call_args[1]
            assert call_kwargs["spec"] == mock_client.specs["v1"]
            assert call_kwargs.get("parameters", {}).get("request_body") == {
                "name": "Alice",
                "age": 30,
            }

    def test_validation_failure_blocks_execution(self, mock_client):
        """
        Test that if validation fails, the function doesn't run.
        """
        inner_logic = Mock()

        @api_endpoint(spec_name="v1", path="/users", methods="POST")
        def create_user(body=None):
            inner_logic()

        # Simulate a validation error
        with patch(
            "domaintools.request_validator.RequestValidator.validate",
            side_effect=ValueError("Bad Input"),
        ):
            with pytest.raises(ValueError, match="Bad Input"):
                create_user(mock_client, body={"bad": "data"})

            inner_logic.assert_not_called()

    def test_complex_spec_lookup_integration(self, mock_client):
        """
        Test that the decorator works with the complex 'v3_complex' spec
        we defined in the fixture.
        """

        @api_endpoint(spec_name="v3_complex", path="/users", methods="POST")
        def create_user_complex(body=None):
            return "Complex Success"

        with patch("domaintools.request_validator.RequestValidator.validate") as mock_validate:
            create_user_complex(mock_client, body={"limit": 10})

            # Verify the correct spec dictionary was retrieved and passed
            call_kwargs = mock_validate.call_args[1]
            assert call_kwargs["spec"]["info"]["title"] == "Complex Lookup Spec"
            assert call_kwargs["path"] == "/users"

    def test_missing_spec_skips_validation(self, mock_client):
        """
        If we ask for a spec name that isn't in the fixture, it should handle gracefully.
        """

        @api_endpoint(spec_name="non_existent_version", path="/users", methods="GET")
        def get_users():
            return "Ran Safe"

        with patch("domaintools.request_validator.RequestValidator.validate") as mock_validate:
            result = get_users(mock_client)

            assert result == "Ran Safe"
            mock_validate.assert_not_called()

    def test_positional_arguments_are_mapped(self, mock_client):
        """
        Test that passing arguments positionally (args) instead of via keywords (kwargs)
        still triggers validation correctly.
        """

        # Define function with explicit parameter names
        @api_endpoint(spec_name="v1", path="/users", methods="POST")
        def create_user(name=None, body=None):
            return "Success"

        with patch("domaintools.request_validator.RequestValidator.validate") as mock_validate:
            # CALL POSITIONALLY: passing client and body as args
            # (Note: we pass mock_client manually because create_user is just a function here)
            create_user(mock_client, "test-name")

            # Verify validator received the data mapped to 'body_data'
            mock_validate.assert_called_once()
            call_kwargs = mock_validate.call_args[1]

            assert call_kwargs.get("parameters") == {"name": "test-name"}
