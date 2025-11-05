import pytest
import inspect

# Import the class to be tested
from domaintools.docstring_patcher import DocstringPatcher
from domaintools.utils import api_endpoint


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
                    # NOTE: No 'parameters' key here, will inherit from GET
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

    class MockAPI:
        def __init__(self, specs):
            self.specs = specs

        @api_endpoint(spec_name="v1", path="/users", methods=["get", "post"])
        def user_operations(self):
            """This is the original user docstring."""
            return "user_operations_called"

        @api_endpoint(spec_name="v1", path="/pets/{petId}", methods="get")
        def get_pet(self):
            """Original pet docstring."""
            return "get_pet_called"

        @api_endpoint(spec_name="v1", path="/health", methods="get")
        def health_check(self):
            """Original health docstring."""
            return "health_check_called"

        @api_endpoint(spec_name="v2_nonexistent", path="/users", methods="get")
        def bad_spec_name(self):
            """Original bad spec docstring."""
            return "bad_spec_called"

        @api_endpoint(spec_name="v1", path="/nonexistent-path", methods="get")
        def bad_path(self):
            """Original bad path docstring."""
            return "bad_path_called"

        def not_an_api_method(self):
            """Internal method docstring."""
            return "internal_called"

    api_instance = MockAPI(specs={"v1": sample_spec})
    return api_instance


# --- Original Test Cases (Updated) ---


def test_patch_method_still_callable(patcher, mock_api_instance):
    """
    Ensures that after patching, the method can still be called
    and returns its original value.
    """
    patcher.patch(mock_api_instance)
    assert mock_api_instance.user_operations() == "user_operations_called"
    assert mock_api_instance.get_pet() == "get_pet_called"


def test_patch_leaves_unmarked_methods_alone(patcher, mock_api_instance):
    """
    Tests that methods without the decorator are not modified.
    """
    original_doc = inspect.getdoc(mock_api_instance.not_an_api_method)
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.not_an_api_method)
    assert new_doc == original_doc
    assert new_doc == "Internal method docstring."


def test_patch_preserves_original_docstring(patcher, mock_api_instance):
    """
    Tests that the new docstring starts with the original docstring.
    """
    original_doc = inspect.getdoc(mock_api_instance.user_operations)
    assert original_doc == "This is the original user docstring."
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.user_operations)
    assert new_doc.startswith(original_doc)
    assert len(new_doc) > len(original_doc)


def test_patch_handles_multiple_operations_and_inheritance(patcher, mock_api_instance):
    """
    Tests that a method with methods=["get", "post"] gets docs
    for BOTH operations and that POST inherits GET's params.
    """
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.user_operations)

    # Check for original doc
    assert new_doc.startswith("This is the original user docstring.")

    # --- Check GET operation details (the source) ---
    get_section_index = new_doc.find("--- Operation: GET /users ---")
    assert get_section_index != -1
    get_section = new_doc[get_section_index:]

    assert "Summary: Get all users" in get_section
    assert "External Doc: http://docs.example.com/get-users" in get_section
    assert "**status** (string)" in get_section
    assert "Required:    True" in get_section
    assert "Description: User's current status." in get_section
    assert "**limit** (integer)" in get_section  # $ref'd param
    assert "Description: Max number of items to return." in get_section

    # --- Check POST operation details (the inheritor) ---
    post_section_index = new_doc.find("--- Operation: POST /users ---")
    assert post_section_index != -1
    post_section = new_doc[post_section_index:]

    assert "Summary: Create a new user" in post_section
    assert "Request Body:" in post_section
    assert "**User**" in post_section  # $ref'd body

    # --- Check for INHERITED parameters ---
    assert "**status** (string)" in post_section
    assert "Required:    True" in post_section
    assert "Description: User's current status." in post_section
    assert "**limit** (integer)" in post_section
    assert "Description: Max number of items to return." in post_section


def test_patch_handles_single_operation(patcher, mock_api_instance):
    """
    Tests a path with only one operation (GET) and no params/body.
    """
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.get_pet)

    assert new_doc.startswith("Original pet docstring.")
    assert "--- Operation: GET /pets/{petId} ---" in new_doc
    assert "Summary: Get a single pet" in new_doc
    assert "Query Parameters:\n    (No query parameters)" in new_doc
    assert "Request Body:\n    (No request body)" in new_doc
    assert "--- Operation: POST /pets/{petId} ---" not in new_doc


