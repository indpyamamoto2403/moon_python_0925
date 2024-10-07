from langchain.text_splitter import RecursiveCharacterTextSplitter
class Trimmer:
    @staticmethod
    def trim_lines(text: str):
        return [line.strip() for line in text.splitlines() if line.strip()]

    @staticmethod
    def trim_spaces(text: str):
        return ' '.join(text.split())

    @staticmethod
    def trim_all(text: str):
        return Trimmer.trim_spaces(text), Trimmer.trim_lines(text)
    

class TextSplitter:
    @staticmethod
    def split(text, chunk_size=1000, chunk_overlap=20):
        """
        テキストを指定された長さで分割し、オーバーラップも考慮したリストと共に情報を返す
        """
        # テキストスプリッターの設定
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        split_texts = text_splitter.split_text(text)
        result = {
            "original_text": text,               # 元のテキスト
            "split_count": len(split_texts),      # 分割された数
            "chunks": []                         # 各チャンクのインデックスとテキストをリスト化
        }
        for idx, chunk in enumerate(split_texts):
            result["chunks"].append({
                "index": idx,
                "text": chunk
            })
        return result

long_text = "ここに長いテキストを挿入します。非常に長いテキストを想定しています。" * 500 
    


if __name__ == "__main__":
    # 使用例
    text = """
    This is   some   example text.   

    It has   extra spaces    and
    newlines that need trimming.   
    """
    trimmed_spaces, trimmed_lines = Trimmer.trim_all(text)
    print(trimmed_spaces)
    print(trimmed_lines)

    long_text = "ここに非常に長いテキストを挿入します。" * 500
    
    # staticmethodを直接呼び出し
    result = TextSplitter.split(long_text, chunk_size=1000, chunk_overlap=20)