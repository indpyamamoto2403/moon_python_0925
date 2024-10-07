from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Chunk:
    index: int
    chunk: str
    summary: str

@dataclass
class SummarizationDataset:
    prompt: str
    origin_text: str
    ChunkSet: List[Chunk] = field(default_factory=list)
    integration_content: str = ""
    integration_summary: str = ""
    
    def set_integration_content(self):
        '''
        ChunkSetの内容を統合してintegration_contentにセット
        '''
        self.integration_content = ' '.join([chunk.summary for chunk in self.ChunkSet])

        