from konlpy.tag import Mecab

class MecabKoreanWordAnalyzer(KoreanWordAnalyzer):
    
    def extract_nouns(self, text: str) -> str[]:
        mecab = Mecab()
        return mecab.nouns(text)
