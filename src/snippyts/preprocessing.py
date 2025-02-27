from collections.abc import Iterable
from doctest import testmod
from typing import Iterable as IterableType, Union

import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from statistics import quantiles

from .__init__ import tryline


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

    Examples
    --------
    >>> kbe = KBinsEncoder(n_bins=3)
    >>> vals = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 10, 100]
    >>> kbe.fit(vals)
    
    >>> kbe.quantiles
    array([1. , 2. , 3.5])

    >>> kbe.transform([1, 3, 7])
    array([1. , 3.5, 3.5])
    
    >>> kbe.transform([1, 3, 88])
    array([1. , 3.5, 3.5])

    >>> kbe.transform([1000, 100000, 0, 1, 1, 1, 0])
    array([3.5, 3.5, 1. , 1. , 1. , 1. , 1. ])

    >>> kbe.transform([1000, 100000, 0, 1, 2, 2, 0])
    array([3.5, 3.5, 1. , 1. , 2. , 2. , 1. ])
    
    """
    
    def __init__(self, n_bins: int = 10) -> None:
        self.n_bins = n_bins
        self.quantiles: np.array[int | float] = []
        self.discretizer = KBinsDiscretizer(
            n_bins=self.n_bins,
            strategy='quantile',
            encode='ordinal'
        )

    def __getitem__(self, key: int) -> int | float:
        return self.quantiles[key]

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
        TypeError
            If the input is not an iterable, or if the array items cannot be cast as numeric values.
        """
        tryline(isinstance, TypeError, x, Iterable)
        x = np.array(x).reshape(-1, 1)
        if not x.astype(float).all():
            raise TypeError(type(x[0]), x[0])
        self.quantiles = np.array([
            float(val) for val in quantiles(x[:, 0], n=self.n_bins + 1)
        ])
        self.discretizer.fit(x)

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
        array([1. , 2. , 3.5])
        
        """
        encoding = self.discretizer.transform(
            np.array(x).reshape(-1, 1)
        )[:, 0]
        return np.array([
            self[bin] for bin in encoding.astype(int)
        ]).reshape(-1, 1)[:, 0]

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
        >>> assert not(transformed.sum() - np.array([1. , 1. , 1. , 1. , 
        ...   1. , 1. , 2. , 2. , 2. , 2. , 3.5, 3.5, 3.5, 3.5, 3.5, 3.5,
        ...   3.5]).sum())

        """
        self.fit(x)
        return self.transform(x)


if __name__ == '__main__':
    testmod()
