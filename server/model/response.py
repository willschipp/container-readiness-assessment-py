from dataclasses import dataclass

from typing import List

@dataclass
class Part:
    text: str

@dataclass
class Content:
    parts: List[Part]

@dataclass
class Candidate:
    content: Content

@dataclass
class GeminiReponse:
    candidates: List[Candidate]
