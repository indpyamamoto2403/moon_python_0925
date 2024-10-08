from dataclasses import dataclass, field
from typing import Any, List, Dict

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
    split_info: SplitInfo = None
    execute_split: bool = False 
    ChunkSet: List[Chunk] = field(default_factory=list)
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
        self.integration_content = ' '.join([chunk.summary for chunk in self.ChunkSet])
        
@dataclass
class SearchResult:
    rank:int
    url:str
    summary:SummarizationDataset


@dataclass
class InputDataset:
    '''
    input要素を格納するクラス
    '''
    keyword1:str = ""
    keyword2:str = ""
    keyword3:str = ""
    const_search_word:str = "ニュース"
    
    conbined_keyword:str = None
    
    def __post_init__(self):
        '''
        conbined keywordをセット
        すべて空文字であればNoneを返す
        '''
        self.conbined_keyword = f"{self.keyword1} {self.keyword2} {self.keyword3} {self.const_search_word}"
        if self.keyword1 == "" and self.keyword2 == "" and self.keyword3 == "":
            self.conbined_keyword = None

@dataclass
class EntireDataset:
    '''
    インプットしたキーワード等の情報と、URLと要約データセットを格納するクラス
    '''
    input_dataset:InputDataset
    output_dataset: list = field(default_factory=list) #list[SearchResult]を有する