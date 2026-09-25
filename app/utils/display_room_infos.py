from typing import Callable, Any, TypeVar

T = TypeVar('T')

def display_room_infos(items: list[T], sort_key: Callable[[T], Any], formatter: Callable[[int, T], str], title: str | None = None) -> None:
    if len(items) == 0:
        return

    if title is not None:
        print(f"\n{title}: ")

    sorted_items = sorted(items, key=sort_key)

    for i, item in enumerate(sorted_items):
        print(formatter(i, item))