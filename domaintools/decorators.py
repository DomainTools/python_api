import functools

from typing import List, Union

from domaintools.docstring_patcher import DocstringPatcher


def api_endpoint(spec_name: str, path: str, methods: Union[str, List[str]]):
    """
    Decorator to tag a method as an API endpoint.

    Args:
        spec_name: The key for the spec in api_instance.specs
        path: The API path (e.g., "/users")
        methods: A single method ("get") or list of methods (["get", "post"])
                 that this function handles.
    """

    def decorator(func):
        func._api_spec_name = spec_name
        func._api_path = path

        # Always store the methods as a list
        if isinstance(methods, str):
            func._api_methods = [methods]
        else:
            func._api_methods = methods

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        # Copy all tags to the wrapper
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