def test_patch_spec_not_found(patcher, mock_api_instance):
    """
    Tests error message if the spec name isn't in the 'specs' dict.
    """
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.bad_spec_name)
    assert new_doc.startswith("Original bad spec docstring.")
    assert "--- API Details Error ---" in new_doc
    assert "Could not find operations ['get']" in new_doc
    assert "for path '/users'" in new_doc


def test_patch_path_not_found(patcher, mock_api_instance):
    """
    Tests error message if the path is not in the spec file.
    """
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.bad_path)
    assert new_doc.startswith("Original bad path docstring.")
    assert "--- API Details Error ---" in new_doc
    assert "for path '/nonexistent-path'" in new_doc


def test_patch_path_found_but_no_operations(patcher, mock_api_instance):
    """
    Tests error message if the path is in the spec
    but the specific method ("get") is not.
    """
    patcher.patch(mock_api_instance)
    new_doc = inspect.getdoc(mock_api_instance.health_check)
    assert new_doc.startswith("Original health docstring.")
    assert "--- API Details Error ---" in new_doc
    assert "for path '/health'" in new_doc


def test_post_inherits_get_parameters(patcher):
    """
    Tests that a POST operation with no parameters defined
    successfully inherits parameters from the GET operation
    at the same path.
    """
    # Arrange: Create a minimal spec to test this exact behavior
    inheritance_spec = {
        "openapi": "3.0.0",
        "info": {"title": "Inheritance Test API"},
        "paths": {
            "/widgets": {
                "get": {
                    "summary": "Get widgets",
                    "parameters": [
                        {
                            "name": "color",
                            "in": "query",
                            "description": "Widget color",
                            "schema": {"type": "string"},
                        }
                    ],
                },
                "post": {
                    "summary": "Create a widget",
                    # No 'parameters' key, should inherit from GET.
                    "requestBody": {"description": "Widget to create"},
                },
            }
        },
    }

    class MockAPI:
        def __init__(self, specs):
            self.specs = specs

        @api_endpoint(spec_name="v1", path="/widgets", methods=["get", "post"])
        def widget_operations(self):
            """Original widget docstring."""
            pass

    api_instance = MockAPI(specs={"v1": inheritance_spec})

    patcher.patch(api_instance)
    new_doc = inspect.getdoc(api_instance.widget_operations)

    # Assert
    assert new_doc.startswith("Original widget docstring.")

    # Find the POST section and check for INHERITED params
    post_section_index = new_doc.find("--- Operation: POST /widgets ---")
    assert post_section_index > -1, "POST operation section not found"

    post_section = new_doc[post_section_index:]
    assert "Summary: Create a widget" in post_section
    assert "**color** (string)" in post_section
    assert "Widget color" in post_section


def test_post_does_not_inherit_when_get_has_no_params(patcher):
    """
    Tests that a POST operation does not inherit anything
    if the GET operation also has no parameters.
    """
    no_params_spec = {
        "openapi": "3.0.0",
        "paths": {
            "/items": {
                "get": {"summary": "Get items"},
                "post": {"summary": "Create an item"},
            }
        },
    }

    class MockAPI:
        def __init__(self, specs):
            self.specs = specs

        @api_endpoint(spec_name="v1", path="/items", methods=["get", "post"])
        def item_operations(self):
            """Original item docstring."""
            pass

    api_instance = MockAPI(specs={"v1": no_params_spec})

    patcher.patch(api_instance)
    new_doc = inspect.getdoc(api_instance.item_operations)

    # Check GET section
    get_section_index = new_doc.find("--- Operation: GET /items ---")
    get_section = new_doc[get_section_index:]
    assert "Query Parameters:\n    (No query parameters)" in get_section

    # Check POST section
    post_section_index = new_doc.find("--- Operation: POST /items ---")
    post_section = new_doc[post_section_index:]
    assert "Query Parameters:\n    (No query parameters)" in post_section
