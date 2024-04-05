from .DetgoriPdfTextExtracter.DetgoriPdfTextExtracter import DetgoriPdfTextExtracter
from .TextAnalyzer.TextAnalyzer import TextAnalyzer
from .GoogleOauth.GoogleOauth import GoogleOauth
from .ObjectStorage.S3 import S3
from .DetgoriSentenceApi.DetgoriSentenceApi import DetgoriSentenceApi

detgoriPdfTextExtracter = DetgoriPdfTextExtracter()
textAnalyzer = TextAnalyzer()
googleOauth = GoogleOauth()
objectStorage = S3()
detgoriSentenceApi = DetgoriSentenceApi()