from django.test import TestCase
from hannuri.job.WordCountAggregateJob import WordCountAggregateJob
from hannuri.models import Detgori, Sentence, Word, SentenceWord, User, Season, Session

class WordCountAggregateJobTest(TestCase):
    
    def setUp(self):
        # 테스트 데이터 생성
        self.user = User.objects.create(name="테스트유저")
        self.season = Season.objects.create(year=2024, semester=1)
        self.session = Session.objects.create(season=self.season, week=1)
        
        # Detgori 생성
        self.detgori1 = Detgori.objects.create(
            parentSession=self.session,
            author=self.user,
            title="테스트글1"
        )
        self.detgori2 = Detgori.objects.create(
            parentSession=self.session,
            author=self.user,
            title="테스트글2"
        )
        self.detgori3 = Detgori.objects.create(
            parentSession=self.session,
            author=self.user,
            title="테스트글3"
        )

        # 문장, 단어, SentenceWord 생성
        self.sentence1 = Sentence.objects.create(
            detgori=self.detgori1,
            content="한글 공부하기",
            seq_no=1
        )
        self.sentence2 = Sentence.objects.create(
            detgori=self.detgori2,
            content="한글 시험보기",
            seq_no=1
        )
        self.sentence3 = Sentence.objects.create(
            detgori=self.detgori3,
            content="한글 말하기, 한글 듣기 시험 준비하기",
            seq_no=1
        )

        self.word1 = Word.objects.create(word="한글")
        self.word2 = Word.objects.create(word="공부")
        self.word3 = Word.objects.create(word="시험")
        self.word4 = Word.objects.create(word="말")
        self.word5 = Word.objects.create(word="준비")
        self.word6 = Word.objects.create(word="듣기")

        # SentenceWord 연결
        SentenceWord.objects.create(sentence=self.sentence1, word=self.word1, count=1)
        SentenceWord.objects.create(sentence=self.sentence1, word=self.word2, count=1)
        SentenceWord.objects.create(sentence=self.sentence2, word=self.word1, count=1)
        SentenceWord.objects.create(sentence=self.sentence2, word=self.word3, count=1)
        SentenceWord.objects.create(sentence=self.sentence3, word=self.word1, count=2)
        SentenceWord.objects.create(sentence=self.sentence3, word=self.word3, count=1)
        SentenceWord.objects.create(sentence=self.sentence3, word=self.word4, count=1)
        SentenceWord.objects.create(sentence=self.sentence3, word=self.word5, count=1)
        SentenceWord.objects.create(sentence=self.sentence3, word=self.word6, count=1)

    def test_aggregate_word_count(self):
        job = WordCountAggregateJob()
        result = job.aggregate_word_count([self.detgori1.id, self.detgori2.id])

        # 예상되는 결과
        expected = {
            "한글": 2,  # 두 문장에서 각각 1번씩
            "공부": 1,  # 첫 번째 문장에서 1번
            "시험": 1,  # 두 번째 문장에서 1번
        }

        self.assertEqual(dict(result), expected)

    def test_aggregate_word_count_2(self):
        job = WordCountAggregateJob()
        result = job.aggregate_word_count([
            self.detgori1.id, 
            self.detgori2.id,
            self.detgori3.id
        ])

        # 예상되는 결과
        expected = {
            "한글": 4,  
            "공부": 1,  
            "시험": 2, 
            "말": 1,
            "준비": 1,
            "듣기": 1,
        }

        self.assertEqual(dict(result), expected)    
    
    def test_aggregate_word_count_empty_detgori(self):
        job = WordCountAggregateJob()
        result = job.aggregate_word_count([999])  # 존재하지 않는 뎃거리 ID
        
        self.assertEqual(dict(result), {})

    def test_aggregate_word_count_single_detgori(self):
        job = WordCountAggregateJob()
        result = job.aggregate_word_count([self.detgori1.id])

        expected = {
            "한글": 1,
            "공부": 1,
        }

        self.assertEqual(dict(result), expected)