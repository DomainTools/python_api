import functools

from typing import List, Union

from domaintools.docstring_patcher import DocstringPatcher
from domaintools.request_validator import RequestValidator


def api_endpoint(spec_name: str, path: str, methods: Union[str, List[str]]):
    """
    Decorator to tag a method as an API endpoint AND validate inputs.

    Args:
        spec_name: The key for the spec in api_instance.specs
        path: The API path (e.g., "/users")
        methods: A single method ("get") or list of methods (["get", "post"])
    """

    def decorator(func):
        func._api_spec_name = spec_name
        func._api_path = path

        # Normalize methods to a list
        normalized_methods = [methods] if isinstance(methods, str) else methods
        func._api_methods = normalized_methods

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Retrieve the Spec from the instance
            # We assume 'self' has a .specs attribute (like DocstringPatcher expects)
            spec = getattr(self, "specs", {}).get(spec_name)

            if spec:
                # Determine which HTTP method is currently being executed.
                # If the function allows dynamic methods (e.g. method="POST"), use that.
                # Otherwise, default to the first method defined in the decorator.
                current_method = kwargs.get("method", normalized_methods[0])

                # Run Validation
                # This will raise a ValueError and stop execution if validation fails.
                try:
                    RequestValidator.validate(
                        spec=spec,
                        path=path,
                        method=current_method,
                        parameters=kwargs,
                    )
                except ValueError as e:
                    # Optional: Log the error or re-raise custom exception
                    print(f"[Validation Error] {e}")
                    raise e

            # 5. Proceed with the original function call
            return func(*args, **kwargs)

        # Copy tags to wrapper for the DocstringPatcher to find
        wrapper._api_spec_name = func._api_spec_name
        wrapper._api_path = func._api_path
        wrapper._api_methods = func._api_methods

        return wrapper

    return decorator


def auto_patch_docstrings(cls):
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        try:
            # We instantiate our patcher and run it
            patcher = DocstringPatcher()
            patcher.patch(self)
        except Exception as e:
            print(f"Auto-patching failed: {e}")

    cls.__init__ = new_init

    return cls
