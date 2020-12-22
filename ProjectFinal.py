from stop import *
import requests
import string


# assignment 3~4
def remove_tag(source):
    start = source.find('<')  # 없으면 -1 반환
    while start != -1:
        # script 태그 및 내용 제거
        if source[start:start+7] == '<script':   # len('<script') == 7
            end = source.find('/script>', start+7) + len('/script>')
            source = source.replace(source[start:end], ' ')
        # style 태그 및 내용 제거
        elif source[start:start+6] == '<style':     # len('<style') == 6
            end = source.find('/style>', start+6) + len('/style>')
            source = source.replace(source[start:end], ' ')
        elif source[start:start+4] == '<!--':       # len('<!--') == 4
            end = source.find('-->', start+4) + len('-->')
            source = source.replace(source[start:end], ' ')
        else:
            end = source.find('>', start+1) + len('>')
            source = source.replace(source[start:end], ' ')
        start = source.find('<', start)
    return source.split()


# 구두문자 삭제와 불용어 삭제
def delete_punctuation(raw_list):
    x = raw_list
    for p in string.punctuation:    # 구두문자 삭제
        x = ' '.join(x).split(p)
    x = ''.join(x).split()
    for stop in stopwords:      # 불용어 삭제
        while stop in x:
            x.remove(stop)
    return x


# 순수 단어 리스트 반환
def pure_word_list(source):
    return delete_punctuation(remove_tag(source))


# 유사도 계산 기본 함수(추출된 단어 빈도를 기준으로 계산)
def similarity_base(s, dictionary, similar):
    index = 0                           # url 순서
    for d in dictionary:                # url 순서대로 사전 불러오기
        for word in s:                  # 비교할 입력 단어
            for key_index in range(len(d)):    # 사전 key 에 접근하기 위함
                # 대소문자 구분하지않고 사전에 있는 단어에 입력단어가 포함돼있으면 가장 유사한 것으로 간주하여 3점을 준다.
                if word.lower() in list(d.keys())[key_index]:    # 사전의 단어에 직접접근한다.
                    similar[index] += (d[list(d.keys())[key_index]]) * 2   # 키값(빈도수)을 점수로 준다.
        index += 1
    return similar


def similarity_plus(s, dictionary, similar):
    index = 0                           # url 순서
    for d in dictionary:                # url 순서대로 사전 불러오기
        for word in s:                  # 비교할 입력 단어
            for key_index in range(len(d)):    # 사전 key 에 접근하기 위함
                # 입력단어의 두글자조합이 사전에 있는 단어에 포함돼있으면 유사한 단어로 간주하여 1점을 준다.
                # (예 - 입력단어: 비밀번호, 비밀/밀번/번호으로 검색)
                for two in range(len(word) - 1): # 입력단어를 두글자씩 묶은 조합
                    if word.lower()[two:two+2] in list(d.keys())[key_index]:    # 사전의 단어에 직접접근한다.
                        similar[index] += d[list(d.keys())[key_index]]    # 키값(빈도수)을 점수로 준다.
        index += 1
    return similar


def similarity_abbreviation(s, dictionary, similar):
    index = 0
    for d in dictionary:              # url 순서대로 사전 불러오기
        for word in s:       # 비교할 입력 단어
            for key_index in range(len(d)):    # 사전 key 에 접근하기 위함
                # 입력단어의 모든 글자가 사전 단어안에 존재하면 줄임말로 간주하여 점수를 2점 준다.
                for abb in word:
                    if abb.lower() not in list(d.keys())[key_index]:   # 한 글자라도 없으면 줄임말이 아니다.
                        break
                    else:
                        if abb == word[len(word) - 1]:  # 마지막 글자까지 통과하면 줄임말로 간주하고 2점을 준다.
                            similar[index] += d[list(d.keys())[key_index]] * 2    # 키값(빈도수)을 점수로 준다.
        index += 1
    return similar


# ASSIGNMENT 5
class SearchEngine:
    def __init__(self, *args):      # 가변인수로 url을 받는 생성자
        self.source = list()  # url을 저장하는 리스트
        self.word = list()  # 단어를 저장하는 리스트
        self.freq_dict = dict()  # 빈도수를 저장하는 딕셔너리
        for url in args:
            self.source.append(url)

    def addUrl(self, url):          # addUrl 함수
        self.source.append(url)

    def removeUrl(self, url):       # removeUrl 함수
        if url in self.source:
            self.source.remove(url)

    def listUrls(self):             # listUrls 함수
        for url in self.source:
            print(url)

    @staticmethod
    def getwords(url):              # staticmethod로 url을 인자로 받아 url의 소스코드를 가져온다.
        return requests.get(url).text

    def getWordsFrequency(self):    # 클래스내의 url의 모든 단어 출현 빈도 사전
        for url in self.source:     # 스태틱메소드를 호출하여 word 리스트에 모든 단어를 담는다.
            self.word += pure_word_list(self.getwords(url).lower())     # 구두문자와 불용어가 삭제된 소문자 단어 리스트
        for key in self.word:
            if self.freq_dict.get(key):
                self.freq_dict[key] += 1
            else:
                self.freq_dict[key] = 1
        return print(self.freq_dict)

    def getMaxFrequencyWords(self):
        most = dict()
        if self.freq_dict.values():                         # 딕셔너리가 비었는지 확인
            m = max(self.freq_dict.values())                # value 값중에서 최대값 저장
        else:                                               # 등록된 URL이 없는 경우
            return None
        count = list(self.freq_dict.values()).count(m)      # 최대값을 가지는 value 개수 저장
        for n in range(count):                              # 최대값의 개수 만큼 반복
            for key, value in self.freq_dict.items():       # 해당 value값의 key값이 필요
                if value == m:  # value와 최대값 비교
                    most.update({key: self.freq_dict.get(key)})  # key 값인 단어와 value 값인 개수 저장)
        return print(most)

    def searchUrlByWord(self, search):                  # 유사도 Url
        each_freq = list()                                    # 각각의 Url에 대한 출현빈도 딕셔너리를 담은 리스트
        for i in range(len(self.source)):
            each_dictionary = dict()                    # 각각의 Url에 대한 딕셔너리
            for key in pure_word_list(self.getwords(self.source[i]).lower()):
                if each_dictionary.get(key):
                    each_dictionary[key] += 1
                else:
                    each_dictionary[key] = 1
            each_freq.append(each_dictionary)           # each_freq 리스트원소는 각각의 url에 대한 출현빈도 사전

        for s in search.split():                        # 유사도 검사 단어 불용어 처리
            if s.lower() in stopwords:                  # 입력단어 불용어 처리
                search = search.replace(s, '')
        search = search.split()                         # 입력단어 배열화

        similar = [0] * len(self.source)                # 해당 사이트의 유사도를 알려주는 리스트
        similarity_base(search, each_freq, similar)
        similarity_plus(search, each_freq,  similar)
        similarity_abbreviation(search, each_freq, similar)
        if similar:                                     # URL이 있는 경우
            for n in range(similar.count(max(similar))):            # 유사도가 같은 URL이 있으면 모두 출력
                print(self.source[similar.index(max(similar))])     # 해당 URL 출력
        else:                                           # URL이 없는 경우
            return None


if __name__ == '__main__':
    w1 = SearchEngine('http://www.cnn.com', 'https://www.amazon.com')
    w2 = SearchEngine('http://www.youtube.com', 'https://www.daum.net')
    w1.getWordsFrequency()
    w1.getMaxFrequencyWords()
    w2.getWordsFrequency()
    w2.getMaxFrequencyWords()
    w1.searchUrlByWord("news")
    w2.searchUrlByWord("news")
