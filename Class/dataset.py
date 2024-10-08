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
        
@dataclass
class SearchResult:
    rank:int
    url:str
    summary:SummarizationDataset

@dataclass
class NewsSearchResult:
    keyword1:str
    keyword2:str
    keyword3:str
    search_num:int
    search_result:List[SearchResult] #URLとその内容を格納する辞書のリスト
    
    def __post_init__(self):
        '''
        conbinated keywordをセット
        '''
        self.search_word = f"{self.keyword1}  {self.keyword2} {self.keyword3} ニュース"
    
    def get_search_result(self):
        '''
        search_resultを返す
        '''
        return self.search_word