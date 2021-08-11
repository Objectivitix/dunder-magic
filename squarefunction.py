from typing import Any, Callable, NoReturn


class SquareFunction:
    """
    Class for functions who are invoked with square brackets instead of parentheses.

    Complete support for argument defaults, pos-only args, pos-or-kw args, and kwargs.
    Normal slice objects whose 'start' attributes are anything other than strings are allowed.
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        """Construct a SquareFunction instance."""
        self.func = func

    @staticmethod
    def _verify(pkargs: tuple) -> None:
        """
        Verify if a tuple of args and kwargs is in the correct format.

        Raise SyntaxError when posargs and kwargs are mixed up.
        """
        riter = reversed(pkargs)
        posarg_start = False
        try:
            start_with_kwarg = isinstance(next(riter), slice)
        except StopIteration:
            return

        for arg in riter:
            if isinstance(arg, slice):
                if (
                    not (start_with_kwarg and not posarg_start)
                    and isinstance(arg.start, str)
                ):
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
            if isinstance(arg, slice):
                if isinstance(arg.start, str):
                    kwargs[arg.start] = arg.stop
                else:
                    posargs.append(arg)
            else:
                posargs.append(arg)

        return posargs, kwargs

    def __getitem__(self, args_and_kwargs: Any) -> None:
        """Invoke the underlying function when subscription is performed."""
        ak = args_and_kwargs
        pkargs: tuple = ak if isinstance(ak, tuple) else (ak,)

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


@SquareFunction
def yeet(a=1, b=2, /, c=3, *, d=4, e=5):
    print([0, 1, 2, 3, 4][a])
    print(a, b, c, d, e)


yeet[1:4, (50,), "e":7]
