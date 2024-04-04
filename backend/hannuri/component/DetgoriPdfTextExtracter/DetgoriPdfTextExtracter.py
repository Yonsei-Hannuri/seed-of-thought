import pdftotext
from kiwipiepy import Kiwi
import re

class DetgoriPdfTextExtracter:

    def __init__(self):
        self.kiwi = Kiwi()
    
    def extract_text(self, file_path):
        pdf = None
        with open(file_path, "rb") as f:
            pdf = pdftotext.PDF(f)
        if pdf is None:
            raise Exception('failed to extract text from the file')
        text = '\n'.join(pdf)
        text = re.sub(r'2\d{3}-[12]{1} *한누리 *댓거리_? *\d{1}[주회]차?', '',text)
        lines = text.split("\n")
        meta = []
        i = 0
        for line in lines:
            if line != '':
                meta.append(line)
            if len(meta) == 2:
                break
            i += 1

        content = self.kiwi.glue(filter(lambda e: e not in ['\x0c', ''], lines[i+1:]))
        
        return content