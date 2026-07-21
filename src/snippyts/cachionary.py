import os
from pathlib import Path
from typing import Any, Iterable, List

from src.snippyts import (
    tryline,
    from_json,
    from_pickle,
    to_json,
    to_pickle,
)

SUPPORTED_FORMATS = ["json", "pickle"]
REFRESH_INTERVAL = 180


class ExcludedMiddleViolation(ValueError): ...

class UnsupportedFormatForPersistenceError(ValueError): ...


class Cachionary:

    def __init__(
        self,
        path: str | Path,
        format: str = "json"         # SUPPORTED_FORMATS
    ) -> None:
        tryline(
            lambda x: x in SUPPORTED_FORMATS,
            UnsupportedFormatForPersistenceError,
            [format]
        )
        self.format = format
        self.new_keys = set([])
        self.path = Path(path).expanduser().resolve()
        self.path.parent.mkdir(exist_ok=True, parents=True)
        self.payload = dict([])
        self.reload()
        atexit.register(self.persist)
    
    def __len__(self) -> int:
        return len(self.payload) + len(self.new_keys)
    
    def __iter__(self) -> Iterable[Any]:
        for key in self.payload.keys():
            yield key
    
    def keys(self) -> List[Any]:
        return [key for key in self]

    def values(self) -> List[Any]:
        return [self[key] for key in self]
    
    def reload(self) -> None:
        if not os.path.exists(self.path):
            return
        prev_records = (
            from_json(self.path) if self.format == "json"
            else from_pickle(self.path)
        )
        self.payload.update(prev_records)

    def persist(self):
        if self.format == "json":
            to_json(self.payload, self.path)
        elif self.format == "pickle":
            to_pickle(self.payload, self.path)
        else:
            raise ExcludedMiddleViolation(
                f"got {self.format} but expected {str(SUPPORTED_FORMATS)}"
            )

    def __del__(self) -> None:
        if hasattr(self, "format") and (self.payload or self.path.exists()):
            self.persist()

    def __contains__(self, key: object) -> bool:
        return key in self.payload

    def __getitem__(self, key: object) -> Any:
        try:
            return self.payload[key]
        except Exception:
            raise KeyError(key)
    
    def get(self, key: object, default: Any = None) -> Any:
        return self.get(key, default)

    def __setitem__(self, key: object, val: object) -> None:
        self.payload[key] = val


if __name__ == "__main__":
    f = "jfeijfe"
    cnary = Cachionary(path=f, format="pickle")

    print(1 in cnary)
    print(2 in cnary)
    
    cnary[1] = "uno"
    cnary[2] = "dos"
    cnary[3] = "tres"

    print(cnary.payload)

    input()
