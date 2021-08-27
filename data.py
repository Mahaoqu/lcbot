
from dataclasses import dataclass
from typing import List


@dataclass
class Problem:
    id: int
    url: str
    title: str
    difficulty: str  # easy, medium, hard
    topics: List[str]


@dataclass
class Record:
    uid: int
    p: Problem
