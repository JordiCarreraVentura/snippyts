import os
import time
from pathlib import Path
from typing import Any

from src.snippyts import (
    tryline,
    from_json,
    from_pickle,
    to_json,
    to_pickle
)

SUPPORTED_FORMATS = ["json", "pickle"]
REFRESH_INTERVAL = 180

class UnsupportedFormatForPersistenceError(ValueError): ...


class Cachionary:

    def __init__(
        self,
        path: str | Path,
        format: str = "json",         # SUPPORTED_FORMATS
        refresh_interval: int = REFRESH_INTERVAL
    ) -> None:
        tryline(
            lambda x: x in SUPPORTED_FORMATS,
            UnsupportedFormatForPersistenceError,
            [format]
        )
        self.path = Path(path).expanduser().resolve()
        self.path.parent.mkdir(exist_ok=True, parents=True)
        self.refresh_interval = refresh_interval
        self.last_persisted = time.time()
        if os.path.exists(self.path):
            #self.payload = snippyts.from_json(self.path)
            self.payload = from_pickle(self.path)
        else:
            self.payload = dict([])

    def __contains__(self, key: object) -> bool:
        return key in self.payload

    def __getitem__(self, key: object) -> Any:
        return self.payload.get(key, None)
    
    def get(self, key: object) -> Any:
        return self[key]

    def __setitem__(self, key: object, val: object) -> None:
        self.payload[key] = val
        self.persist()
    
    def persist(self, force: bool = False) -> None:
        if (
            force 
            or (time.time() - self.last_persisted >= self.refresh_interval)
        ):
            #snippyts.to_json(self.payload, self.path)
            to_pickle(self.payload, self.path)
            self.last_persisted = time.time()


if __name__ == "__main__":
    cnary = Cachionary()
