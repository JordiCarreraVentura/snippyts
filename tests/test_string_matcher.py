import pytest

from src.snippyts import (
    ExactStringMatcher,
    FuzzyStringMatcher,
    NestedObjectsNotSupportedError
)



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



def test_exact_extract_words():

    terms = [
        ("uno", "1"),
        ("dos", "2"),
        ("tres", "3")
    ]
    sm = ExactStringMatcher()
    sm += terms

    text = " ".join([
        "dos", "cinco", "tres", "cuatro",
        "seis", "siete", "ocho", "nueve",
        "dieciseis", "doce", "cuarenta", "diantres",
        "dos", "tres", "tres"
    ])
    expected = "2 cinco 3 cuatro seis siete ocho nueve "\
               "dieciseis doce cuarenta diantres 2 3 3"

    transformed = sm.transform(text)
    assert transformed == expected



def test_exact_extract_words_many():

    terms = [
        ("uno", "1"),
        ("dos", "2"),
        ("tres", "3")
    ]
    sm = ExactStringMatcher()
    sm += terms

    documents = [
        "dos", "cinco", "tres", "cuatro",
        "seis", "siete", "ocho", "nueve",
        "dieciseis", "doce", "cuarenta", "diantres",
        "dos", "tres", "tres"
    ]
    expected = [
        "2", "cinco", "3", "cuatro",
        "seis", "siete", "ocho", "nueve",
        "dieciseis", "doce", "cuarenta", "diantres",
        "2", "3", "3"
    ]

    transformed = sm.transform(documents)
    assert transformed == expected



def test_exact_reject_nested_inputs():

    terms = [
        ("uno", "1"),
        ("dos", "2"),
        ("tres", "3")
    ]
    sm = ExactStringMatcher()
    sm += terms

    documents = [
        "dos", "cinco", "tres", "cuatro",
        "seis", "siete", "ocho", "nueve",
        "dieciseis", "doce", "cuarenta", "diantres",
        "dos", "tres", "tres"
    ]

    try:
        sm.transform([documents])
    except NestedObjectsNotSupportedError:
        assert True



# def test():
#     test_exact_add_words()
#     test_exact_iadd_words()
#     test_exact_contains_word()
#     test_exact_filter_words()
#     test_exact_extract_words()
#     test_exact_extract_words_many()
#     test_exact_reject_nested_inputs()

