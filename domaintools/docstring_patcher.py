import inspect
import functools
import textwrap
import logging


class DocstringPatcher:
    """
    Patches docstrings for methods decorated with @api_endpoint.
    """

    def patch(self, api_instance):
        method_names = []
        for attr_name in dir(api_instance):
            attr = getattr(api_instance, attr_name)
            if (
                inspect.ismethod(attr)
                and hasattr(attr, "_api_spec_name")
                and hasattr(attr, "_api_path")
                and hasattr(attr, "_api_methods")
            ):
                method_names.append(attr_name)

        for attr_name in method_names:
            original_method = getattr(api_instance, attr_name)
            original_function = original_method.__func__

            spec_name = getattr(original_function, "_api_spec_name", None)
            path = getattr(original_function, "_api_path", None)
            http_methods_to_check = getattr(original_function, "_api_methods", [])

            spec_to_use = api_instance.specs.get(spec_name)
            original_doc = inspect.getdoc(original_function) or ""

            all_doc_sections = []
            if spec_to_use:
                path_item = spec_to_use.get("paths", {}).get(path, {})
                for http_method in http_methods_to_check:
                    if http_method.lower() in path_item:
                        # Helper is called via self, but it's an instance method calling a static method internally
                        api_doc = self._generate_api_doc_string(spec_to_use, path, http_method)
                        all_doc_sections.append(api_doc)

            if not all_doc_sections:
                all_doc_sections.append(
                    f"\n--- API Details Error ---"
                    f"\n  (Could not find operations {http_methods_to_check} for path '{path}' in spec '{spec_name}')"
                )

            new_doc = textwrap.dedent(original_doc) + "\n\n" + "\n\n".join(all_doc_sections)

            @functools.wraps(original_function)
            def method_wrapper(*args, _orig_meth=original_method, **kwargs):
                return _orig_meth(*args, **kwargs)

            method_wrapper.__doc__ = new_doc
            setattr(
                api_instance,
                attr_name,
                method_wrapper.__get__(api_instance, api_instance.__class__),
            )

    @staticmethod
    def get_operation_details(spec: dict, path: str, method: str) -> dict:
        """
        Gets all details for a specific operation.
        Static method: Can be used without instantiating the class.
        Usage: DocstringPatcher.get_operation_details(spec, '/users', 'post')
        """
        details = {"query_params": [], "request_body": None, "responses": []}
        if not spec:
            return details

        try:
            components = spec.get("components", {})
            all_component_params = components.get("parameters", {})

            path_item = spec.get("paths", {}).get(path, {})
            operation = path_item.get(method.lower(), {})
            if not operation:
                return details

            # --- Parameter Logic ---
            path_level_params = path_item.get("parameters", [])
            operation_level_params = operation.get("parameters", [])
            body_level_params = []

            body_def = operation.get("requestBody")
            resolved_body_def = {}
            if body_def:
                if "$ref" in body_def:
                    resolved_body_def = DocstringPatcher._resolve_ref(spec, body_def["$ref"])
                else:
                    resolved_body_def = body_def
                body_level_params = resolved_body_def.get("parameters", [])

            all_param_defs = path_level_params + operation_level_params

            details["summary"] = operation.get("summary")
            details["description"] = operation.get("description")
            details["external_doc"] = operation.get("externalDocs", {}).get("url", "N/A")

            # --- Query Params ---
            resolved_params = []
            for param_def in all_param_defs:
                if "$ref" in param_def:
                    resolved_params.append(DocstringPatcher._resolve_ref(spec, param_def["$ref"]))
                else:
                    resolved_params.append(param_def)

            for p in [p for p in resolved_params if p.get("in") == "query"]:
                details["query_params"].append(
                    {
                        "name": p.get("name"),
                        "required": p.get("required", False),
                        "description": p.get("description", "N/A"),
                        "type": DocstringPatcher._get_param_type(spec, p.get("schema")),
                    }
                )

            # --- Request Body ---
            if body_def:
                content = resolved_body_def.get("content", {})
                media_type = next(iter(content.values()), None)
                schema_type = "N/A"
                schema = {}

                if media_type and "schema" in media_type:
                    schema = media_type["schema"]
                    schema_type = DocstringPatcher._get_param_type(spec, schema)

                details["request_body"] = {
                    "required": resolved_body_def.get("required", False),
                    "description": resolved_body_def.get("description", "N/A"),
                    "type": schema_type,
                    "parameters": [],
                    "properties": [],
                }

                # --- Schema Properties ---
                resolved_schema = {}
                current_schema_for_props = schema
                while "$ref" in current_schema_for_props or "$ref:" in current_schema_for_props:
                    ref = current_schema_for_props.get("$ref") or current_schema_for_props.get(
                        "$ref:"
                    )
                    if not ref:
                        break
                    current_schema_for_props = DocstringPatcher._resolve_ref(spec, ref)

                if (
                    current_schema_for_props.get("type") == "object"
                    and "properties" in current_schema_for_props
                ):
                    for prop_name, prop_def in current_schema_for_props["properties"].items():

                        found_param_match = False
                        for component_param_def in all_component_params.values():
                            if component_param_def.get("name") == prop_name:
                                prop_type = DocstringPatcher._get_param_type(
                                    spec, component_param_def.get("schema")
                                )
                                prop_desc = component_param_def.get("description", "N/A")
                                details["request_body"]["properties"].append(
                                    {"name": prop_name, "type": prop_type, "description": prop_desc}
                                )
                                found_param_match = True
                                break

                        if not found_param_match:
                            prop_type = DocstringPatcher._get_param_type(spec, prop_def)
                            prop_desc = prop_def.get("description", "N/A")
                            details["request_body"]["properties"].append(
                                {"name": prop_name, "type": prop_type, "description": prop_desc}
                            )

                # --- Body Parameters ---
                resolved_body_params = []
                for param_def in body_level_params:
                    if "$ref" in param_def:
                        resolved_body_params.append(
                            DocstringPatcher._resolve_ref(spec, param_def["$ref"])
                        )
                    else:
                        resolved_body_params.append(param_def)

                for p in resolved_body_params:
                    details["request_body"]["parameters"].append(
                        {
                            "name": p.get("name"),
                            "in": p.get("in"),
                            "required": p.get("required", False),
                            "description": p.get("description", "N/A"),
                            "type": DocstringPatcher._get_param_type(spec, p.get("schema")),
                        }
                    )

            # --- Responses ---
            responses_def = operation.get("responses", {})
            for status_code, resp_def in responses_def.items():
                resolved_resp = {}
                if "$ref" in resp_def:
                    resolved_resp = DocstringPatcher._resolve_ref(spec, resp_def["$ref"])
                else:
                    resolved_resp = resp_def

                description = resolved_resp.get("description", "N/A")
                resp_type = "N/A"
                content = resolved_resp.get("content", {})
                media_type = next(iter(content.values()), None)

                if media_type and "schema" in media_type:
                    schema = media_type["schema"]
                    resp_type = DocstringPatcher._get_param_type(spec, schema)

                details["responses"].append(
                    {
                        "status_code": status_code,
                        "description": description,
                        "type": resp_type,
                    }
                )

            return details
        except Exception as e:
            logging.warning(f"Error parsing spec for {method.upper()} {path}: {e}", exc_info=True)
            return details

    @staticmethod
    def _resolve_ref(spec: dict, ref: str):
        """Resolves a JSON schema $ref string."""
        if not spec or not ref.startswith("#/"):
            return {}
        parts = ref.split("/")[1:]
        current_obj = spec
        for part in parts:
            if isinstance(current_obj, list):
                try:
                    current_obj = current_obj[int(part)]
                except (IndexError, ValueError):
                    return {}
            elif isinstance(current_obj, dict):
                current_obj = current_obj.get(part)
            else:
                return {}
            if current_obj is None:
                return {}
        return current_obj

    @staticmethod
    def _get_param_type(spec: dict, schema: dict) -> str:
        """
        Gets the type name. Handles recursion and arrays.
        """
        if not schema:
            return "N/A"

        current_schema = schema
        ref_name = None

        while True:
            ref_string = current_schema.get("$ref") or current_schema.get("$ref:")

            if not ref_string:
                break

            ref_name = ref_string.split("/")[-1]

            resolved = DocstringPatcher._resolve_ref(spec, ref_string)

            if not resolved:
                return ref_name or "N/A"

            if "schema" in resolved:
                current_schema = resolved["schema"]
            else:
                current_schema = resolved

        schema_type = current_schema.get("type", "N/A")

        if schema_type == "array":
            items_schema = current_schema.get("items", {})
            items_type = DocstringPatcher._get_param_type(spec, items_schema)
            return f"array[{items_type}]"

        if schema_type == "object" and ref_name:
            return ref_name

        return schema_type

    def _generate_api_doc_string(self, spec: dict, path: str, method: str) -> str:
        """Creates the formatted API docstring section for ONE operation."""

        # Call static method
        details = self.get_operation_details(spec, path, method)

        lines = [f"--- Operation: {method.upper()} {path} ---"]

        lines.append(f"\n  Summary: {details.get('summary', 'N/A')}")
        lines.append(f"  Description: {details.get('description', 'N/A')}")
        lines.append(f"  External Doc: {details.get('external_doc', 'N/A')}")

        lines.append("\n  Query Parameters:")
        if not details["query_params"]:
            lines.append("    (No query parameters)")
        else:
            for param in details["query_params"]:
                lines.append(f"\n    **{param['name']}** ({param['type']})")
                lines.append(f"      Required:    {param['required']}")
                lines.append(f"      Description: {param['description']}")

        lines.append("\n  Request Body:")
        if not details["request_body"]:
            lines.append("    (No request body)")
        else:
            body = details["request_body"]
            lines.append(f"\n    **{body['type']}**")
            lines.append(f"      Required:    {body['required']}")
            lines.append(f"      Description: {body['description']}")

            if body.get("properties"):
                lines.append(f"      Properties:")
                for prop in body["properties"]:
                    lines.append(f"\n        **{prop['name']}** ({prop['type']})")
                    lines.append(f"          Description: {prop['description']}")

            if body.get("parameters"):
                lines.append(f"      Parameters (associated with this body):")
                for param in body["parameters"]:
                    param_in = param.get("in", "N/A")
                    lines.append(
                        f"\n        **{param['name']}** ({param['type']}) [in: {param_in}]"
                    )
                    lines.append(f"          Required:    {param['required']}")
                    lines.append(f"          Description: {param['description']}")

        lines.append("\n  Result Body (Responses):")
        if not details["responses"]:
            lines.append("    (No responses defined in spec)")
        else:
            for resp in details["responses"]:
                lines.append(f"\n    **{resp['status_code']}**: ({resp['type']})")
                lines.append(f"      Description: {resp['description']}")

        return "\n".join(lines)
