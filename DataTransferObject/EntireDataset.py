from dataclasses import dataclass, field
from InputDataset import InputDataset
@dataclass
class EntireDataset:
    '''
    インプットしたキーワード等の情報と、URLと要約データセットを格納するクラス
    '''
    input_dataset:InputDataset
    output_dataset: list = field(default_factory=list) #list[SearchResult]を有する