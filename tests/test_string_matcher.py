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



def test_exact_replace_words():

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


def test_fuzzy_add_words():

    terms = [
        "alpha", "beta", "gamma", "delta",
        "eta", "epsilon", "omicron", "omega",
        "tau", "mu", "nu", "chi", "rho", "iota",
        "lambda", "theta", "sigma", "psi", "pi"
    ]
    sm_05 = FuzzyStringMatcher(min_sim_retrieval=0.5)
    sm_08 = FuzzyStringMatcher(min_sim_retrieval=0.8)
    for term in terms:
        sm_05.add(term)
        sm_08.add(term)

    results_05 = sm_05("eta")
    results_08 = sm_08("eta")
    assert len(results_05) == 5
    assert len(results_08) == 1
    assert results_05[0][0] == 1.0
    assert results_05[2][0] == 0.6
    assert results_05[1][1] == "beta"
    assert results_08[0][0] == 1.0
    assert results_08[0][1] == "eta"



def test_fuzzy_iadd_words():

    terms = [
        "alpha", "beta", "gamma", "delta",
        "eta", "epsilon", "omicron", "omega",
        "tau", "mu", "nu", "chi", "rho", "iota",
        "lambda", "theta", "sigma", "psi", "pi"
    ]
    sm_05 = FuzzyStringMatcher(min_sim_retrieval=0.5)
    sm_05 += terms
    sm_08 = FuzzyStringMatcher(min_sim_retrieval=0.8)
    sm_08 += terms

    results_05 = sm_05("eta")
    results_08 = sm_08("eta")
    assert len(results_05) == 5
    assert len(results_08) == 1
    assert results_05[0][0] == 1.0
    assert results_05[2][0] == 0.6
    assert results_05[1][1] == "beta"
    assert results_08[0][0] == 1.0
    assert results_08[0][1] == "eta"


def test_fuzzy_contains_word():

    terms = [
        "alpha", "beta", "gamma", "delta",
        "eta", "epsilon", "omicron", "omega",
        "tau", "mu", "nu", "chi", "rho", "iota",
        "lambda", "theta", "sigma", "psi", "pi"
    ]
    sm_05 = FuzzyStringMatcher(min_sim_retrieval=0.5, min_sim=0.0)
    sm_05 += terms

    assert "eta" in sm_05
    assert "laetitia" in sm_05
    assert "111000" not in sm_05


    sm_08 = FuzzyStringMatcher(min_sim_retrieval=0.8, min_sim=0.5)
    sm_08 += terms

    assert "eta" in sm_08
    assert "laetitia" not in sm_08
    assert "111000" not in sm_08


def test_fuzzy_filter_words():

    terms = [
        "alpha", "beta", "gamma", "delta",
        "eta", "epsilon", "omicron", "omega",
        "tau", "mu", "nu", "chi", "rho", "iota",
        "lambda", "theta", "sigma", "psi", "pi"
    ]

    words = [
        "alphabet",
        "omegan",
        "lambda func"
    ]

    sm = FuzzyStringMatcher(min_sim_retrieval=0.2, min_sim=0.8)
    sm += terms
    expected = [False, True, False]
    filtered = sm.filter(words)
    assert filtered == expected

    sm = FuzzyStringMatcher(min_sim_retrieval=0.2, min_sim=0.6)
    sm += terms
    expected = [True, True, False]
    filtered = sm.filter(words)
    assert filtered == expected


