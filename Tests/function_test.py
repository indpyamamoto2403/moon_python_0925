import pytest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from html_parser import HTMLParser
from utils import TextSplitter
from pprint import pprint
from dataset import SummarizationDataset, Chunk
def test_html_parse():
    '''
    Test the HTMLParser class
    '''
    parser = HTMLParser()
    result = parser.fetch_content_from_url('https://www.python.org/')
    print(result)
    assert 'Python' in result
    
def test_text_split():
    long_text = "ここに長いテキストを挿入します。非常に長いテキストを想定しています。"
    result = TextSplitter.split(long_text, chunk_size=5, chunk_overlap=2)
        
    #それぞれのテキストを取り出す方法はこちら
    for text in result['chunks']:
        print(f'Index: {text["index"]}, Text: {text["text"]}')
        
    assert len(result['chunks']) == 11

def test_text_split_short_text():
    short_text = "短いテキスト"
    result = TextSplitter.split(short_text, chunk_size=10, chunk_overlap=2)
        
    # 短いテキストの場合、分割されないことを確認
    for text in result['chunks']:
        print(f'Index: {text["index"]}, Text: {text["text"]}')
        
    assert len(result['chunks']) == 1
    assert result['chunks'][0]['text'] == short_text
    
def test_question_answer_by_split():
    '''
    Test the question_answer_by_split method
    '''
    prompt = "事業内容を要約してください。"
    content = "ここに長いテキストを挿入します。非常に長いテキストを想定しています。"
    result = TextSplitter.split(content, chunk_size=5, chunk_overlap=2)
    partials = []
    for text in result['chunks']:
        partials.append(prompt + text['text'])
    summary = ' '.join(partials)
    assert len(partials) == 11
    assert '事業内容を要約してください' in summary

if __name__ == '__main__':
    test_text_split_short_text()
    pass