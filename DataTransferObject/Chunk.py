from dataclasses import dataclass, field
from typing import Any, List, Dict
from abc import ABC, abstractmethod


# 抽象基底クラス
@dataclass
class AbstractChunk:
    index: int
    chunk: str

@dataclass
class Chunk(AbstractChunk):
    summary: str

@dataclass
class RaggedChunk(AbstractChunk):
    cosine_similarity: str
