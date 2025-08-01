from typing import Any, Callable, Iterable

    
class UnsupportedInputShapeError(ValueError):
    pass



def is_all_numerical_immutable(iterable):
    """
    Check if all elements in an iterable are immutable numerical types (int, float, complex).

    Parameters
    ----------
        iterable: Iterable[complex | float | int]
          An iterable of elements to check.

    Returns
    -------
        bool:
          True if all elements are instances of immutable numerical types, False otherwise.

    Raises
    ------
        UnsupportedInputShapeError: If the input is not an iterable.

    Examples
    --------
    >>> is_all_numerical_immutable([1, 2.5, 3])
    True
    >>> is_all_numerical_immutable((1+2j, 3.0))
    True
    >>> is_all_numerical_immutable((333.3, 0.0393, 0.1887))
    True
    >>> is_all_numerical_immutable([1, "2", 3])
    False
    >>> is_all_numerical_immutable(["11", "2", "3"])
    False
    >>> is_all_numerical_immutable("123")
    False
    >>> is_all_numerical_immutable(123)
    Traceback (most recent call last):
    ...
    UnsupportedInputShapeError: Input must be an iterable.

    """
    if not isinstance(iterable, Iterable):
        raise UnsupportedInputShapeError("Input must be an iterable.")
    
    immutable_numerics = (int, float, complex)
    
    return all(isinstance(item, immutable_numerics) for item in iterable)


def smart_cast_number(x: float | int) -> float | int:
    """
    Cast a numeric value to an integer if it is numerically whole; otherwise, return as float.

    Parameters
    ----------
        x: float | int
          A numeric value to be cast intelligently.

    Returns
    -------
        float | int:
          The input value cast to an integer if it has no fractional part, otherwise returned as a float.

    Examples
    --------
    >>> smart_cast_number(1)
    1
    >>> smart_cast_number(1.0)
    1
    >>> smart_cast_number(1.333)
    1.333
    """
    if (
        isinstance(x, int)
        or isinstance(x, float) and int(x) == x
    ):
        return int(x)
    return float(x)


def tryline(_call: Callable, exception: Exception, *args, **kwargs) -> Any:
    """
    Wraps a try-raise block into a single statement. It is intended to
    flatten try-catch
    
    It attempts to call the specified Python-callable object with the provided 
    arguments and keyword arguments.
    
    If the call is successful, it silently returns the output of the call.
    If it fails, it raises an exception of the type provided as the second
    argument.
    
    Parameters
    ----------
    _call: object
        Any Python object that can be called on the specified arguments.
    
    exception: Exception
        The exception that must be raised if the call fails.
    
    *args: List[Any]
        Its standard meaning.
        
    **kwargs: Dict[str, Any]
        Its standard meaning.
    
    Returns
    -------
    object:
        Whichever object is returned by the call to the callable object.
    
    Examples
    --------
    >>> class CustomError(Exception):
    ...   pass

    >>> assert tryline(sum, CustomError, [1, 1]) == 2
    >>> tryline(
    ...   lambda x, y: x + "." + y,
    ...   CustomError,
    ...   'text',
    ...   'and more text'
    ... )
    'text.and more text'
    
    >>> try:
    ...   tryline(sum, CustomError, ['text', 1])
    ... except CustomError:
    ...   assert True
    
    >>> try:
    ...   tryline(lambda x, y: x + "." + y, CustomError, 'text', 1)
    ... except CustomError:
    ...   assert True
    """
    try:
        return _call(*args, **kwargs)
    except Exception:
        raise exception(args)