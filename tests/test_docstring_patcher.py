import pytest
import inspect
import functools

from domaintools.docstring_patcher import DocstringPatcher


@pytest.fixture
def patcher():
    """Returns an instance of the class under test."""
    return DocstringPatcher()


@pytest.fixture(scope="module")
def sample_spec():
    """
    Provides a comprehensive, reusable mock OpenAPI spec dictionary.
    """
    return {
        "openapi": "3.0.0",
        "info": {"title": "Test API", "version": "1.0.0"},
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
                "User": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                }
            },
            "requestBodies": {
                "UserBody": {
                    "description": "User object to create.",
                    "required": True,
                    "content": {
                        "application/json": {"schema": {"$ref": "#/components/schemas/User"}}
                    },
                }
            },
        },
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get all users",
                    "description": "Returns a list of users.",
                    "externalDocs": {"url": "http://docs.example.com/get-users"},
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "required": True,
                            "description": "User's current status.",
                            "schema": {"type": "string"},
                        },
                        {"$ref": "#/components/parameters/LimitParam"},
                    ],
                },
                "post": {
                    "summary": "Create a new user",
                    "description": "Creates a single new user.",
                    "requestBody": {"$ref": "#/components/requestBodies/UserBody"},
                },
            },
            "/pets/{petId}": {
                "get": {
                    "summary": "Get a single pet",
                    "description": "Returns one pet by ID.",
                }
            },
            "/health": {
                # This path exists, but has no operations (get, post, etc.)
                "description": "Health check path."
            },
        },
    }


@pytest.fixture
def mock_api_instance(sample_spec):
    """
    Provides a mock API instance with decorated methods
    that the DocstringPatcher will look for.
    """

    # This decorator mimics the one you'd use in your real API class
    def api_endpoint(spec_name, path):
        def decorator(func):
            func._api_spec_name = spec_name
            func._api_path = path

            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    class MockAPI:
        def __init__(self, specs):
            # The patcher expects the instance to have a 'specs' attribute
            self.specs = specs

        @api_endpoint(spec_name="v1", path="/users")
        def user_operations(self):
            """This is the original user docstring."""
            return "user_operations_called"

        @api_endpoint(spec_name="v1", path="/pets/{petId}")
        def get_pet(self):
            """Original pet docstring."""
            return "get_pet_called"

        @api_endpoint(spec_name="v1", path="/health")
        def health_check(self):
            """Original health docstring."""
            return "health_check_called"

        @api_endpoint(spec_name="v2_nonexistent", path="/users")
        def bad_spec_name(self):
            """Original bad spec docstring."""
            return "bad_spec_called"

        @api_endpoint(spec_name="v1", path="/nonexistent-path")
        def bad_path(self):
            """Original bad path docstring."""
            return "bad_path_called"

        def not_an_api_method(self):
            """Internal method docstring."""
            return "internal_called"

    # Create an instance, passing in the spec fixture
    api_instance = MockAPI(specs={"v1": sample_spec})
    return api_instance


# --- Test Cases ---


def test_patch_method_still_callable(patcher, mock_api_instance):
    """
    Ensures that after patching, the method can still be called
    and returns its original value.
    """
    # Act
    patcher.patch(mock_api_instance)

    # Assert
    assert mock_api_instance.user_operations() == "user_operations_called"
    assert mock_api_instance.get_pet() == "get_pet_called"


def test_patch_leaves_unmarked_methods_alone(patcher, mock_api_instance):
    """
    Tests that methods without the decorator are not modified.
    """
    # Arrange
    original_doc = inspect.getdoc(mock_api_instance.not_an_api_method)

    # Act
    patcher.patch(mock_api_instance)

    # Assert
    new_doc = inspect.getdoc(mock_api_instance.not_an_api_method)
    assert new_doc == original_doc
    assert new_doc == "Internal method docstring."


def test_patch_preserves_original_docstring(patcher, mock_api_instance):
    """
    Tests that the new docstring starts with the original docstring.
    """
    # Arrange
    original_doc = inspect.getdoc(mock_api_instance.user_operations)
    assert original_doc == "This is the original user docstring."

    # Act
    patcher.patch(mock_api_instance)

    # Assert
    new_doc = inspect.getdoc(mock_api_instance.user_operations)
    assert new_doc.startswith(original_doc)
    assert len(new_doc) > len(original_doc)


def test_patch_handles_multiple_operations(patcher, mock_api_instance):
    """
    Tests that a single method gets docs for ALL operations
    on its path (e.g., GET and POST for /users).
    """
    # Act
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.user_operations)

    # Assert
    # Check for original doc
    assert new_doc.startswith("This is the original user docstring.")

    # Check for GET operation details
    assert "--- Operation: GET /users ---" in new_doc
    assert "Summary: Get all users" in new_doc
    assert "External Doc: http://docs.example.com/get-users" in new_doc
    assert "**status** (string)" in new_doc
    assert "Required:    True" in new_doc
    assert "Description: User's current status." in new_doc

    # Check for $ref'd query param
    assert "**limit** (integer)" in new_doc
    assert "Description: Max number of items to return." in new_doc

    # Check for POST operation details
    assert "--- Operation: POST /users ---" in new_doc
    assert "Summary: Create a new user" in new_doc
    assert "Request Body:" in new_doc

    # Check for $ref'd request body
    assert "**User**" in new_doc
    assert "Description: User object to create." in new_doc
    assert "Required:    True" in new_doc


def test_patch_handles_single_operation(patcher, mock_api_instance):
    """
    Tests a path with only one operation (GET) and no params/body.
    """
    # Act
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.get_pet)

    # Assert
    assert new_doc.startswith("Original pet docstring.")
    assert "--- Operation: GET /pets/{petId} ---" in new_doc
    assert "Summary: Get a single pet" in new_doc

    # Check for empty sections
    assert "Query Parameters:\n    (No query parameters)" in new_doc
    assert "Request Body:\n    (No request body)" in new_doc

    # Ensure other methods aren't included
    assert "--- Operation: POST /pets/{petId} ---" not in new_doc


def test_patch_spec_not_found(patcher, mock_api_instance):
    """
    Tests that an error message is added to the doc if the
    spec name (e.g., 'v2_nonexistent') isn't in the instance's 'specs' dict.
    """
    # Act
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.bad_spec_name)

    # Assert
    assert new_doc.startswith("Original bad spec docstring.")
    # Check for the specific error message your code generates
    assert "--- API Details Error ---" in new_doc
    assert "(Could not find any operations for path '/users')" in new_doc


def test_patch_path_not_found(patcher, mock_api_instance):
    """
    Tests that an error message is added if the path exists on the method
    but not in the spec file.
    """
    # Act
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.bad_path)

    # Assert
    assert new_doc.startswith("Original bad path docstring.")
    assert "--- API Details Error ---" in new_doc
    assert "(Could not find any operations for path '/nonexistent-path')" in new_doc


def test_patch_path_found_but_no_operations(patcher, mock_api_instance):
    """
    Tests that an error message is added if the path (/health) is in
    the spec but has no operations (get, post, etc.) defined.
    """
    # Act
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.health_check)

    # Assert
    assert new_doc.startswith("Original health docstring.")
    assert "--- API Details Error ---" in new_doc
    assert "(Could not find any operations for path '/health')" in new_doc
