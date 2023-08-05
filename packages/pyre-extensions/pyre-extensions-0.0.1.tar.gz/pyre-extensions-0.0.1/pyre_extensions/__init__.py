def CallableParametersVariable(name):
    """This kind of type variable captures callable parameter specifications
    instead of types, allowing the typing of decorators which transform the 
    return type of the given callable.  For example:
        from typing import TypeVar, Callable, List
        from typing_extensions import CallableParametersVariable
        Tparams = CallableParametersVariable("Tparams")
        Treturn = TypeVar("Treturn")
        def unwrap(
            f: Callable[Tparams, List[Treturn],
        ) -> Callable[Tparams, Treturn]: ...
        @unwrap
        def foo(x: int, y: str, z: bool = False) -> List[int]:
            return [1, 2, 3]
    decorates foo into a callable that returns int, but still has the same 
    parameters, including their names and whether they are required.
    
    The empty list is required for backwards compatibility with the runtime 
    implementation for callables, which requires the first argument to be 
    a list of types
    """
    return []
