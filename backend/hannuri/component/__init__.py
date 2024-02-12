from .PdfTextExtracter.PdfMinerExtracter import PdfMinerExtracter
from .KoreanWordAnalyzer.MecabKoreanWordAnalyzer import MecabKoreanWordAnalyzer
from .WordCounter.SimpleWordCounter import SimpleWordCounter
from .GoogleOauth.GoogleOauth import GoogleOauth
from .ObjectStorage.S3 import S3

pdfTextExtracter = PdfMinerExtracter()
koreanWordAnalyzer = MecabKoreanWordAnalyzer()
wordCounter = SimpleWordCounter() 
googleOauth = GoogleOauth()
objectStorage = S3()