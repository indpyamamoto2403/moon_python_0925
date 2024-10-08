classDiagram
    class InputDataset {
        str keyword1
        str keyword2
        str keyword3
        str const_search_word
        str conbined_keyword
    }
    class EntireDataset {
        InputDataset input_dataset
        List~SearchResult~ output_dataset
    }
    class SearchResult {
        int rank
        str url
        SummarizationDataset summary
    }
    class SummarizationDataset {
        str prompt
        str origin_text
        SplitInfo split_info
        bool execute_split
        List~Chunk~ ChunkSet
        str integration_content
        str summary
        int origin_text_length
    }
    class SplitInfo {
        int split_chunk_size
        int split_oqverlap
    }
    class Chunk {
        int index
        str chunk
        str summary
    }


    %% 関係性を定義
    EntireDataset --> InputDataset : contains
    EntireDataset --> SearchResult : contains
    SearchResult --> SummarizationDataset : contains
    SummarizationDataset --> Chunk : contains
    SummarizationDataset --> SplitInfo : has
