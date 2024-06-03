from pony.orm import select, db_session
from abc import ABC
from typing import Any
import models

class ListMixin(ABC):
    @db_session
    def get(self) -> list[dict[str, Any]]:
        return [element.to_dict() for element in self.query]