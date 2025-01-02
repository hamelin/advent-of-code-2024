import marimo as mo
from pathlib import Path
from typing import Any, Callable, TypeVar


T = TypeVar("T")


def input_editor(num: int) -> mo.Html:
    path_input = Path("inputs") / f"{num:02d}.txt"
    value_input = (
        path_input.read_text(encoding="utf-8")
        if path_input.is_file()
        else "(No input yet)"
    )

    def on_change(value_new: str) -> None:
        path_input.write_text(value_new, encoding="utf-8")

    return mo.ui.code_editor(
        value=value_input,
        language="",
        on_change=on_change
    )


Method = Callable[[T, ...], Any]


def add_method(cls: T) -> Callable[[Method[T]], Method[T]]:
    def _add_method(method: Method[T]) -> Method[T]:
        setattr(cls, method.__name__, method)
        return method

    return _add_method
