#https://bab2min.github.io/kiwipiepy/v0.17.0/kr/
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords

class TextAnalyzer:

    COUNT_TARGETS = ['NNG', 'NNP']

    def __init__(self):
        self.kiwi = Kiwi()

    def count_words(self, text):
        words = self.kiwi.tokenize(text)
        counts = dict()
        for word in words:
            w = word.form
            t = word.tag
            if t not in TextAnalyzer.COUNT_TARGETS:
               continue
            if not w in counts.keys():
                counts[w] = 1
            else:
                counts[w] += 1
        return counts
    
    def split_into_sentences(self, text):
        return [elem.text for elem in self.kiwi.split_into_sents(text)]
