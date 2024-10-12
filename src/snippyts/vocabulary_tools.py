import json

from flashtext2 import KeywordProcessor

try:
    from cfuzzyset import cFuzzySet as FuzzySet
except ImportError:
    from fuzzyset import FuzzySet

from typing import Any, List, Tuple, Union



class AttemptedToAddTupleToFuzzyVocabulary(RuntimeError):
    pass

class OperationNotYetSupportedForFuzzyVocabulary(NotImplementedError):
    pass



class StringMatcher:

    def __init__(
        self,
        min_sim_retrieval: float = 0.6,
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

    def __call__(self, documents: str):
        if isinstance(documents, str):
            return self([documents]).pop()
        func = self.vocab.extract_keywords if self.exact \
               else self.vocab.get
        return [func(document) for document in documents]

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

    def __iadd__(self, words: List[str]) -> Any:
        for word in words:
            self.add(word)
        return self

    def fit(self, words: List[str]) -> None:
        self += words

    def filter(self, words: List[str]) -> bool:
        return [word in self for word in words]

    def __contains__(self, word: str) -> bool:
        if self.exact:
            return True if self(word) else False
        else:
            matches = self.vocab.get(word)
            return True if matches else False

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



def test_exact_add_words():

    terms = ["uno", "dos", "tres"]
    sm = ExactStringMatcher(case_sensitive=True)
    sm.add("uno")
    sm.add("dos")
    sm.add("tres")

    assert not sm("Uno")
    assert sm("uno")
    assert len(sm("uno")) == 1
    assert len(sm("Uno")) == 0


def test_exact_iadd_words():

    terms = ["uno", "dos", "tres"]
    sm = ExactStringMatcher(case_sensitive=True)
    sm += terms

    assert not sm("Uno")
    assert sm("uno")
    assert len(sm("uno")) == 1
    assert len(sm("Uno")) == 0


def test_exact_contains_word():

    terms = ["uno", "dos", "tres"]
    sm = ExactStringMatcher(case_sensitive=True)
    sm += terms

    assert "uno" in sm
    assert "tres" in sm
    assert "Uno" not in sm
    assert "cuatro" not in sm


def test_exact_filter_words():

    terms = ["uno", "dos", "tres"]
    sm = ExactStringMatcher(case_sensitive=True)
    sm += terms

    words = ["dos", "cinco", "tres", "cuatro"]
    expected = [True, False, True, False]

    filtered = sm.filter(words)
    assert filtered == expected



def test_exact_extract_words():

    terms = ["uno", "dos", "tres"]
    sm = ExactStringMatcher()
    sm += terms

    text = " ".join([
        "dos", "cinco", "tres", "cuatro",
        "seis", "siete", "ocho", "nueve",
        "dieciseis", "doce", "cuarenta", "diantres",
        "dos", "tres", "tres"
    ])
    expected = "dos tres dos tres tres".split()

    extracted = sm(text)
    assert extracted == expected



def test():

    test_exact_add_words()
    test_exact_iadd_words()
    test_exact_contains_word()
    test_exact_filter_words()
    test_exact_extract_words()
    terms = [
       "orca", "Orco", "orco", "oro",
       "orwelliano", "oráculo", "oración",
    ]

    fsm = FuzzyStringMatcher(min_sim_retrieval=0.5)
    fsm += terms
    for term in terms:
        print(term, fsm(term))

    esm = ExactStringMatcher()
    esm += terms
    for term in terms:
        print(term, esm(term))



if __name__ == '__main__':
    test()
