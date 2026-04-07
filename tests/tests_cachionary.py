import os
from pathlib import Path

from src.snippyts import tryline
from src.snippyts.cachionary import Cachionary

PATH_TESTS_MODULE = Path(os.path.realpath(__file__))
PATH_REPO = PATH_TESTS_MODULE.parent.parent
PATH_CACHIONARY_JSON = PATH_REPO / "cachionary.json"

def clear():
    if os.path.exists(PATH_CACHIONARY_JSON):
        os.remove(PATH_CACHIONARY_JSON)

def test_param_format_true():
    cnary = Cachionary(PATH_CACHIONARY_JSON)
    cnary = Cachionary(PATH_CACHIONARY_JSON, format="json")
    cnary = Cachionary(PATH_CACHIONARY_JSON, format="pickle")
    clear()
    assert True

def test_param_format_false():
    try:
        cnary = Cachionary(PATH_CACHIONARY_JSON, format="csv")
    except Exception:
        assert True
    clear()


if __name__ == "__main__":
    test_param_format_true()
    test_param_format_false()