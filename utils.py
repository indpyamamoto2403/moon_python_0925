
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