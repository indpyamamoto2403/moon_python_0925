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

@dataclass
class SplitInfo:
    split_chunk_size:int
    split_oqverlap:int

@dataclass
class SummarizationDataset:
    prompt: str
    origin_text: str
    origin_text_length: int = field(init=False) 
    split_info: SplitInfo = None
    execute_split: bool = False 
    ChunkSet: List[AbstractChunk] = field(default_factory=list)
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
        #結合したキーワードからNoneを取り除く
        self.conbined_keyword = f"{self.keyword1} {self.keyword2} {self.keyword3} {self.const_search_word}".replace("None", "").strip()
        if self.keyword1 == "" and self.keyword2 == "" and self.keyword3 == "":
            self.conbined_keyword = " "
        print(self.conbined_keyword)

@dataclass
class EntireDataset:
    '''
    インプットしたキーワード等の情報と、URLと要約データセットを格納するクラス
    '''
    input_dataset:InputDataset
    output_dataset: list = field(default_factory=list) #list[SearchResult]を有する