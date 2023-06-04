"""
This type stub file was generated by pyright.
"""

import ast
from typing import Any, Optional, Union

_ = ...
_ = ...
_ASYNC_EVAL_CODE_TEMPLATE = ...
ASTWithBody = Union[ast.Module, ast.With, ast.AsyncWith]

class _AsyncNodeFound(Exception): ...
class _AsyncCodeVisitor(ast.NodeVisitor): ...

def is_async_code(code: str) -> bool: ...
def async_eval(
    code: str,
    _globals: Optional[dict[str, Any]] = ...,
    _locals: Optional[dict[str, Any]] = ...,
    *,
    filename: str = ...
) -> Any: ...

__all__ = ["async_eval", "is_async_code"]
