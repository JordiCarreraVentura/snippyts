from flashtext import KeywordProcessor

try:
    from cfuzzyset import cFuzzySet as FuzzySet
except ImportError:
    from fuzzyset import FuzzySet

from fuzzyset import FuzzySet()

from typing import Any, List, Tuple



class AttemptedToAddTupleToFuzzyVocabulary(RuntimeError):
    pass

class OperationNotYetSupportedForFuzzyVocabulary(NotImplementedError):
    pass


class StringMatcher:

    def __init__(
        self,
        min_sim_retrieval: float = 0.6
        case_sensitive: bool = False,
        exact: bool = False,
    ):
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

    def __call__(self, word: str):
        if self.exact:
            raise self.extract_keywords(word)
        else:
            return self.vocab.get(word)

    def add(self, word: str) -> None:
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

    def __iadd__(self, words: List[str]) -> Any:
        for word in words:
            self.add(word)

    def fit(self, words: List[str]) -> None:
        self += words

    def __contains__(self, word: str) -> bool:
        if self.exact:
            raise NotImplementedError()
        else:
            matches = self.vocab.get(word)
            return True if matches else False

    def transform(self, documents: List[str]) -> List[str]:
        if not self.exact:
            raise OperationNotYetSupportedForFuzzyVocabulary()
        return [
            self.vocab.replace_keywords(document)
            document for documents
        ]


if __name__ == '__main__':

    sm = StringMatcher()
