
class SerachResult:
    '''
    検索結果のURLを格納するDataTransferObject
    url: 検索結果のURL
    originText: 検索結果のテキスト
    summary: 要約されたテキスト
    split_num: 分割数
    split_method: 分割方法
    split_text: 分割されたテキスト
    
    '''
    def __init__(self, url:str, originText:str, summary:str, split_num:int = 0, split_method:str = "normal", split_text:list[str] = "", ):
        
        self.url:str = url
        self.originText:str = originText
        self.summary:str = summary
        self.split_num:int = split_num
        self.split_method:str = split_method
        self.split_text:list[str] = split_text
    
    def get_result(self):
        return {
            "url": self.url,
            "originText": self.originText,
            "summary": self.summary,
            "split_num": self.split_num,
            "split_method": self.split_method,
            "split_text": self.split_text,
        }
    
    def get_url(self):
        return self.url