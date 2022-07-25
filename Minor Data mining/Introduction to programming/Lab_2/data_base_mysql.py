import re
import nltk
from nltk.corpus import stopwords
from stop_words import get_stop_words

import pymysql
from pymysql.cursors import DictCursor

from timeit import default_timer as timer
# nltk.download('stopwords')


start = timer()
file = open('data.txt', 'r', encoding='utf-8-sig')


def extra_stopwords():  # Наш собственный лист стоп-слов, который формируется на протяжении всей работы
    file = open('additional_stopwords.txt', 'r', encoding='utf-8')
    additional_list = []
    for line in file:
        additional_list.append(line[:-1].lower())
    file.close()
    return additional_list


surnames1 = []
connection = pymysql.connect(user='root',
                             password='A5467392',
                             host='localhost',
                             database='russian_surnames',
                             cursorclass=DictCursor)
try:
    with connection.cursor() as cursor:
        for line in file:
            line = re.sub(r'http(?:s)?://[^\s<>"]+|www\.[^\s<>"]+|pic.twitter.com/[^\s<>"]+', '', str(line),
                          flags=re.IGNORECASE)  # Ищем по заданному шаблону весь ссылочный мусор, часть [^\s<>"] соответствует символу non-whitespace, non quote, non anglebracket, чтобы избежать совпадения строк
            date = re.findall(r'\d\d\d\d-\d\d-\d\d+|\d\d:\d\d+', str(line))
            re_tweets = re.findall(r'(?:RT )*@+ *[^\s<>"а-яёА-ЯЁ]+', str(line))
            strong_language = re.findall(  # Обработка "крепких" выражений
                r'[^\sa-zа-яё#$%&@]*[^\s]*(?:[a-zа-яё])*[^\s]+[#$%&@]+[^\s]+(?:[a-zа-яё])*[^\s]*[^\sa-zа-яё#$%&@]*',
                str(line), flags=re.IGNORECASE)
            for i in range(0, len(re_tweets)):
                line = line.replace(re_tweets[i], '')
            my_list = line.split()
            for j in range(0, len(my_list)):
                for i in range(0, len(strong_language)):
                    if strong_language[i] == my_list[j]:
                        my_list[j] = re.compile('[#$%&@]', flags=re.IGNORECASE).sub('*', strong_language[i])
            if len(my_list) == 0:
                continue
            else:
                tokens = list(nltk.word_tokenize(re.sub('[^a-zа-яё* ]+', '', ' '.join(my_list), flags=re.IGNORECASE)))
                stop_list = list(set(stopwords.words('russian') + get_stop_words('russian') + extra_stopwords()))
                filtered_words = [word for word in tokens if word.lower() not in stop_list]
                surnames = re.findall(r'[А-ЯЁ]+[a-zа-яё]+(?:ов|ев|ын|ин|ер|ский|ес|к'
                                      r'|ко|ий|ич|ек|ан|ар|ия|а)[^a-zA-Zа-яёА-ЯЁ]', ' '.join(filtered_words))
                if len(surnames) == 0:
                    continue
                else:
                    for s in range(0, len(surnames)):
                        if surnames[s] not in surnames1:
                            query = """SELECT Surname FROM russian_surnames WHERE Surname = %s"""
                            cursor.execute(query, (surnames[s]))
                            for row in cursor:
                                surnames1.append(surnames[s])
                                with open('surnames_in_tweets.txt', 'a', encoding='utf8') as surnames_file:
                                    surnames_file.write(surnames[s] + '\n')
finally:
    connection.close()

end = timer()
execTime = end - start
print(execTime)

# Время: 1384.0781405999999
# Количество: 161
# Обработано до 83
