from dataclasses import dataclass, field
@dataclass
class SplitInfo:
    split_chunk_size:int
    split_oqverlap:int