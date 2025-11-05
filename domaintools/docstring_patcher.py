import inspect
import functools
import textwrap


class DocstringPatcher:
    """
    Patches docstrings for methods decorated with @api_endpoint.
    """

    def patch(self, api_instance):
        method_names = []
        for attr_name in dir(api_instance):
            attr = getattr(api_instance, attr_name)
            # Look for the new decorator's tags
            if (
                inspect.ismethod(attr)
                and hasattr(attr, "_api_spec_name")
                and hasattr(attr, "_api_path")
            ):
                method_names.append(attr_name)

        for attr_name in method_names:
            original_method = getattr(api_instance, attr_name)
            original_function = original_method.__func__

            spec_name = original_function._api_spec_name
            path = original_function._api_path

            spec_to_use = api_instance.specs.get(spec_name)
            original_doc = inspect.getdoc(original_function) or ""

            all_doc_sections = []
            if spec_to_use:
                path_item = spec_to_use.get("paths", {}).get(path, {})

                # Loop over all HTTP methods defined for this path
                for http_method in ["get", "post", "put", "delete", "patch"]:
                    if http_method in path_item:
                        # Generate a doc section for this specific operation
                        api_doc = self._generate_api_doc_string(spec_to_use, path, http_method)
                        all_doc_sections.append(api_doc)

            if not all_doc_sections:
                all_doc_sections.append(
                    f"\n--- API Details Error ---"
                    f"\n  (Could not find any operations for path '{path}')"
                )

            # Combine the original doc with all operation docs
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

    def _generate_api_doc_string(self, spec: dict, path: str, method: str) -> str:
        """Creates the formatted API docstring section for ONE operation."""

        details = self._get_operation_details(spec, path, method)
        # Add a clear title for this specific method
        lines = [f"--- Operation: {method.upper()} {path} ---"]

        # Render Query Params
        lines.append(f"\n  Summary: {details.get('summary')}")
        lines.append(f"  Description: {details.get('description')}")
        lines.append(f"  External Doc: {details.get('external_doc')}")
        lines.append("\n  Query Parameters:")
        if not details["query_params"]:
            lines.append("    (No query parameters)")
        else:
            for param in details["query_params"]:
                lines.append(f"\n    **{param['name']}** ({param['type']})")
                lines.append(f"      Required:    {param['required']}")
                lines.append(f"      Description: {param['description']}")

        # Render Request Body
        lines.append("\n  Request Body:")
        if not details["request_body"]:
            lines.append("    (No request body)")
        else:
            body = details["request_body"]
            lines.append(f"\n    **{body['type']}**")
            lines.append(f"      Required:    {body['required']}")
            lines.append(f"      Description: {body['description']}")

        return "\n".join(lines)

    def _get_operation_details(self, spec: dict, path: str, method: str) -> dict:
        details = {"query_params": [], "request_body": None}
        if not spec:
            return details
        try:
            path_item = spec.get("paths", {}).get(path, {})
            operation = path_item.get(method.lower(), {})
            if not operation:
                return details
            all_param_defs = path_item.get("parameters", []) + operation.get("parameters", [])
            details["summary"] = operation.get("summary")
            details["description"] = operation.get("description")
            details["external_doc"] = operation.get("externalDocs", {}).get("url", "N/A")
            resolved_params = []
            for param_def in all_param_defs:
                if "$ref" in param_def:
                    resolved_params.append(self._resolve_ref(spec, param_def["$ref"]))
                else:
                    resolved_params.append(param_def)
            for p in [p for p in resolved_params if p.get("in") == "query"]:
                details["query_params"].append(
                    {
                        "name": p.get("name"),
                        "required": p.get("required", False),
                        "description": p.get("description", "N/A"),
                        "type": self._get_param_type(spec, p.get("schema")),
                    }
                )
            body_def = operation.get("requestBody")
            if body_def:
                if "$ref" in body_def:
                    body_def = self._resolve_ref(spec, body_def["$ref"])
                content = body_def.get("content", {})
                media_type = next(iter(content.values()), None)
                if media_type and "schema" in media_type:
                    schema = media_type["schema"]
                    schema_type = self._get_param_type(spec, schema)
                    if "$ref" in schema:
                        schema_type = schema["$ref"].split("/")[-1]
                    details["request_body"] = {
                        "required": body_def.get("required", False),
                        "description": body_def.get("description", "N/A"),
                        "type": schema_type,
                    }
            return details
        except Exception:
            return details

    def _resolve_ref(self, spec: dict, ref: str):
        if not spec or not ref.startswith("#/"):
            return {}
        parts = ref.split("/")[1:]
        current_obj = spec
        for part in parts:
            if not isinstance(current_obj, dict):
                return {}
            current_obj = current_obj.get(part)
            if current_obj is None:
                return {}
        return current_obj

    def _get_param_type(self, spec: dict, schema: dict) -> str:
        if not schema:
            return "N/A"
        schema_ref = schema.get("$ref")
        if schema_ref:
            resolved_schema = self._resolve_ref(spec, schema_ref)
            return resolved_schema.get("type", "N/A")
        return schema.get("type", "N/A")
