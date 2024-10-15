from SplitInfo import SplitInfo
from dataclasses import dataclass, field
from Chunk import AbstractChunk
@dataclass
class SummarizationDataset:
    prompt: str
    origin_text: str
    origin_text_length: int = field(init=False) 
    split_info: SplitInfo = None
    execute_split: bool = False 
    ChunkSet: list[AbstractChunk] = field(default_factory=list)
    integration_content: str = ""
    summary: str = ""
    
    def __post_init__(self):
        '''
        origin_textの長さを自動的に計算してorigin_text_lengthにセット
        '''
        self.origin_text_length = len(self.origin_text)
                
    def set_integration_content(self):
        '''
        ChunkSetの内容を統合してintegration_contentにセット
        '''
        self.execute_split = True
        self.integration_content = ' '.join([chunk.summary for chunk in self.ChunkSet])