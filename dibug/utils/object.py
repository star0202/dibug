from inspect import getmembers, isbuiltin, ismethod
from typing import Any, Iterable


def inspect(obj: Any, indent: int) -> list[str]:
    lines = [" " * indent + f"{type(obj)} ["]

    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        for item in obj:
            lines.extend(inspect(item, indent + 2))

    ignore = getmembers(obj, ismethod) + getmembers(obj, isbuiltin)

    members = [
        member
        for member in getmembers(obj)
        if member not in ignore and not member[0].startswith("_")
    ]

    for member in members:
        lines.append(" " * (indent + 2) + str(member))

    if not members and not isinstance(obj, Iterable) or isinstance(obj, (str, bytes)):
        lines[-1] += "]"
    else:
        lines.append(" " * indent + "]")

    return lines
