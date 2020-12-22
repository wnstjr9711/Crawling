import string
import pickle
from stop import *

s = ["https://www.github.com",
     "http://www.google.com",
     "http://www.naver.com",
     "http://www.youtube.com",
     "http://www.nytimes.com",
     "https://www.daum.net"]

source_1 = requests.get(s[0]).text
source_2 = requests.get(s[1]).text
source_3 = requests.get(s[2]).text
source_4 = requests.get(s[3]).text
source_5 = requests.get(s[4]).text
source_6 = requests.get(s[5]).text


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


# 구두문자 삭제
def delete_punctuation(raw_list):
    x = raw_list
    for p in string.punctuation:
        x = ' '.join(x).split(p)
    x = ''.join(x).split()
    return x


# 순수 단어 리스트 반환
def pure_word_list(source):
    return delete_punctuation(remove_tag(source))


# 리스트 원소 개수 반환
def count_word(source):     # 개수와 단어 샘플 15개 출력
    count = pure_word_list(source)
    word_example = count[:15] + [...]
    return print('단어 샘플:{}\n단어 개수{}'.format(word_example, len(count)))


# 단어와 빈도수를 저장한 사전
def word_dictionary(source):
    word_list = pure_word_list(source)
    dictionary = dict()
    for word in word_list:
        word = word.lower()     # 모두 소문자로 저장
        if dictionary.get(word):
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary


# assignment4
def remove_stopwords(dictionary):    # 사전에서 불용어 제거코드
    return_dict = dictionary.copy()  # 사전 복사
    for w in dictionary:
         if w in stopwords:
            return_dict.pop(w)
    return return_dict


def pure_dictionary(source):
    return remove_stopwords(word_dictionary(source))


print(s[0])
print('불용어 삭제 후: ', pure_dictionary(source_1))

print(s[1])
print('불용어 삭제 후: ', pure_dictionary(source_2))

print(s[2])
print('불용어 삭제 후: ', pure_dictionary(source_3))

print(s[3])
print('불용어 삭제 후: ', pure_dictionary(source_4))

print(s[4])
print('불용어 삭제 후: ', pure_dictionary(source_5))

print(s[5])
print('불용어 삭제 후: ', pure_dictionary(source_6))

# 피클 모듈 이용하여 파일 저장
for i in s:     # url 을 담은 s 배열 호출
    with open(i[i.index('//') + 2:] + '.html', 'w', encoding="utf-8") as f:     # encoding='utf-8'-> request 시 오류해결
        f.write(requests.get(i).text)   # url source 저장
    with open(i[i.index('//') + 2:] + '.words_frequency.pickle', 'wb') as f:
        pickle.dump(pure_dictionary(requests.get(i).text), f)     # url 단어 사전 피클저장

pickle_dict = list()    # 불러오는 피클된 사전을 저장하는 리스트
for j in s:     # url 을 담은 s 배열 호출
    with open(j[j.index('//') + 2:] + '.words_frequency.pickle', 'rb') as f:
        pickle_dict.append(pickle.load(f))   # 불러온 피클 사전을 리스트에 전달


# 가장 많이 나온 단어 3개 뽑는 함수
def get_most_3(pickled):
    dict_x = pickled.copy()     # 피클 사전 복사
    count = 0   # 3개를 카운트
    most = list()   # 많이나온 단어 3개씩 차례대로 저장하는 리스트
    while True:
        for key, value in dict_x.items():
            if value == max(dict_x.values()):   # value 값중에서 최대값 찾기
                most.append((key, dict_x.pop(key)))     # key 값인 단어와 value 값인 개수 저장
                count += 1
                if count == 3:  # 3개가 되면 return
                    return print('1위:{}, 2위{}, 3위{}'.format(most[0], most[1], most[2]))
                break


# 피클 사전 개수(url 개수) 만큼 실행
for k in range(len(pickle_dict)):
    print('{:<30} 에서 가장 많이 나온 단어:\t' .format(s[k]), end='')
    get_most_3(pickle_dict[k])


def similarity():
    # 유사도 사이트를 검색할 단어 입력
    input_word_ = input('1개이상의 단어 입력:\t')
    for iw in input_word_.split():
        if iw.lower() in stopwords:     # 입력단어 불용어 처리
            input_word_ = input_word_.replace(iw, '')
    input_word_ = input_word_.split()   # 입력단어 배열화
    print('유사도')
    similar = [0] * len(s)              # 사이트에 해당하는 배열
    similarity_base(input_word_, similar)
    similarity_plus(input_word_, similar)
    similarity_abbreviation(input_word_, similar)

    def get_count(a):       # 정렬 시 유사도 점수를 기준으로 정렬
        return a[1]
    return sorted(tuple(zip(s, similar)), key=get_count, reverse=True)  # url 과 유사도를 zip함수로 묶고 tuple로 반환


# 유사도 계산 기본 함수(추출된 단어 빈도를 기준으로 계산)
def similarity_base(input_word, similar):
    index = 0                           # url 순서
    for pd in pickle_dict:              # url 순서대로 사전 불러오기
        for search in input_word:       # 비교할 입력 단어
            for key_index in range(len(pd)):    # 사전 key 에 접근하기 위함
                # 대소문자 구분하지않고 사전에 있는 단어에 입력단어가 포함돼있으면 가장 유사한 것으로 간주하여 3점을 준다.
                if search.lower() in list(pd.keys())[key_index]:    # 사전의 단어에 직접접근한다.
                    similar[index] += (pd[list(pd.keys())[key_index]]) * 2   # 키값(빈도수)을 점수로 준다.
        index += 1
    return similar


def similarity_plus(input_word, similar):
    index = 0                           # url 순서
    for pd in pickle_dict:              # url 순서대로 사전 불러오기
        for search in input_word:       # 비교할 입력 단어
            for key_index in range(len(pd)):    # 사전 key 에 접근하기 위함
                # 입력단어의 두글자조합이 사전에 있는 단어에 포함돼있으면 유사한 단어로 간주하여 1점을 준다.
                # (예 - 입력단어: 비밀번호, 비밀/밀번/번호으로 검색)
                for two in range(len(search) - 1): # 입력단어를 두글자씩 묶은 조합
                    if search.lower()[two:two+2] in list(pd.keys())[key_index]:    # 사전의 단어에 직접접근한다.
                        similar[index] += pd[list(pd.keys())[key_index]]    # 키값(빈도수)을 점수로 준다.
        index += 1
    return similar


def similarity_abbreviation(input_word, similar):
    index = 0
    for pd in pickle_dict:              # url 순서대로 사전 불러오기
        for search in input_word:       # 비교할 입력 단어
            for key_index in range(len(pd)):    # 사전 key 에 접근하기 위함
                # 입력단어의 모든 글자가 사전 단어안에 존재하면 줄임말로 간주하여 점수를 2점 준다.
                for abb in search:
                    if abb.lower() not in list(pd.keys())[key_index]:   # 한 글자라도 없으면 줄임말이 아니다.
                        break
                    else:
                        if abb == search[len(search) - 1]:  # 마지막 글자까지 통과하면 줄임말로 간주하고 2점을 준다.
                            similar[index] += pd[list(pd.keys())[key_index]] * 2    # 키값(빈도수)을 점수로 준다.
        index += 1
    return similar


print(similarity())
print(similarity())
print(similarity())
print(similarity())
print(similarity())
