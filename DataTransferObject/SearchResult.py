from dataclasses import dataclass, field
from SummarizationDataset import SummarizationDataset

@dataclass
class SearchResult:
    url:str
    origin:str
    summary:SummarizationDataset
    title:str
    rank: int = field(default=None)  # Noneをデフォルト値として設定