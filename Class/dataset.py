from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Chunk:
    index: int
    chunk: str
    summary: str

@dataclass
class SplitInfo:
    split_chunk_size:int
    split_oqverlap:int

@dataclass
class SummarizationDataset:
    prompt: str
    origin_text: str
    split_info: SplitInfo
    ChunkSet: List[Chunk] = field(default_factory=list)
    integration_content: str = ""
    integration_summary: str = ""
    
    def __post_init__(self):
        '''
        origin_textの長さを自動的に計算してorigin_text_lengthにセット
        '''
        self.origin_text_length = len(self.origin_text)
                
    def set_integration_content(self):
        '''
        ChunkSetの内容を統合してintegration_contentにセット
        '''
        self.integration_content = ' '.join([chunk.summary for chunk in self.ChunkSet])

