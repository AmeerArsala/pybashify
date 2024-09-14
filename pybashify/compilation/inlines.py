import ast
import importlib
import inspect
import os
import sys
from types import ModuleType

import astor


class RecursiveImportInliner(ast.NodeTransformer):
    def __init__(self):
        self.processed_modules = set()

    def visit_Import(self, node):
        new_nodes = []
        for alias in node.names:
            new_nodes.extend(self.inline_module(alias.name))
        return new_nodes

    def visit_ImportFrom(self, node):
        module = node.module
        new_nodes = []
        if node.level > 0:  # Relative import
            package = self.get_package_from_path(sys.modules['__main__'].__file__, node.level)
            if module:
                module = f"{package}.{module}"
            else:
                module = package
        for alias in node.names:
            if alias.name == '*':
                new_nodes.extend(self.inline_module(module))
            else:
                new_nodes.extend(self.inline_attribute(module, alias.name))
        return new_nodes

    def inline_module(self, module_name):
        if module_name in self.processed_modules:
            return []
        self.processed_modules.add(module_name)

        if module_name in sys.stdlib_module_names:
            return [f"import {module_name}"]

        try:
            module = importlib.import_module(module_name)

            if hasattr(module, '__file__') and module.__file__:
                source = inspect.getsource(module)
                module_ast = ast.parse(source)
                self.generic_visit(module_ast)  # Recursively inline imports in this module
                return module_ast.body
            else:
                return [f"import {module_name}"]
        except:  # Exception as e
            return [f"import {module_name}"]
            # return [ast.Expr(ast.Str(f"# Error inlining module {module_name}: {str(e)}"))]

    def inline_attribute(self, module_name, attr_name):
        module = importlib.import_module(module_name)
        attr = getattr(module, attr_name)
        if inspect.ismodule(attr):
            return self.inline_module(attr.__name__)
        elif isinstance(attr, ModuleType):
            return self.inline_module(attr.__name__)
        else:
            try:
                source = inspect.getsource(attr)
                attr_ast = ast.parse(source)
                self.generic_visit(attr_ast)  # Recursively inline imports in this attribute
                return attr_ast.body
            except Exception as e:
                return [
                    ast.Expr(
                        ast.Str(
                            f"# Error inlining attribute {attr_name} from {module_name}: {str(e)}"
                        )
                    )
                ]

    @staticmethod
    def get_package_from_path(path, level):
        dir_path = os.path.dirname(path)
        for _ in range(level - 1):
            dir_path = os.path.dirname(dir_path)
        return os.path.basename(dir_path)


def inline_imports_from_source(source: str) -> str:
    tree = ast.parse(source)
    transformer = RecursiveImportInliner()
    new_tree = transformer.visit(tree)

    return astor.to_source(new_tree)


def inline_imports(module_name: str) -> str:
    module = importlib.import_module(module_name)
    source = inspect.getsource(module)

    return inline_imports_from_source(source)
