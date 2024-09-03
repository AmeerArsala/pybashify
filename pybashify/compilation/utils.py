import importlib
import inspect


def get_module_code(module_name: str) -> str:
    """
    Gets the code of the module
    module_name - Example: `my.python.module`; it's just the Python import syntax
    """
    
    module = importlib.import_module(module_name)
    source_code: str = inspect.getsource(module)

    return source_code
