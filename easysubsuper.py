class EasySubSuper(type):
    """
    Metaclass whose class instances have an easy way of comparing sub/superclasses.

    The rich comparison operators only consider sub/superclasses as strict MRO concepts;
    any __subclasscheck__ is ignored and, consequently, ABC behaviour might be unexpected.
    """

    def __lt__(cls, other: type) -> bool:
        """Check if 'cls' is a proper subclass of 'other'."""
        return other in cls.__mro__[1:]

    def __le__(cls, other: type) -> bool:
        """Check if 'cls' is a subclass of 'other'."""
        return other in cls.__mro__

    def __gt__(cls, other: type) -> bool:
        """Check if 'cls' is a proper superclass of 'other'."""
        return cls in other.__mro__[1:]

    def __ge__(cls, other: type) -> bool:
        """Check if 'cls' is a superclass of 'other'."""
        return cls in other.__mro__


# ----- DRIVER CODE -----

class A(metaclass=EasySubSuper): pass
class B(A): pass
class C(A): pass
class D(A): pass
class E(B, C): pass
class F(C, D): pass
class G(E, F): pass


print(
    object > A,
    A > B,
    A > C,
    B > C,
    G < G,
    G <= G,
    G < E,
    D > F,
    C < object,
    F < E,
    F > E,
    sep="\n",
)
