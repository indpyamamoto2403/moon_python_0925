classDiagram
    class Chunk {
        +int index
        +str chunk
        +str summary
    }

    class SplitInfo {
        +int split_chunk_size
        +int split_overlap
    }

    class SummarizationDataset {
        +str prompt
        +str origin_text
        +SplitInfo split_info
        +List~Chunk~ ChunkSet
        +str integration_content
        +str integration_summary
        +int origin_text_length
        +set_integration_content()
    }

    class SearchResult {
        +int rank
        +str url
        +SummarizationDataset summary
    }

    class NewsSearchResult {
        +str keyword1
        +str keyword2
        +str keyword3
        +int search_num
        +List~SearchResult~ search_result
        +str search_word
        +get_search_result()
    }

    SummarizationDataset o-- SplitInfo : has
    SummarizationDataset o-- Chunk : contains
    SearchResult o-- SummarizationDataset : contains
    NewsSearchResult o-- SearchResult : contains
