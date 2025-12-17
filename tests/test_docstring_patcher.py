import logging
import types

from unittest.mock import Mock

from domaintools.docstring_patcher import DocstringPatcher


class TestDocstringPatcher:

    def _setup_mock_api(
        self,
        spec_dict: dict,
        spec_name: str,
        method_name: str,
        path: str,
        http_methods: list,
        docstring: str,
    ) -> Mock:
        """
        Helper to create a mock API instance with a mock decorated method.
        """
        # Create the mock API instance
        mock_api = Mock()
        mock_api.specs = {spec_name: spec_dict}

        # Create the underlying function that was decorated
        def original_func():
            """Original docstring."""
            pass

        original_func.__doc__ = docstring
        original_func._api_spec_name = spec_name
        original_func._api_path = path
        original_func._api_methods = http_methods

        # Create the mock instance method
        mock_method = types.MethodType(original_func, mock_api)
        setattr(mock_api, method_name, mock_method)

        return mock_api, method_name

    def setup_method(self, method):
        """Pytest setup hook, runs before each test."""
        self.patcher = DocstringPatcher()

        # SPEC 1: The very first spec with non-standard 'parameters' in requestBody
        self.SPEC_1_NON_STANDARD_PARAMS = {
            "openapi": "3.0.0",
            "info": {"title": "Spec 1"},
            "components": {
                "parameters": {
                    "LimitParam": {
                        "name": "limit",
                        "in": "query",
                        "description": "Max number of items.",
                        "schema": {"type": "integer"},
                    }
                },
                "schemas": {"User": {"type": "object"}},
                "requestBodies": {
                    "UserBody": {
                        "description": "User object.",
                        "required": True,
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/User"}}
                        },
                        "parameters": [{"$ref": "#/components/parameters/LimitParam"}],
                    }
                },
            },
            "paths": {
                "/users": {
                    "post": {
                        "summary": "Create user",
                        "requestBody": {"$ref": "#/components/requestBodies/UserBody"},
                    },
                }
            },
        }

        # SPEC 2: The spec with UserRequestParameters (name, age)
        self.SPEC_2_SCHEMA_PROPS = {
            "openapi": "3.0.0",
            "info": {"title": "Spec 2"},
            "components": {
                "schemas": {
                    "UserRequestParameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "User's name"},
                            "age": {"type": "int", "description": "User's age"},
                        },
                    },
                },
                "requestBodies": {
                    "UserBody": {
                        "description": "User object to create.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserRequestParameters"}
                            }
                        },
                    }
                },
            },
            "paths": {
                "/users": {
                    "post": {
                        "summary": "Create a new user",
                        "requestBody": {"$ref": "#/components/requestBodies/UserBody"},
                    },
                }
            },
        }

        # SPEC 3: The final spec with the "lookup-by-name" logic
        self.SPEC_3_LOOKUP_BY_NAME = {
            "openapi": "3.0.0",
            "info": {"title": "Spec 3"},
            "components": {
                "parameters": {
                    "LimitParam": {
                        "name": "limit",
                        "in": "query",
                        "description": "Max number of items to return.",
                        "schema": {"type": "integer"},
                    }
                },
                "schemas": {
                    "UserRequestParameters": {
                        "type": "object",
                        "properties": {"limit": {"$ref:": "#/components/schemas/ApexDomain"}},
                    },
                },
                "requestBodies": {
                    "UserBody": {
                        "description": "User object to create.",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserRequestParameters"}
                            }
                        },
                    }
                },
            },
            "paths": {
                "/users": {
                    "post": {
                        "summary": "Create a new user",
                        "requestBody": {"$ref": "#/components/requestBodies/UserBody"},
                    },
                }
            },
        }

        # SPEC 4: A full spec for GET, including Responses
        self.SPEC_4_WITH_RESPONSE = {
            "openapi": "3.0.0",
            "info": {"title": "Spec 4"},
            "components": {
                "parameters": {
                    "LimitParam": {
                        "name": "limit",
                        "in": "query",
                        "description": "Max items.",
                        "schema": {"type": "integer"},
                    }
                },
                "schemas": {"User": {"type": "object"}},
            },
            "paths": {
                "/users": {
                    "get": {
                        "summary": "Get all users",
                        "parameters": [
                            {
                                "name": "status",
                                "in": "query",
                                "required": True,
                                "description": "User status.",
                                "schema": {"type": "string"},
                            },
                            {"$ref": "#/components/parameters/LimitParam"},
                        ],
                        "responses": {
                            "200": {
                                "description": "A list of users.",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/User"},
                                        }
                                    }
                                },
                            }
                        },
                    },
                }
            },
        }

    def test_spec_1_non_standard_params(self):
        """
        Tests the first spec: parameters inside requestBody should
        be displayed under 'Request Body'.
        """
        mock_api, method_name = self._setup_mock_api(
            spec_dict=self.SPEC_1_NON_STANDARD_PARAMS,
            spec_name="spec1",
            method_name="create_user",
            path="/users",
            http_methods=["post"],
            docstring="This creates a user.",
        )

        self.patcher.patch(mock_api)

        doc = getattr(mock_api, method_name).__doc__

        assert "This creates a user." in doc
        assert "--- Operation: POST /users ---" in doc
        assert "Request Body:" in doc
        assert "**User**" in doc
        assert "Parameters (associated with this body):" in doc
        assert "**limit** (integer) [in: query]" in doc
        assert "Description: Max number of items." in doc
        assert "Query Parameters:" in doc
        assert "(No query parameters)" in doc

    def test_spec_2_schema_props(self):
        """
        Tests the second spec: requestBody schema properties (name, age)
        should be unpacked and displayed.
        """
        mock_api, method_name = self._setup_mock_api(
            spec_dict=self.SPEC_2_SCHEMA_PROPS,
            spec_name="spec2",
            method_name="create_user",
            path="/users",
            http_methods=["post"],
            docstring="Creates user.",
        )

        self.patcher.patch(mock_api)

        doc = getattr(mock_api, method_name).__doc__

        assert "Creates user." in doc
        assert "--- Operation: POST /users ---" in doc
        assert "Request Body:" in doc
        assert "**UserRequestParameters**" in doc
        assert "Description: User object to create." in doc
        assert "Properties:" in doc
        assert "**name** (string)" in doc
        assert "Description: User's name" in doc
        assert "**age** (int)" in doc
        assert "Description: User's age" in doc
        assert "Parameters (associated with this body):" not in doc

    def test_spec_3_lookup_by_name(self):
        """
        Tests the final spec: requestBody property 'limit' should
        be matched with components.parameters.LimitParam by name.
        """
        mock_api, method_name = self._setup_mock_api(
            spec_dict=self.SPEC_3_LOOKUP_BY_NAME,
            spec_name="spec3",
            method_name="create_user",
            path="/users",
            http_methods=["post"],
            docstring="Creates user.",
        )

        self.patcher.patch(mock_api)

        doc = getattr(mock_api, method_name).__doc__

        assert "--- Operation: POST /users ---" in doc
        assert "Request Body:" in doc
        assert "**UserRequestParameters**" in doc
        assert "Properties:" in doc
        # This is the key assertion:
        assert "**limit** (integer)" in doc
        assert "Description: Max number of items to return." in doc
        # Ensure it didn't use the $ref: value
        assert "ApexDomain" not in doc

    def test_spec_4_get_with_response(self):
        """
        Tests a GET operation with query params and a response.
        """
        mock_api, method_name = self._setup_mock_api(
            spec_dict=self.SPEC_4_WITH_RESPONSE,
            spec_name="spec4",
            method_name="get_users",
            path="/users",
            http_methods=["get"],
            docstring="Gets users.",
        )

        self.patcher.patch(mock_api)

        doc = getattr(mock_api, method_name).__doc__

        assert "Gets users." in doc
        assert "--- Operation: GET /users ---" in doc

        # Check Query Params
        assert "Query Parameters:" in doc
        assert "**status** (string)" in doc
        assert "Required:    True" in doc
        assert "Description: User status." in doc
        assert "**limit** (integer)" in doc
        assert "Description: Max items." in doc

        # Check Request Body
        assert "Request Body:" in doc
        assert "(No request body)" in doc

        # Check Responses
        assert "Result Body (Responses):" in doc
        assert "**200**: (array[User])" in doc
        assert "Description: A list of users." in doc

    def test_patching_error_path(self, caplog):
        """
        Tests that a failure to find the operation generates the
        correct error docstring and logs a warning.
        """
        mock_api, method_name = self._setup_mock_api(
            spec_dict=self.SPEC_1_NON_STANDARD_PARAMS,  # Spec doesn't matter
            spec_name="spec1",
            method_name="get_pets",
            path="/pets",  # This path doesn't exist in the spec
            http_methods=["get"],
            docstring="Original doc.",
        )

        with caplog.at_level(logging.WARNING):
            self.patcher.patch(mock_api)

        doc = getattr(mock_api, method_name).__doc__

        assert "Original doc." in doc
        assert "--- API Details Error ---" in doc
        assert "(Could not find operations ['get'] for path '/pets' in spec 'spec1')" in doc

        # Test that no *parsing* error was logged
        assert "Error parsing spec" not in caplog.text
