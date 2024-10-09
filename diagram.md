classDiagram
    class AbstractChunk {
        +int index
        +str chunk
    }

    class Chunk {
        +str summary
    }

    class RaggedChunk {
        +str cosine_similarity
    }

    class SplitInfo {
        +int split_chunk_size
        +int split_overlap
    }

    class SummarizationDataset {
        +str prompt
        +str origin_text
        +int origin_text_length
        +SplitInfo split_info
        +bool execute_split
        +List<AbstractChunk> chunk_set
        +str integration_content
        +str summary
        +set_integration_content()
    }

    class SearchResult {
        +int rank
        +str url
        +SummarizationDataset summary
    }

    class InputDataset {
        +str keyword1
        +str keyword2
        +str keyword3
        +str const_search_word
        +str combined_keyword
        +set_combined_keyword()
    }

    class EntireDataset {
        +InputDataset input_dataset
        +List<SearchResult> output_dataset
    }

    AbstractChunk <|-- Chunk
    AbstractChunk <|-- RaggedChunk
    SummarizationDataset --> SplitInfo
    SummarizationDataset --> AbstractChunk
    SearchResult --> SummarizationDataset
    EntireDataset --> InputDataset
    EntireDataset --> SearchResult
