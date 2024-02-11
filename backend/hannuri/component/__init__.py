from .PdfTextExtracter.PdfMinerExtracter import PdfMinerExtracter
from .KoreanWordAnalyzer.MecabKoreanWordAnalyzer import MecabKoreanWordAnalyzer
from .WordCounter.SimpleWordCounter import SimpleWordCounter
from .GoogleOauth.GoogleOauth import GoogleOauth

pdfTextExtracter = PdfMinerExtracter()
koreanWordAnalyzer = MecabKoreanWordAnalyzer()
wordCounter = SimpleWordCounter() 
googleOauth = GoogleOauth()