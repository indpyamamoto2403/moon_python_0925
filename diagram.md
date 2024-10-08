```mermaid
classDiagram
    class Chunk {
        int index
        string chunk
        string summary
    }
    
    class SplitInfo {
        int split_chunk_size
        int split_oqverlap
    }
    
    class SummarizationDataset {
        string prompt
        string origin_text
        int origin_text_length
        SplitInfo split_info
        List~Chunk~ ChunkSet
        string integration_content
        string integration_summary
        set_integration_content()
    }
    
    SummarizationDataset --> Chunk : "List of"
    SummarizationDataset --> SplitInfo : "1"
