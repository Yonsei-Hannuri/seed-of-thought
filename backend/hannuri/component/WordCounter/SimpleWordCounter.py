class SimpleWordCounter(WordCounter):
    def count(self, words: str[]) -> dict[str, int]:
        meaningless_words = ('한누리', '아무것', '누구', '거기', '그것', '이것', '거리',)
        counts = dict()
        for word in words:
            if len(word)==1 or word in meaningless_words:
                continue
            elif not(word in res.keys()):
                counts[word] = 1
            else:
                counts[word] += 1
        return counts