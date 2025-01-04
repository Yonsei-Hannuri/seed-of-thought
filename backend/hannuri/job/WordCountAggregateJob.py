from hannuri.models import Word, SentenceWord
from collections import defaultdict

class WordCountAggregateJob:
    def aggregate_word_count(self, detgori_ids):
        sentence_words = SentenceWord.objects.filter(sentence__detgori_id__in=detgori_ids).select_related('word').all()
        count = defaultdict(int)
        for sentence_word in sentence_words:
            count[sentence_word.word.word] += sentence_word.count
        return count
    
