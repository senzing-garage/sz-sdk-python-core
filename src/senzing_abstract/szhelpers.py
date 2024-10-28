"""
TODO: g2helpers.py
"""

import inspect
from typing import Any

# -----------------------------------------------------------------------------
# Help
# -----------------------------------------------------------------------------


def construct_help(self: Any, method_name: str = "") -> str:
    """
    Construct help text.

    Args:
        method_name (str, optional): The name of the method. Defaults to "".

    Returns:
        str: if method_name is empty, a list of methods and their description is returned. If not empty, the description of the method is returned.
    """
    result: str = ""
    if method_name == "":
        class_name = self.__class__.__name__
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        for method in methods:
            method_name = method[0]
            if not method_name.startswith(("_")):
                method_comment = inspect.getdoc(getattr(self, method_name))
                if method_comment is not None:
                    lines = method_comment.split("\n")
                    method_overview = lines[0].strip()
                    result = f"{result}\n{method_name} - {method_overview}"
        result = f"{result}\n\nFor method details, use <{class_name}-variable>.help('method_name')"
    else:
        method_comment = inspect.getdoc(getattr(self, method_name))
        if method_comment is not None:
            lines = method_comment.split("\n")
            for line in lines:
                line_stripped = line.strip()
                if not line_stripped.startswith(("..", ":", "**")):
                    result = f"{result}\n{line}"
    return result
