from dataclasses import dataclass, field

@dataclass
class BusinessExtractionData:
    '''
    事業内容を抽出するときに運搬されるDTO
    '''
    search_type: str = ""
    keyword: str = ""
    url: str = ""
    content: str = ""
    prompt: str = ""
    answer: str = ""
