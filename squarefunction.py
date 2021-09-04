from __future__ import annotations

from typing import Any, Callable, NoReturn, Optional, Union

GenericFunc = Callable[..., Any]


def tuplefy(obj: Any) -> tuple:
    return obj if isinstance(obj, tuple) else (obj,)


class SquareMethod:
    """
    Class implementing method support for SquareFunction.

    To expand on this, class and static method equivalents can also be easily created.
    """

    def __init__(self, func: SquareFunction, instance: Any, qualname: str) -> None:
        """Construct a SquareMethod instance bounded to an object."""
        self.__func__ = func
        self.__self__ = instance
        self.__qualname__ = qualname

    def __getitem__(self, poskwargs: Any) -> None:
        """
        Perform a method call with the bounded object prepended to inputted arguments.

        Call the __getitem__ of the underlying SquareFunction.
        """
        self.__func__.__getitem__((self.__self__,) + tuplefy(poskwargs))

    def __repr__(self) -> str:
        """Return the standard developer representation of a method."""
        return f"<bounded SquareMethod {self.__qualname__} of {self.__self__}>"


class SquareFunction:
    """
    Class for functions who are invoked with square brackets instead of parentheses.

    Complete support for argument defaults, all types of arguments, and even instance methods!
    Normal slice objects whose 'start' attributes are anything other than strings are allowed.
    """

    def __init__(self, func: GenericFunc, no_verify) -> None:
        """Construct a SquareFunction instance."""
        self.func = func
        self.no_verify = no_verify

    @staticmethod
    def _is_valid_kwarg(arg: Any) -> bool:
        """
        Check if an argument is a valid kwarg.

        (i.e. if it's a slice and if it has a string as its start attribute)
        """
        return isinstance(arg, slice) and isinstance(arg.start, str)

    @staticmethod
    def _verify(pkargs: tuple) -> None:
        """
        Verify if a tuple of args and kwargs is in the correct format.

        Raise SyntaxError when posargs and kwargs are mixed up.
        """
        riter = reversed(pkargs)
        posargs_starts = False
        kwargs_keys = []
        try:
            first = next(riter)
            if SquareFunction._is_valid_kwarg(first):
                start_with_kwarg = True
                kwargs_keys.append(first.start)
            else:
                start_with_kwarg = False
        except StopIteration:
            return

        for arg in riter:
            if SquareFunction._is_valid_kwarg(arg):
                if not (start_with_kwarg and not posargs_starts):
                    raise SyntaxError(
                        "positional arguments were found "
                        "after keyword arguments"
                    )

                key = arg.start
                if key in kwargs_keys:
                    raise SyntaxError(f"keyword argument repeated: {key}")
                kwargs_keys.append(key)
            else:
                if not posargs_starts:
                    posargs_starts = True

    @staticmethod
    def _split(pkargs: tuple) -> tuple[list[Any], dict[str, Any]]:
        """Split a tuple of args and kwargs into a list of args and a dict of kwargs."""
        posargs, kwargs = [], {}
        for arg in pkargs:
            if SquareFunction._is_valid_kwarg(arg):
                kwargs[arg.start] = arg.stop
            else:
                posargs.append(arg)

        return posargs, kwargs

    def __getitem__(self, poskwargs: Any) -> None:
        """Invoke the underlying function when subscription is performed."""
        pkargs = tuplefy(poskwargs)

        if not self.no_verify:
            self._verify(pkargs)
        posargs, kwargs = self._split(pkargs)
        self.func(*posargs, **kwargs)

    def __call__(self, *args, **kwargs) -> NoReturn:
        """
        Inform the user that this class of functions uses square brackets syntax.

        Raise SyntaxError.
        """
        raise SyntaxError(
            "function calling with parentheses is utterly horrid. Join us on the "
            "journey to enlightenment, where we use square brackets [] instead!"
        )

    def __set_name__(self, owner: Optional[type], name: str) -> None:
        """Set the qualified name of the SquareFunction object when in a class."""
        self.cls_qualname = f"{owner.__qualname__}.{name}"

    def __get__(
            self, instance: Any, owner: Optional[type] = None
    ) -> Union[SquareFunction, SquareMethod]:
        """Clone of standard function descriptor behaviour."""
        if instance is None:
            return self
        else:
            return SquareMethod(self, instance, self.cls_qualname)


def squarefunction(
        function: Optional[GenericFunc] = None,
        *, no_verify: bool = False,
) -> Union[SquareFunction, Callable[[GenericFunc], SquareFunction]]:
    """Decorate a function to become a SquareFunction instead."""
    def decorator(func):
        return SquareFunction(func, no_verify)

    if function is not None:  # if deco is invoked in the "normal" way
        return decorator(function)

    return decorator


# ----- DRIVER CODE -----


@squarefunction
def yeet(a=1, b=2, /, c=3, *, d=4, e=5):
    if isinstance(d, slice):
        print([0, 1, 2, 3, 4][d], end="   ")
    print(a, b, c, d, e)


class Yeet:
    @squarefunction
    def foo(self, x, y):
        self.x, self.y = x, y


yeet[10]                              # output: 10 2 3 4 5
yeet[10, 20, "c":30, "d":40, "e":50]  # output: 10 20 30 40 50
yeet["d": slice(1, 4)]                # output: [1, 2, 3]   1 2 3 slice(1, 4, None) 5
# yeet[1:4, 3, "d":4, 2:5]            # error: posargs were found after kwargs
# yeet[1, 2, 3, "d":4, "d":5, "e":6]  # error: keyword argument repeated: d

yeet_obj = Yeet()
yeet_obj.foo[5, "y":3]
print(yeet_obj.x, yeet_obj.y)         # output: 5 3
print(Yeet.foo)                       # output: <__main__.SquareFunction object at 0x000001ECC142A790>
