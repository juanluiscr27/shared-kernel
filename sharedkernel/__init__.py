import ast
import os
from typing import Optional, List, Tuple

from . import api, application, domain, infrastructure

__all__ = [
    "api",
    "application",
    "domain",
    "infrastructure",
    "gethandledtypes"
]


class HandlerVisitor(ast.NodeVisitor):

    def __init__(self, class_name: str):
        self._class_name = class_name
        self._match: Optional[ast.AST] = None

    @property
    def matched_node(self):
        return self._match

    def visit_ClassDef(self, node: ast.AST):
        match node:
            case ast.ClassDef(name=self._class_name):
                self._match = node

        ast.NodeVisitor.generic_visit(self, node)


class FunctionVisitor(ast.NodeVisitor):

    def __init__(self):
        self._matches: List[str] = []

    @property
    def matches(self):
        return tuple(dict.fromkeys(self._matches))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        match node:
            case ast.FunctionDef(
                decorator_list=[
                    ast.Attribute(value=ast.Name(id="apply"), attr="register")
                ]
            ):
                _ = 0
                arguments = node.args.args
                annotations = [arg.annotation for arg in arguments if arg != "self"]
                # noinspection PyUnresolvedReferences
                handled_type = [annotation.id for annotation in annotations if annotation is not None]

                self._matches.extend(handled_type)

        ast.NodeVisitor.generic_visit(self, node)


def _get_abs_path(module_name: str):
    rel_path = "/".join(module_name.split("."))
    file_path = f"{rel_path}.py"

    return os.path.abspath(file_path)


def zip_type_names(module_name: str, types: Tuple[str, ...]):
    return [f"{module_name}.{type_name}" for type_name in types]


def gethandledtypes(handler):
    try:
        module_name = handler.__module__
        class_name = handler.__name__
        module_path = _get_abs_path(module_name)

        with open(module_path, encoding="UTF-8") as file:
            code = file.read()

        module = ast.parse(code)

        handler_visitor = HandlerVisitor(class_name)
        handler_visitor.visit(module)

        handler_node = handler_visitor.matched_node

        function_visitor = FunctionVisitor()

        function_visitor.visit(handler_node)

        handled_types = function_visitor.matches

        return zip_type_names(module_name, handled_types)

    except Exception as e:
        print(e)
        return []
