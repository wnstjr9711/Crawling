from ProjectFinal import *


class SearchEngineWithOrderedWebWords(SearchEngine):
    def __init__(self, *args):
        super().__init__(*args)

    def getWordsFrequency(self, reverse=False):
        for url in self.source:     # 스태틱메소드를 호출하여 word 리스트에 모든 단어를 담는다.
            self.word += pure_word_list(self.getwords(url).lower())     # 구두문자와 불용어가 삭제된 소문자 단어 리스트
        for key in self.word:
            if self.freq_dict.get(key):
                self.freq_dict[key] += 1
            else:
                self.freq_dict[key] = 1
        sorted_list = list(tuple(zip(self.freq_dict.keys(), self.freq_dict.values())))
        if reverse is True:
            return sorted(sorted_list, key=lambda x: x[1])
        else:
            return sorted(sorted_list, key=lambda x: x[1], reverse=True)

    def __iter__(self):
        return self

    def __next__(self):
        return next(iter(sorted(list(self.freq_dict.items()), key=lambda x: x[1], reverse=True)))


if __name__ == '__main__':
    w4 = SearchEngineWithOrderedWebWords('https://www.amazon.com', 'https://github.com')
    print(w4.getWordsFrequency())
    for i in w4:
        print(i)
