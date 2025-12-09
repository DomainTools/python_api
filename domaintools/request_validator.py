from domaintools.docstring_patcher import DocstringPatcher


class RequestValidator:
    """
    Validates user input against the OpenAPI spec using DocstringPatcher.
    Separates validation logic based on HTTP verbs.
    """

    TYPE_MAP = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    @staticmethod
    def validate(
        spec: dict,
        path: str,
        method: str,
        parameters: dict = None,
    ):
        """
        Orchestrator: Decides which validation to run based on the HTTP method.
        """
        method = method.upper()

        # GET requests: Validate Query Parameters only
        if method == "GET":
            RequestValidator.validate_query_params(spec, path, method, parameters)

        # POST/PUT/PATCH: Validate Request Body
        elif method in ["POST", "PUT", "PATCH"]:
            RequestValidator.validate_body(spec, path, method, parameters)

        return True

    @staticmethod
    def validate_query_params(spec: dict, path: str, method: str, q_params: dict):
        """
        Validates ONLY the query parameters.
        """
        q_params = q_params or {}
        details = DocstringPatcher.get_operation_details(spec, path, method)
        errors = []

        for param in details["query_params"]:
            param_name = param["name"]
            is_required = param["required"]
            param_type = param["type"]

            # Check existence
            if is_required and param_name not in q_params:
                errors.append(f"Missing required query parameter: '{param_name}'")
                continue

            # Check Type (only if present)
            if param_name in q_params:
                val = q_params[param_name]
                RequestValidator._check_type(val, param_type, f"query.{param_name}", errors)

        if errors:
            raise ValueError("Query Parameter Validation Failed:\n  - " + "\n  - ".join(errors))

    @staticmethod
    def validate_body(spec: dict, path: str, method: str, body_data: dict):
        """
        Validates ONLY the request body.
        """
        details = DocstringPatcher.get_operation_details(spec, path, method)
        errors = []

        if not details["request_body"]:
            # If spec has no body defined, but user sent one, you might want to warn
            # or simply ignore. We will ignore here.
            return

        body_rules = details["request_body"]

        # Check Body Existence
        if not body_data:
            raise ValueError("Validation Failed: Missing required request body.")

        # Check Body Properties
        # Only proceed if we have data and the spec defines properties
        if body_data and body_rules.get("properties"):
            for prop in body_rules["properties"]:
                p_name = prop["name"]
                p_type = prop["type"]

                # Check Type if the property exists in the user input
                if p_name in body_data:
                    RequestValidator._check_type(
                        body_data[p_name], p_type, f"body.{p_name}", errors
                    )

        if errors:
            raise ValueError("Body Validation Failed:\n  - " + "\n  - ".join(errors))

    @staticmethod
    def _check_type(value, openapi_type, field_name, errors):
        """Helper to check python types against OpenAPI string types."""
        simple_type = openapi_type

        if "array" in openapi_type:
            simple_type = "array"
        elif openapi_type not in RequestValidator.TYPE_MAP:
            return

        expected_type = RequestValidator.TYPE_MAP.get(simple_type)

        if expected_type and not isinstance(value, expected_type):
            errors.append(
                f"Invalid type for '{field_name}'. Expected {simple_type}, got {type(value).__name__}."
            )
