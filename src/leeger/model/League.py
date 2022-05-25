from dataclasses import dataclass
from typing import List

from src.leeger.model.Owner import Owner
from src.leeger.model.Year import Year
from src.leeger.model.abstract.UniqueId import UniqueId


@dataclass(kw_only=True)
class League(UniqueId):
    """test"""
    name: str
    owners: List[Owner]
    years: List[Year]
