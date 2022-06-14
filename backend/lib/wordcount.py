from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from konlpy.tag import Mecab
import json

meaningless_words = ('한누리', '아무것', '누구', '거기', '그것', '이것', '거리',)

def read_pdf(f):
    output_string = StringIO()
    parser = PDFParser(f)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    
    return output_string.getvalue()

def tokenizer(text):
    mecab = Mecab()
    nouns = mecab.nouns(text)
    words = counter(nouns)
    return words

def counter(nouns):
    res = dict()
    for noun in nouns:
        if len(noun)==1 or noun in meaningless_words:
            continue
        elif not(noun in res.keys()):
            res[noun] = 1
        else:
            res[noun] += 1
    return json.dumps(res)