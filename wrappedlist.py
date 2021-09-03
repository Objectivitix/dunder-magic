from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Optional, Union

Key = Union[int, slice]


class WrappedList(list):
    """Class for lists who wrap back to the start when an index is out of range."""

    def __init__(self, *items, iterable: Optional[Iterable] = None) -> None:
        """Construct a WrappedList instance."""
        super_init = super().__init__

        if items and iterable is not None:  # both specified
            raise ValueError("cannot specify items and iterable at the same time")
        elif not items and iterable is not None:  # iterable specified
            super_init(iterable)
        elif items and iterable is None:  # items specified
            super_init(items)
        else:  # nothing specified, default a tuple
            super_init(())

    def __repr__(self) -> str:
        """Return the developer representation."""
        return f"{WrappedList.__qualname__}({super().__repr__()[1:-1]})"

    @staticmethod
    def _wrap_int(key: int, length: int) -> int:
        """Do a wrap-around on an integer key with modulus."""
        return key % length - (0, length)[key < 0]

    @staticmethod
    def _wrap_slice(key: slice, length: int) -> slice:
        """Do a wrap-around on a slice key with modulus."""
        return slice(
            *(
                WrappedList._wrap_int(attr, length)
                for attr in (key.start, key.stop)
            ),
            key.step,
        )

    @staticmethod
    def _wrap_both(key: Key, length: int) -> Key:
        """Wrap the key using an appropriate function based on its type (convenience func)."""
        func = (
            WrappedList._wrap_int
            if isinstance(key, int)
            else WrappedList._wrap_slice
        )

        return func(key, length)

    def __getitem__(self, key: Key) -> Any:
        """Get item from 'key'."""
        super_getitem = super().__getitem__
        length = len(self)

        if isinstance(key, int):
            return super_getitem(self._wrap_int(key, length))
        elif isinstance(key, slice):
            return WrappedList(
                iterable=super_getitem(
                    self._wrap_slice(key, length)
                ),
            )
        else:  # invalid type
            raise TypeError("key must be of type int or slice")

    def __setitem__(self, key: Key, value: Any) -> None:
        """Set a new value to self[key]."""
        super().__setitem__(self._wrap_both(key, len(self)), value)

    def __delitem__(self, key: Key) -> None:
        """Delete a value with index 'key'."""
        super().__delitem__(self._wrap_both(key, len(self)))

    def __add__(self, other: Union[WrappedList, list]) -> WrappedList:
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, (WrappedList, list)):
            return WrappedList(iterable=super().__add__(other))
        else:
            return NotImplemented

    def __radd__(self, other: list) -> list:
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, list):
            return other + list(self)
        else:
            return NotImplemented

    def __iadd__(self, other: Iterable) -> WrappedList:
        """Boilerplate to fulfill arithmetic."""
        try:
            self.extend(other)
        except TypeError:
            return NotImplemented
        else:
            return self

    def __mul__(self, other: int) -> WrappedList:
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, int):
            return WrappedList(iterable=super().__mul__(other))
        else:
            return NotImplemented

    def __rmul__(self, other: int) -> WrappedList:
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, int):
            return self * other
        else:
            return NotImplemented

    def __imul__(self, other: int) -> WrappedList:
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, int):
            super().__imul__(other)
            return self
        else:
            return NotImplemented


# ----- DRIVER CODE -----

a = WrappedList(0, 1, 2, 3, 4)
print(a[-6])                         # output: 4
a[917] = 5; print(a)                 # output: WrappedList(0, 1, 5, 3, 4)
a *= 2; print(a)                     # output: WrappedList(0, 1, 5, 3, 4, 0, 1, 5, 3, 4)
print(list("abc") + a)               # output: ['a', 'b', 'c', 0, 1, 5, 3, 4, 0, 1, 5, 3, 4]

b = WrappedList(iterable="abcdefgh")
print(b[-1:-13:-1])                  # output: WrappedList('h', 'g', 'f', 'e')
b[8:14:2] = "o", "p", "q"; print(b)  # output: WrappedList('o', 'b', 'p', 'd', 'q', 'f', 'g', 'h')
del b[123:765]; print(b)             # output: WrappedList('o', 'b', 'p', 'f', 'g', 'h')
