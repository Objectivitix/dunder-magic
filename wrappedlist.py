from collections.abc import Iterable
from typing import Any, Optional, Union


class WrappedList(list):
    """Class for lists who wrap back to the start when an index is out of range."""

    def __init__(self, *items, iterable: Optional[Iterable] = None) -> None:
        """Construct a WrappedList instance."""
        s = super().__init__

        if items and iterable is not None:  # both specified
            raise ValueError("cannot specify items and iterable at the same time")
        elif not items and iterable is not None:  # iterable specified
            s(iterable)
        elif items and iterable is None:  # items specified
            s(items)
        else:  # nothing specified, default a tuple
            s(())

    def __repr__(self) -> str:
        """Return the developer representation."""
        return f"{WrappedList.__qualname__}({super().__repr__()[1:-1]})"

    @staticmethod
    def _wrap(key: int, length: int) -> int:
        """Do a wrap-around with modulus."""
        return key % length - (0, length)[key < 0]

    def __getitem__(self, key: Union[int, slice]) -> Any:
        """Get item from 'key'."""
        s = super().__getitem__
        l = len(self)

        if isinstance(key, slice):  # let list do the work with slices
            return WrappedList(iterable=s(key))
        elif isinstance(key, int):  # if it's an integer, use our function
            return s(self._wrap(key, l))
        else:  # invalid type
            raise TypeError("key must be of type int or slice")

    def __setitem__(self, key: int, value: Any) -> None:
        """Set a new value to self[key]."""
        super().__setitem__(self._wrap(key, len(self)), value)

    def __delitem__(self, key: int) -> None:
        """Delete a value with index 'key'."""
        super().__delitem__(self._wrap(key, len(self)))

    def __add__(self, other: Union["WrappedList", list]) -> "WrappedList":
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

    def __iadd__(self, other: Iterable) -> "WrappedList":
        """Boilerplate to fulfill arithmetic."""
        try:
            self.extend(other)
        except TypeError:
            return NotImplemented
        else:
            return self

    def __mul__(self, other: int) -> "WrappedList":
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, int):
            return WrappedList(iterable=super().__mul__(other))
        else:
            return NotImplemented

    def __rmul__(self, other: int) -> "WrappedList":
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, int):
            return self * other
        else:
            return NotImplemented

    def __imul__(self, other: int) -> "WrappedList":
        """Boilerplate to fulfill arithmetic."""
        if isinstance(other, int):
            super().__imul__(other)
            return self
        else:
            return NotImplemented


a = WrappedList(0, 1, 2, 3, 4)

print(a[-6])
a[917] = 5; print(a)
a *= 2; print(a)
a += iter("abc"); print(a)
