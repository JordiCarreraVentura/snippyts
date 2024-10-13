from functools import wraps
import json

from flashtext2 import KeywordProcessor

try:
    from cfuzzyset import cFuzzySet as FuzzySet
except ImportError:
    from fuzzyset import FuzzySet

from typing import Any, List, Tuple, Union



class AttemptedToAddTupleToFuzzyVocabulary(AttributeError):
    pass

class NestedObjectsNotSupportedError(ValueError):
    pass

class OperationNotYetSupportedForFuzzyVocabulary(NotImplementedError):
    pass




def reject_nested_input(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):

        if args \
        and isinstance(args[0], list) \
        and isinstance(args[0][0], list):
            raise NestedObjectsNotSupportedError(args[0])

        return method(self, *args, **kwargs)

    return wrapper




class StringMatcher:

    def __init__(
        self,
        min_sim: float = 0.5,
        min_sim_retrieval: float = 0.6,
        case_sensitive: bool = False,
        exact: bool = False,
    ):
        self.min_sim = min_sim
        self.min_sim_retrieval = min_sim_retrieval
        self.exact = exact
        self.case_sensitive = case_sensitive

        if self.exact:
            self.vocab = KeywordProcessor(
                case_sensitive=self.case_sensitive
            )
        else:
            self.vocab = FuzzySet(
                use_levenshtein=True,
                rel_sim_cutoff=self.min_sim_retrieval,
            )

    def __str__(self):
        meta_keys = [
            "min_sim_retrieval",
            "case_sensitive",
            "exact"
        ]
        meta = {
            'current': str(self.__class__.__name__),
            'parent': str(self.__class__.__base__),
        }
        meta.update({key: self.__dict__[key] for key in meta_keys})
        return json.dumps(meta)

    @reject_nested_input
    def __call__(self, documents: Union[str, List[str]]):
        if isinstance(documents, str):
            return self([documents]).pop()
        func = self.vocab.extract_keywords if self.exact \
               else self.vocab.get
        matches = []
        for document in documents:
            _matches = func(document)
            matches.append(_matches if _matches else [])
        return self.__filter_by_jaro_distance(matches)

    def __filter_by_jaro_distance(
        self,
        matches: List[Union[str, Tuple[float, str]]]
    ) -> List[Union[str, Tuple[float, str]]]:
        if isinstance(self, ExactStringMatcher):
            return matches
        else:
            return [
                [ (score, text) for score, text in _match
                  if score >= self.min_sim ]
                for _match in matches
            ]

    @reject_nested_input
    def add(self, word: Union[str, Tuple[str]]) -> None:
        if isinstance(word, tuple) and self.exact:
            self.add_mapping(*word)
        elif isinstance(word, tuple):
            raise AttemptedToAddTupleToFuzzyVocabulary(word)
        elif self.exact:
            self.vocab.add_keyword(word)
        else:
            self.vocab.add(word)

    def add_mapping(self, word_from: str, word_to: str) -> None:
        self.vocab.add_keyword(word_from, word_to)

    @reject_nested_input
    def __iadd__(self, words: List[str]) -> Any:
        for word in words:
            self.add(word)
        return self

    @reject_nested_input
    def fit(self, words: List[str]) -> None:
        self += words

    @reject_nested_input
    def filter(self, words: List[str]) -> bool:
        return [word in self for word in words]

    def __contains__(self, word: str) -> bool:
        return True if self(word) else False

    @reject_nested_input
    def transform(self, documents: List[str]) -> List[str]:
        if not self.exact:
            raise OperationNotYetSupportedForFuzzyVocabulary()
        if isinstance(documents, str):
            return self.transform([documents]).pop()
        else:
            return [
                self.vocab.replace_keywords(document)
                for document in documents
            ]


class ExactStringMatcher(StringMatcher):

    def __init__(self, *args, **kwargs) -> None:
        params = dict(kwargs)
        params["exact"] = True
        super().__init__(*args, **params)



class FuzzyStringMatcher(StringMatcher):

    def __init__(self, *args, **kwargs) -> None:
        params = dict(kwargs)
        params["exact"] = False
        super().__init__(*args, **params)


