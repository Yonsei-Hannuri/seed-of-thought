from .PdfTextExtracter.PdfMinerExtracter import PdfMinerExtracter
from .KoreanWordAnalyzer.MecabKoreanWordAnalyzer import MecabKoreanWordAnalyzer
from .WordCounter.SimpleWordCounter import SimpleWordCounter

pdfTextExtracter = PdfMinerExtracter()
koreanWordAnalyzer = MecabKoreanWordAnalyzer()
wordCounter = SimpleWordCounter() 