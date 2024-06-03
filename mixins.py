from pony.orm import select, db_session
from datetime import date, time, datetime
from abc import ABC
from typing import Any
from decimal import Decimal
import models

class ListMixin(ABC):
    @db_session
    def get(self) -> list[dict[str, Any]]:
        if not hasattr(self, 'dict'):
            return [element.to_dict() for element in self.query]
        
        dicts = []
        for tup in self.query:
            tup = list(tup)
            tup = [float(item) if isinstance(item, Decimal) else item for item in tup]
            tup = [str(item) if isinstance(item, (date, time, datetime)) else item for item in tup]
            element = {key: value for key, value in zip(self.dict.__annotations__.keys(), tup)}
            dicts.append(element)
        
        return dicts