from typing import Any, Callable, NoReturn, Optional, Union


def tuplefy(obj: Any) -> tuple:
    return obj if isinstance(obj, tuple) else (obj,)


class SquareMethod:
    """
    Class implementing method support for SquareFunction.

    To expand on this, class and static method equivalents can also be easily created.
    """

    def __init__(self, func: "SquareFunction", instance: Any) -> None:
        """Construct a SquareMethod instance bounded to obj."""
        self.__func__ = func
        self.__self__ = instance

    def __getitem__(self, poskwargs: Any) -> None:
        """
        Perform a method call with the bounded object prepended to inputted arguments.

        Call the __getitem__ of the underlying SquareFunction.
        """
        self.__func__.__getitem__((self.__self__,) + tuplefy(poskwargs))


class SquareFunction:
    """
    Class for functions who are invoked with square brackets instead of parentheses.

    Complete support for argument defaults, all types of arguments, and even instance methods!
    Normal slice objects whose 'start' attributes are anything other than strings are allowed.
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        """Construct a SquareFunction instance."""
        self.func = func

    @staticmethod
    def _is_valid_kwarg(arg: Any) -> bool:
        return isinstance(arg, slice) and isinstance(arg.start, str)

    @staticmethod
    def _verify(pkargs: tuple) -> None:
        """
        Verify if a tuple of args and kwargs is in the correct format.

        Raise SyntaxError when posargs and kwargs are mixed up.
        """
        riter = reversed(pkargs)
        posarg_start = False
        try:
            start_with_kwarg = SquareFunction._is_valid_kwarg(next(riter))
        except StopIteration:
            return

        for arg in riter:
            if SquareFunction._is_valid_kwarg(arg):
                if not (start_with_kwarg and not posarg_start):
                    raise SyntaxError(
                        "positional arguments were found "
                        "after keyword arguments"
                    )
            else:
                if not posarg_start:
                    posarg_start = True

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

    def __get__(
            self, instance: Any, owner: Optional[type] = None
    ) -> Union["SquareFunction", "SquareMethod"]:
        """Clone of standard function descriptor behaviour."""
        if instance is None:
            return self
        else:
            return SquareMethod(self, instance)


# ----- DRIVER CODE -----


@SquareFunction
def yeet(a=1, b=2, /, c=3, *, d=4, e=5):
    if isinstance(d, slice):
        print([0, 1, 2, 3, 4][d], end="   ")
    print(a, b, c, d, e)


class Yeet:
    @SquareFunction
    def foo(self, x, y):
        self.x, self.y = x, y


yeet[10]                              # output: 10 2 3 4 5
yeet[10, 20, "c":30, "d":40, "e":50]  # output: 10 20 30 40 50
yeet["d": slice(1, 4)]                # output: [1, 2, 3]   1 2 3 slice(1, 4, None) 5
# yeet[1:4, 3, "d":4, 2:5]            # error: posargs were found after kwargs

yeet_obj = Yeet()
yeet_obj.foo[5, "y":3]
print(yeet_obj.x, yeet_obj.y)         # output: 5 3
print(Yeet.foo)                       # output: <__main__.SquareFunction object at 0x000001ECC142A790>
