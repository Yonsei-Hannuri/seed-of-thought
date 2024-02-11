from konlpy.tag import Mecab

class MecabKoreanWordAnalyzer(KoreanWordAnalyzer):
    
    def extract_nouns(self, text):
        mecab = Mecab()
        return mecab.nouns(text)
