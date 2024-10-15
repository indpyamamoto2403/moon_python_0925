from dataclasses import dataclass
from SummarizationDataset import SummarizationDataset

@dataclass
class SearchResult:
    rank:int
    url:str
    summary:SummarizationDataset