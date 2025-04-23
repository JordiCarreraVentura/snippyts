from collections.abc import Iterable
from doctest import testmod
from typing import Iterable as IterableType, Union

import numpy as np
from statistics import quantiles

from .__init__ import (
    UnsupportedInputShapeError,
    is_all_numerical_immutable,
    smart_cast_number,
    tryline
)


class KBinsEncoder:
    """
    Discretizes the data into `n_bins` using scikit-learn's `KBinsDiscretizer` class, and then replaces every input value with the value at the bin-th quantile, ensuring that the output vector
    - only has `n_bins` unique element but
    - has the same dimensionality as the original input vector.
    
    Parameters
    ----------
    n_bins : int, optional
        The number of bins into which the data will be grouped. Defaults to 10.
    
    Attributes
    ----------
    quantiles : np.array[int | float]
        The computed quantiles after fitting the data.

    discretizer : KBinsDiscretizer object
        The KBinsDiscretizer object for transforming the data.

    Raises
    ------
    UnsupportedInputShapeError
        Raised when trying to feed the `fit` a non-iterable object or an iterable
        containing objects of types other than `float` or `int`.

    Examples
    --------
    >>> kbe = KBinsEncoder(n_bins=3)
    >>> vals = [1, 1, 1, 1, 1.0, 1.0, 2.33, 2, 2, 2, 3, 3, 3, 4, 4, 10, 100]
    >>> kbe.fit(vals)

    >>> kbe = KBinsEncoder(n_bins=3)
    >>> try:
    ...   vals = [1, 1, 1, None, 1.0, 1.0, 2.33, 2, 'hello', 'world', 3, 3, 12]
    ...   kbe.fit(vals)
    ... except ValueError:
    ...   assert True

    >>> kbe = KBinsEncoder(n_bins=3)
    >>> vals = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 10, 100]
    >>> kbe.fit(vals)
    
    >>> kbe.quantiles
    [1.3333, 3, 100.0]

    >>> kbe.transform([1, 3, 7])
    [1.3333, 3, 3]
    
    >>> kbe.transform([1, 3, 88])
    [1.3333, 3, 100.0]

    >>> kbe.transform([1000, 100000, 0, 1, 1, 1, 0])
    [100.0, 100.0, 1.3333, 1.3333, 1.3333, 1.3333, 1.3333]

    >>> kbe.transform([1000, 100000, 0, 1, 2, 2, 0])
    [100.0, 100.0, 1.3333, 1.3333, 1.3333, 1.3333, 1.3333]
    
    """
    
    def __init__(self, n_bins: int = 10, rounding: int = 4) -> None:
        self.n_bins = n_bins
        self.rounding = rounding
        self.quantiles: np.array[int | float] = []


    def fit(self, x: IterableType[Union[float, int]]) -> None:
        """
        Fits the encoder by
        - calculating the quantiles and then
        - fitting the discretizer.

        Parameters
        ----------
        x : IterableType[Union[float, int]]
            The data to fit.
        
        Returns
        -------
        None.
        
        Raises
        ------
        UnsupportedInputShapeError
            Raised when trying to feed the `fit` a non-iterable object or an iterable
            containing objects of types other than `float` or `int`.

        """
        all_numerical_immutable = tryline(is_all_numerical_immutable, UnsupportedInputShapeError, x)
        if not all_numerical_immutable:
            raise UnsupportedInputShapeError(type(x), x)
        x = np.array(x).reshape(-1, 1)
        if not x.astype(float).all():
            raise TypeError(type(x[0]), x[0])
        
        quantile = (1 / self.n_bins) * 100
        
        self.quantiles = []
        while len(self.quantiles) < self.n_bins:
            bin = np.percentile(x, quantile * (1 + len(self.quantiles)))
            self.quantiles.append(round(smart_cast_number(bin), self.rounding))
        self.quantiles = self.quantiles


    def transform(
        self, 
        x: IterableType[Union[float, int]]
    ) -> IterableType[Union[float, int]]:
        """
        Replaces every input value with the value at the bin-th quantile, ensuring the output vector only has `n_bins` unique elements, but the same dimensionality as the original input vector.

        Parameters
        ----------
        x : IterableType[Union[float, int]]
            The data to transform.

        Returns
        -------
        IterableType[Union[float, int]]
            The transformed data.
        
        Example
        -------
        >>> kbe = KBinsEncoder(n_bins=3)
        >>> vals = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 10, 100]
        >>> kbe.fit(vals)
        >>> kbe.transform([1, 2, 3])
        [1.3333, 1.3333, 3]
        
        """
        return type(x)(map(self._get_bin, x))


    def _get_bin(self, val: Union[float, int]) -> Union[float, int]:
        arg, argval = None, 10**10
        for quantile in self.quantiles:
            distance = abs(val - quantile)
            if distance < argval:
                arg = quantile
                argval = distance
        return arg


    def fit_transform(
        self, 
        x: IterableType[Union[float, int]]
    ) -> IterableType[Union[float, int]]:
        """
        Fit the data and then transform it.

        Parameters
        ----------
        x : IterableType[Union[float, int]]
            The data to fit and transform.

        Returns
        -------
        IterableType[Union[float, int]]
            The transformed data.

        Example
        -------
        >>> kbe = KBinsEncoder(n_bins=3)
        >>> vals = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 10, 100]
        >>> transformed = kbe.fit_transform(vals)
        >>> assert transformed == [
        ...   1.3333, 1.3333, 1.3333, 1.3333, 1.3333, 1.3333, 
        ...   1.3333, 1.3333, 1.3333, 1.3333, 
        ...   3, 3, 3, 3, 3, 3, 100.0
        ... ]

        """
        self.fit(x)
        return self.transform(x)


if __name__ == '__main__':
    testmod()

    # print(-1, is_all_numerical_immutable([1, 1, 1, None, 1.0, 1.0, 2.33, 2, 'hello', 'world', 3, 3, 12]))
    # print(0, is_all_numerical_immutable([1, 2, 3]))
    # print(1, is_all_numerical_immutable([1, 2.5, 3]))
    # print(2, is_all_numerical_immutable((1+2j, 3.0)))
    # print(3, is_all_numerical_immutable((333.3, 0.0393, 0.1887)))
    # print(4, is_all_numerical_immutable([1, "2", 3]))
    # print(5, is_all_numerical_immutable(["11", "2", "3"]))
    # print(6, is_all_numerical_immutable("123"))
    # print(7, is_all_numerical_immutable(123))

    # kbe = KBinsEncoder()