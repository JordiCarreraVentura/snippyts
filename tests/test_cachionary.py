import os
from pathlib import Path

from src.snippyts import Cachionary
from src.snippyts.cachionary import Cachionary as CachionaryFromModule

PATH_TESTS_MODULE = Path(os.path.realpath(__file__))
PATH_REPO = PATH_TESTS_MODULE.parent.parent
PATH_CACHIONARY_JSON = PATH_REPO / "cachionary.json"

def clear():
    if os.path.exists(PATH_CACHIONARY_JSON):
        os.remove(PATH_CACHIONARY_JSON)

def test_param_format_true():
    clear()
    _ = Cachionary(PATH_CACHIONARY_JSON)
    _ = Cachionary(PATH_CACHIONARY_JSON, format="json")
    _ = Cachionary(PATH_CACHIONARY_JSON, format="pickle")
    clear()
    assert True

def test_public_imports():
    assert Cachionary is CachionaryFromModule

def test_param_format_false():
    try:
        cnary = Cachionary(PATH_CACHIONARY_JSON, format="csv")
    except Exception:
        assert True
    clear()

def test_cachionary():
    path_test_cachionary = "cachionary_test.json"
    if os.path.exists(path_test_cachionary):
        os.remove(path_test_cachionary)
    assert not os.path.exists(path_test_cachionary)
    cachionary = Cachionary(path_test_cachionary)
    assert len(cachionary) == 0
    cachionary[1] = 1
    cachionary[2] = 2
    assert len(cachionary) == 2
    assert cachionary.get(1) == 1
    assert cachionary.get("missing", "default") == "default"
    del cachionary
    assert os.path.exists(path_test_cachionary)
    _cachionary = Cachionary(path_test_cachionary)
    assert len(_cachionary) == 2
    del _cachionary
    os.remove(path_test_cachionary)



if __name__ == "__main__":
    test_cachionary()
    test_public_imports()
    test_param_format_true()
    test_param_format_false()
