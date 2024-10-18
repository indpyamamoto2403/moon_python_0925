from dataclasses import dataclass

@dataclass
class InputDataset:
    '''
    input要素を格納するクラス
    '''
    keyword1:str = ""
    keyword2:str = ""
    keyword3:str = ""
    const_search_word:str = "ニュース"
    
    conbined_keyword:str = None
    
    def __post_init__(self):
        '''
        conbined keywordをセット
        すべて空文字であればNoneを返す
        '''
        #結合したキーワードからNoneを取り除く
        self.conbined_keyword = f"{self.keyword1} {self.keyword2} {self.keyword3} {self.const_search_word}".replace("None", "").strip()
        if self.keyword1 == "" and self.keyword2 == "" and self.keyword3 == "":
            self.conbined_keyword = " "
    
    def get_combined_keyword(self):
        return self.conbined_keyword