import re
import nltk
import math
import datetime
import pymorphy2
import numpy as np
from nltk.corpus import stopwords
from stop_words import get_stop_words
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib import style
import matplotlib.font_manager as font_manager
from sklearn.feature_extraction.text import CountVectorizer

from timeit import default_timer as timer

morph = pymorphy2.MorphAnalyzer()
vectorizer = CountVectorizer()
file = open('data.txt', 'r', encoding='utf-8-sig')


# nltk.download('stopwords')


class Lab:

    def __init__(self):
        self.tweets_dict = {}  # Хранит словарь; ключ: дата, значение: список слов в твите
        self.words_in_tweets = {}  # Хранит отсортированный словарь; ключ: слово, значение: число твитов, содер-х слово
        self.length_of_tweet = {}  # Хранит отсортированный словарь; ключ: длина твита, значение: число твитов с этой длиной
        self.estimation_book = {}  # Хранит отсорт-й по частоте встречаемости (от наиболее встречаемого к наименее) словарь; ключ: слово, значение: оценка тональности
        self.tweets_dict_tonality = {}  # Хранит словарь; ключ: дата, значение: список оценок тональности слов из значений словаря tweets_dict

        self.first_rule_tweets = {}
        self.second_rule_tweets = {}
        self.third_rule_tweets = {}
        self.fourth_rule_tweets = {}

        self.first_rule = []
        self.second_rule = []
        self.third_rule = []
        self.fourth_rule = []

        self.top5_positive_adj = {}
        self.top5_neutral_adj = {}
        self.top5_negative_adj = {}

        self.classification_label_r1 = []
        self.classification_pos_r1 = []
        self.classification_neu_r1 = []
        self.classification_neg_r1 = []
        self.classification_sum_r1 = []

        self.classification_label_r2 = []
        self.classification_pos_r2 = []
        self.classification_neu_r2 = []
        self.classification_neg_r2 = []
        self.classification_sum_r2 = []

        self.classification_label_r3 = []
        self.classification_pos_r3 = []
        self.classification_neu_r3 = []
        self.classification_neg_r3 = []
        self.classification_sum_r3 = []

        self.classification_label_r4 = []
        self.classification_pos_r4 = []
        self.classification_neu_r4 = []
        self.classification_neg_r4 = []
        self.classification_sum_r4 = []

    def extra_stopwords(self):  # Наш собственный лист стоп-слов, который формируется на протяжении всей работы
        file = open('additional_stopwords.txt', encoding='utf-8')
        additional_list = []
        for line in file:
            additional_list.append(line[:-1].lower())
        file.close()
        return additional_list

    def surnames_in_tweets(self):
        file = open('surnames_in_tweets.txt', encoding='utf-8')
        surnames_list = []
        for line in file:
            surnames_list.append(line[:-1].lower())
        file.close()
        return surnames_list

    def filtered_data(self):
        number = 1
        for line in file:
            date = re.findall(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d+', str(line))
            line = re.sub(r'http(?:s)?://[^\s<>"]+|www\.[^\s<>"]+|pic.twitter.com/[^\s<>"]+', '', str(line),
                          flags=re.IGNORECASE)  # символу non-whitespace, non quote, non anglebracket, чтобы избежать совпадения строк
            line = re.sub(r'(?:RT )*@+ *[^\s<>"а-яёА-ЯЁ]+', '', str(line), flags=re.IGNORECASE)
            line = re.sub(r'([a-zа-яё])\1+(?=\1)+', '', str(line), flags=re.IGNORECASE)
            line = re.sub(r'чемпионатмирапофутболу+', 'чемпионат мира по футболу', str(line), flags=re.IGNORECASE)
            line = re.sub(r'чемпионатмира+', 'чемпионат мира', str(line), flags=re.IGNORECASE)
            line = re.sub(r'спасибозаборьбу+', 'спасибо за борьбу', str(line), flags=re.IGNORECASE)
            line = re.sub(r'славаукраине+', 'слава украине', str(line), flags=re.IGNORECASE)
            line = re.sub(r'футболжив+', 'футбол жив', str(line), flags=re.IGNORECASE)
            line = re.sub(r'бразилиябельгия+', 'бразилия бельгия', str(line), flags=re.IGNORECASE)
            strong_language = re.findall(
                r'[^\sa-zа-яё#$%&@]*[^\s]*(?:[a-zа-яё])*[^\s]+[#$%&@]+[^\s]+(?:[a-zа-яё])*[^\s]*[^\sa-zа-яё#$%&@]*',
                str(line), flags=re.IGNORECASE)
            for d in range(0, len(date)):
                line = line.replace(date[d], '')
            my_list = line.split()
            if len(my_list) == 0:
                continue
            else:
                for j in range(0, len(my_list)):
                    for st in range(0, len(strong_language)):
                        if strong_language[st] == my_list[j]:
                            my_list[j] = re.compile('[#$%&@]', flags=re.IGNORECASE).sub('@', strong_language[st])

                tokens = nltk.word_tokenize(re.sub('[^-a-zа-яё@ ]+', ' ', ' '.join(my_list), flags=re.IGNORECASE))
                stop_list = stopwords.words('russian') + get_stop_words('russian') + self.extra_stopwords() + \
                            self.surnames_in_tweets() + stopwords.words('english')
                ne_constructions = []
                ind = len(tokens) - 1
                while ind >= 0:
                    if tokens[ind] not in stop_list:
                        if tokens[ind - 1].lower() == 'не':
                            ne_constructions.append('не {}'.format(morph.parse(tokens[ind])[0].normal_form))
                            tokens.remove(tokens[ind])
                            ind -= 2
                        else:
                            ind -= 1
                    else:
                        ind -= 1
                surnames = list(set(' '.join(tokens).lower().split()) & set(self.surnames_in_tweets()))
                filtered_words = [word for word in tokens if word.lower() not in stop_list]
                if len(filtered_words) == 0:
                    continue
                else:
                    for f in range(0, len(filtered_words)):
                        filtered_words[f] = morph.parse(filtered_words[f])[0].normal_form
                    for s in range(0, len(surnames)):
                        filtered_words.append(surnames[s].title())
                    filtered_words.extend(ne_constructions)
                    # with open('filtered_data.txt', 'a', encoding='utf-8') as filtered_data:
                    #     filtered_data.write(' '.join(filtered_words) + '\n')
                    self.tweets_dict['{} {}'.format(date[0], number)] = filtered_words
                    number += 1

    def frequency_length(self):
        filtered_data = open('filtered_data.txt', 'r', encoding='utf-8')
        word_list = []

        for line in filtered_data:
            line = re.sub(r'не +', '', str(line), flags=re.IGNORECASE)
            word_list.append(str(line[:-1]))

        count_words_in_tweets = np.array(vectorizer.fit_transform(word_list).todense())
        word_dict = list(dict(sorted(vectorizer.vocabulary_.items(), key=lambda x: x[0])))
        # print(count_words_in_tweets)
        # print(word_dict)

        # Считаем количество твитов, в которых встречается каждое слово хотя бы 1 раз
        for i in range(0, count_words_in_tweets.shape[1]):
            count = len(list(count_words_in_tweets[:, i])) - list(count_words_in_tweets[:, i]).count(0)
            self.words_in_tweets[word_dict[i]] = count

        self.words_in_tweets = dict(sorted(self.words_in_tweets.items(), key=lambda x: -x[1]))
        # print(self.words_in_tweets)

        # for k, v in self.words_in_tweets.items():
        #     percentage = (v * 100) / 10000
        #     with open('frequency.txt', 'a', encoding='utf-8') as frequency:
        #         frequency.write('{} - {} - {}%\n'.format(k, v, percentage))
        #     with open('estimations.txt', 'a', encoding='utf-8') as estimations:
        #         estimations.write('{} \n'.format(k))

        lengths_of_tweets = []

        for j in range(0, count_words_in_tweets.shape[0]):
            count = sum(count_words_in_tweets[j, :])
            lengths_of_tweets.append(count)

        for count in lengths_of_tweets:
            if count in self.length_of_tweet:
                self.length_of_tweet[count] += 1
            else:
                self.length_of_tweet[count] = 1

        zero_tweets = 10000 - sum(list(self.length_of_tweet.values()))
        self.length_of_tweet[0] += zero_tweets
        self.length_of_tweet = dict(sorted(self.length_of_tweet.items(), key=lambda x: -x[1]))
        # print(self.length_of_tweet)

        # for k, v in self.length_of_tweet.items():
        #     percentage = (v * 100) / 10000
        #     with open('tweets_length.txt', 'a', encoding='utf-8') as tweets_length:
        #         tweets_length.write('{} - {} - {}%\n'.format(k, v, percentage))

    def classification_rules(self):
        with open('estimations.txt', 'r', encoding='utf-8') as estimations:
            for line in estimations:
                try:
                    l = line.split()
                    self.estimation_book[l[0]] = int(l[1])
                except ValueError:
                    self.estimation_book[l[0]] = -1
                    continue
                except IndexError:
                    continue

        # print(self.estimation_book)

        for key, value in self.tweets_dict.items():
            value_list = []
            for i in range(0, len(value)):
                ne_cons = value[i].split(' ')
                if ne_cons[0] == 'не':
                    for k, v in self.estimation_book.items():
                        if ne_cons[1] == k:
                            value_list.append(-v)
                            break
                else:
                    c = 0
                    for k, v in self.estimation_book.items():
                        if value[i] == k:
                            value_list.append(v)
                            c += 1
                            break
                    if c == 0:
                        value_list.append(0)
            self.tweets_dict_tonality[key] = value_list

        # print(self.tweets_dict_tonality)

        def first_rule():
            positive = 0
            neutral = 0
            negative = 0

            for key, value in self.tweets_dict_tonality.items():
                average = (sum(value)) / len(value)
                if 1 / 3 < average <= 1:
                    positive += 1
                    self.first_rule_tweets[key] = 1
                elif -(1 / 3) <= average <= (1 / 3):
                    neutral += 1
                    self.first_rule_tweets[key] = 0
                elif -1 <= average < -(1 / 3):
                    negative += 1
                    self.first_rule_tweets[key] = -1

            self.first_rule.append(positive)
            self.first_rule.append(neutral)
            self.first_rule.append(negative)

            positive_percentage = round((positive * 100) / len(self.tweets_dict), 2)
            neutral_percentage = round((neutral * 100) / len(self.tweets_dict), 2)
            negative_percentage = round((negative * 100) / len(self.tweets_dict), 2)

            with open('classifications.txt', 'a', encoding='utf-8') as classification:
                classification.write('The first rule. The arithmetic mean threshold classification:\n')
                classification.write('Positive - {} - {}%\n'.format(positive, positive_percentage))
                classification.write('Neutral - {} - {}%\n'.format(neutral, neutral_percentage))
                classification.write('Negative - {} - {}%\n\n'.format(negative, negative_percentage))

        def second_rule():
            positive = 0
            neutral = 0
            negative = 0

            for key, value in self.tweets_dict_tonality.items():
                positive_v = value.count(1)
                neutral_v = value.count(0)
                negative_v = value.count(-1)

                maximum = max(positive_v, neutral_v, negative_v)

                if maximum == positive_v and maximum != neutral_v and maximum != negative_v:
                    positive += 1
                    self.second_rule_tweets[key] = 1
                elif maximum == neutral_v and maximum != positive_v and maximum != negative_v:
                    neutral += 1
                    self.second_rule_tweets[key] = 0
                elif maximum == negative_v and maximum != positive_v and maximum != neutral_v:
                    negative += 1
                    self.second_rule_tweets[key] = -1
                elif maximum == positive_v and maximum == neutral_v and maximum != negative_v:
                    positive += 1
                    self.second_rule_tweets[key] = 1
                elif maximum == positive_v and maximum == negative_v and maximum != neutral_v:
                    neutral += 1
                    self.second_rule_tweets[key] = 0
                elif maximum == neutral_v and maximum == negative_v and maximum != positive_v:
                    negative += 1
                    self.second_rule_tweets[key] = -1
                elif maximum == neutral_v and maximum == negative_v and maximum == positive_v:
                    neutral += 1
                    self.second_rule_tweets[key] = 0

            self.second_rule.append(positive)
            self.second_rule.append(neutral)
            self.second_rule.append(negative)

            positive_percentage = round((positive * 100) / len(self.tweets_dict), 2)
            neutral_percentage = round((neutral * 100) / len(self.tweets_dict), 2)
            negative_percentage = round((negative * 100) / len(self.tweets_dict), 2)

            with open('classifications.txt', 'a', encoding='utf-8') as classification:
                classification.write('The second rule. '
                                     'The classification by the proportion of words of each type in tweets:\n')
                classification.write('Positive - {} - {}%\n'.format(positive, positive_percentage))
                classification.write('Neutral - {} - {}%\n'.format(neutral, neutral_percentage))
                classification.write('Negative - {} - {}%\n\n'.format(negative, negative_percentage))

        def third_rule():
            positive = 0
            neutral = 0
            negative = 0

            for k, v in self.tweets_dict.items():
                value_ton_dict = {}
                for i in range(0, len(v)):
                    a1 = v.count(v[i].lower())
                    a2 = len(v)
                    a3 = len(self.tweets_dict)
                    try:
                        if v[i].lower().split()[0] == 'не':
                            a4 = self.words_in_tweets.get(v[i].lower().split()[1])
                        else:
                            a4 = self.words_in_tweets.get(v[i].lower())

                        tf_idf = (int(a1) / int(a2)) * math.log10(int(a3) / int(a4))
                        rate = self.estimation_book.get(v[i])
                        value_ton_dict[tf_idf] = rate
                    except TypeError:
                        continue

                pos = 0
                neu = 0
                neg = 0

                for key, value in value_ton_dict.items():
                    if value == 1:
                        pos += key
                    elif value == 0:
                        neu += key
                    elif value == -1:
                        neg += key

                maximum = max(pos, neu, neg)

                if maximum == pos and maximum != neu and maximum != neg:
                    positive += 1
                    self.third_rule_tweets[k] = 1
                elif maximum == neu and maximum != pos and maximum != neg:
                    neutral += 1
                    self.third_rule_tweets[k] = 0
                elif maximum == neg and maximum != pos and maximum != neu:
                    negative += 1
                    self.third_rule_tweets[k] = -1
                elif maximum == pos and maximum == neu and maximum != neg:
                    positive += 1
                    self.third_rule_tweets[k] = 1
                elif maximum == pos and maximum == neg and maximum != neu:
                    neutral += 1
                    self.third_rule_tweets[k] = 0
                elif maximum == neu and maximum == neg and maximum != pos:
                    negative += 1
                    self.third_rule_tweets[k] = -1
                elif maximum == neu and maximum == neg and maximum == pos:
                    neutral += 1
                    self.third_rule_tweets[k] = 0

            self.third_rule.append(positive)
            self.third_rule.append(neutral)
            self.third_rule.append(negative)

            positive_percentage = round((positive * 100) / len(self.tweets_dict), 2)
            neutral_percentage = round((neutral * 100) / len(self.tweets_dict), 2)
            negative_percentage = round((negative * 100) / len(self.tweets_dict), 2)

            with open('classifications.txt', 'a', encoding='utf-8') as classification:
                classification.write('The third rule. '
                                     'The classification based on the TF-IDF metric:\n')
                classification.write('Positive - {} - {}%\n'.format(positive, positive_percentage))
                classification.write('Neutral - {} - {}%\n'.format(neutral, neutral_percentage))
                classification.write('Negative - {} - {}%\n\n'.format(negative, negative_percentage))

        def fourth_rule():
            positive = 0
            neutral = 0
            negative = 0

            for key, value in self.tweets_dict_tonality.items():
                average = sum(value)
                i = 1
                while i < len(value):
                    if value[i] == 1:
                        for k, v in self.tweets_dict.items():
                            if k == key:
                                word = morph.parse(v[i])[0]
                                if str(word.tag.POS) == 'NOUN' or str(word.tag.POS) == 'VERB' or str(
                                        word.tag.POS) == 'INFN':
                                    word1 = morph.parse(v[i - 1])[0]
                                    if str(word1.tag.POS) == 'ADJF' or str(word1.tag.POS) == 'ADJS' or str(
                                            word1.tag.POS) == 'COMP' or str(word1.tag.POS) == 'NUMR' or str(
                                            word1.tag.POS) == 'ADVB':
                                        if value[i - 1] == 0:
                                            average += 1
                                            if i > 1:
                                                word2 = morph.parse(v[i - 2])[0]
                                                if str(word2.tag.POS) == 'ADJF' or str(word2.tag.POS) == 'ADJS' or str(
                                                        word2.tag.POS) == 'COMP' or str(word2.tag.POS) == 'PRTF' or str(
                                                        word2.tag.POS) == 'PRTS' or str(word2.tag.POS) == 'NUMR' or str(
                                                        word2.tag.POS) == 'ADVB':
                                                    if value[i - 2] == 0:
                                                        average += 1
                                                        i += 2
                                                else:
                                                    i += 2
                                            else:
                                                i += 2
                                        else:
                                            i += 2
                                    else:
                                        i += 1
                                else:
                                    i += 1
                                i += 1

                    elif value[i] == -1:
                        for k, v in self.tweets_dict.items():
                            if k == key:
                                word = morph.parse(v[i])[0]
                                if str(word.tag.POS) == 'NOUN' or str(word.tag.POS) == 'VERB' or str(
                                        word.tag.POS) == 'INFN':
                                    word1 = morph.parse(v[i - 1])[0]
                                    if str(word1.tag.POS) == 'ADJF' or str(word1.tag.POS) == 'ADJS' or str(
                                            word1.tag.POS) == 'COMP' or str(word1.tag.POS) == 'NUMR' or str(
                                            word1.tag.POS) == 'ADVB':
                                        if value[i - 1] == 0:
                                            average += -1
                                            if i > 1:
                                                word2 = morph.parse(v[i - 2])[0]
                                                if str(word2.tag.POS) == 'ADJF' or str(word2.tag.POS) == 'ADJS' or str(
                                                        word2.tag.POS) == 'COMP' or str(word2.tag.POS) == 'PRTF' or str(
                                                        word2.tag.POS) == 'PRTS' or str(word2.tag.POS) == 'NUMR' or str(
                                                        word2.tag.POS) == 'ADVB':
                                                    if value[i - 2] == 0:
                                                        average += -1
                                                        i += 2
                                                else:
                                                    i += 2
                                            else:
                                                i += 2
                                        else:
                                            i += 2
                                    else:
                                        i += 1
                                else:
                                    i += 1
                                i += 1

                    elif value[i] == 0:
                        i += 1

                average1 = average / len(value)
                if 1 / 3 < average1 <= 1:
                    positive += 1
                    self.fourth_rule_tweets[key] = 1
                elif -(1 / 3) <= average1 <= (1 / 3):
                    neutral += 1
                    self.fourth_rule_tweets[key] = 0
                elif -1 <= average1 < -(1 / 3):
                    negative += 1
                    self.fourth_rule_tweets[key] = -1

            # print(self.fourth_rule_tweets)

            self.fourth_rule.append(positive)
            self.fourth_rule.append(neutral)
            self.fourth_rule.append(negative)

            positive_percentage = round((positive * 100) / len(self.tweets_dict), 2)
            neutral_percentage = round((neutral * 100) / len(self.tweets_dict), 2)
            negative_percentage = round((negative * 100) / len(self.tweets_dict), 2)

            with open('classifications.txt', 'a', encoding='utf-8') as classification:
                classification.write('The fourth rule. The arithmetic classification with the amplification'
                                     ' of tonality due to auxiliary words:\n')
                classification.write('Positive - {} - {}%\n'.format(positive, positive_percentage))
                classification.write('Neutral - {} - {}%\n'.format(neutral, neutral_percentage))
                classification.write('Negative - {} - {}%\n\n'.format(negative, negative_percentage))

        first_rule()
        second_rule()
        third_rule()
        fourth_rule()

        # print(self.first_rule_tweets)
        # print(self.second_rule_tweets)
        # print(self.third_rule_tweets)
        # print(self.fourth_rule_tweets)

    def classification_rules_barplots(self):

        labels = ['Positive', 'Neutral', 'Negative']

        x = np.arange(len(labels))
        width = 0.2

        fig, ax = plt.subplots()
        rule1 = ax.bar(x - (width*3)/2, self.first_rule, width, label='First rule', color='darkblue', alpha=0.9)
        rule2 = ax.bar(x - width/2, self.second_rule, width, label='Second rule', color='slateblue')
        rule3 = ax.bar(x + width/2, self.third_rule, width, label='Third rule', color='mediumorchid')
        rule4 = ax.bar(x + (width*3)/2, self.fourth_rule, width, label='Fourth rule', color='plum')

        font_t = {'fontname': 'montserrat', 'size': '14', 'color': 'black', 'weight': 'medium',
                  'verticalalignment': 'bottom'}
        font_o = {'fontname': 'montserrat', 'size': '9', 'color': 'black', 'weight': 'light'}

        font_path = 'C:\\Users\\paxom\\Documents\\ноВШЭсти\\Шрифты\\Montserrat&FiraSans\\Montserrat-Light.ttf'
        font_prop = font_manager.FontProperties(fname=font_path, size=11)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('The amount of tweets', font_o)
        ax.set_title('The classification of tweets by tonality according to rules', **font_t)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, **font_o)
        ax.legend(prop=font_prop)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', size=9)

        autolabel(rule1)
        autolabel(rule2)
        autolabel(rule3)
        autolabel(rule4)

        fig.tight_layout()

        plt.show()

    def top5_adjectives(self):
        count_pos = 0
        count_neu = 0
        count_neg = 0

        for key, value in self.estimation_book.items():
            word = morph.parse(key)[0]
            if str(word.tag.POS) == 'ADJF' or str(word.tag.POS) == 'ADJS':
                if value == 1:
                    if count_pos < 5:
                        count_pos += 1
                        self.top5_positive_adj[key] = self.words_in_tweets.get(key)
                    else:
                        continue
                elif value == 0:
                    if count_neu < 5:
                        count_neu += 1
                        self.top5_neutral_adj[key] = self.words_in_tweets.get(key)
                    else:
                        continue
                elif value == -1:
                    if count_neg < 5:
                        count_neg += 1
                        self.top5_negative_adj[key] = self.words_in_tweets.get(key)
                    else:
                        continue
                if count_pos == 5 and count_neu == 5 and count_neg == 5:
                    break

        # print(self.top5_positive_adj)
        # print(self.top5_neutral_adj)
        # print(self.top5_negative_adj)

        with open('adjectives.txt', 'a', encoding='utf-8') as adjectives:
            adjectives.write('TOP-5 Positive:\n')
            for k, v in self.top5_positive_adj.items():
                percentage = (v * 100) / 10000
                adjectives.write('{} - {} - {}%\n'.format(k, v, percentage))

            adjectives.write('\nTOP-5 Neutral:\n')
            for k, v in self.top5_neutral_adj.items():
                percentage = (v * 100) / 10000
                adjectives.write('{} - {} - {}%\n'.format(k, v, percentage))

            adjectives.write('\nTOP-5 Negative:\n')
            for k, v in self.top5_negative_adj.items():
                percentage = (v * 100) / 10000
                adjectives.write('{} - {} - {}%\n'.format(k, v, percentage))

    def top5_adjectives_barplot(self):
        labels_pos = []
        labels_neu = []
        labels_neg = []

        means_pos = []
        means_neu = []
        means_neg = []

        for k, v in self.top5_positive_adj.items():
            labels_pos.append(k)
            means_pos.append(v)

        for k, v in self.top5_neutral_adj.items():
            labels_neu.append(k)
            means_neu.append(v)

        for k, v in self.top5_negative_adj.items():
            labels_neg.append(k)
            means_neg.append(v)

        x = np.arange(len(labels_pos))
        width = 1.5

        overall_labels = labels_pos + labels_neu + labels_neg
        ticks_x = []
        max_y = max(means_pos + means_neu + means_neg)

        c = 0
        while c != 30:
            array = c + (x - width) / 0.6
            ticks_x.extend(array)
            c += 10

        ticks_x1 = np.array(ticks_x)
        font_t = {'fontname': 'montserrat', 'size': '16', 'color': 'black', 'weight': 'medium',
                  'verticalalignment': 'bottom'}
        font_o = {'fontname': 'montserrat', 'size': '9', 'color': 'black', 'weight': 'light'}

        font_path = 'C:\\Users\\paxom\\Documents\\ноВШЭсти\\Шрифты\\Montserrat&FiraSans\\Montserrat-Light.ttf'
        font_prop = font_manager.FontProperties(fname=font_path, size=11)

        fig, ax = plt.subplots()

        pos = ax.bar(0 + (x - width) / 0.6, means_pos, width, label='Positive', color='gold', alpha=0.9)
        neu = ax.bar(10 + (x - width) / 0.6, means_neu, width, label='Neutral', color='lightsteelblue')
        neg = ax.bar(20 + (x - width) / 0.6, means_neg, width, label='Negative', color='maroon', alpha=0.9)

        ax.set_xticks(ticks_x1)
        ax.set_xticklabels(overall_labels, **font_o, rotation=60)
        plt.ylim(0, max_y + 100)
        ax.set_ylabel('The amount of tweets', **font_o)
        ax.set_title('TOP-5 Adjectives distributed by tonality', **font_t)
        ax.legend(loc='upper right', prop=font_prop)
        fig.tight_layout()

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', size=10)

        autolabel(pos)
        autolabel(neu)
        autolabel(neg)

        plt.show()

    def time_distribution(self):
        def rule_time(dict, file, labels, rate_pos, rate_neu, rate_neg, rate_sum):
            key_list = list(dict.keys())
            k = key_list[len(key_list) - 1]
            start_point = k[:16]
            key_list_reversed = reversed(key_list)

            model_start = datetime.datetime.strptime(start_point, '%Y-%m-%d %H:%M')  # Начало отсчёта
            model_end = model_start + datetime.timedelta(minutes=180)  # Конец отсчёта

            labels.append(start_point[11:16])
            labels.append(model_end.strftime('%H:%M'))

            rule_tweets_2 = {}
            for i in key_list_reversed:
                rule_tweets_2[i] = dict[i]

            positive = 0
            neutral = 0
            negative = 0

            sum = positive + neutral + negative
            rate_sum.append(sum)
            rate_pos.append(positive)
            rate_neu.append(neutral)
            rate_neg.append(negative)

            for k, v in rule_tweets_2.items():
                date_start = datetime.datetime.strptime(k[:16], '%Y-%m-%d %H:%M')
                if k[17:len(k)] != '1':
                    if model_start <= date_start <= model_end:
                        if v == 1:
                            positive += 1
                        elif v == 0:
                            neutral += 1
                        elif v == -1:
                            negative += 1
                        continue
                    else:
                        sum = positive + neutral + negative

                        positive_percentage = round((positive * 100) / sum, 2)
                        neutral_percentage = round((neutral * 100) / sum, 2)
                        negative_percentage = round((negative * 100) / sum, 2)

                        rate_sum.append(sum)
                        rate_pos.append(positive_percentage)
                        rate_neu.append(neutral_percentage)
                        rate_neg.append(negative_percentage)

                        with open(file, 'a', encoding='utf-8') as hours:
                            hours.write(
                                '{} - {} : {}  {}/{}/{}\n'.format(model_start.time(), model_end.time(), sum,
                                                                  positive_percentage,
                                                                  neutral_percentage,
                                                                  negative_percentage))
                        model_end += datetime.timedelta(minutes=180)
                        labels.append(model_end.strftime('%H:%M'))
                        if model_start <= date_start <= model_end:
                            if v == 1:
                                positive += 1
                            elif v == 0:
                                neutral += 1
                            elif v == -1:
                                negative += 1
                            continue

                elif k[17:len(k)] == '1':
                    if model_start <= date_start <= model_end:
                        if v == 1:
                            positive += 1
                        elif v == 0:
                            neutral += 1
                        elif v == -1:
                            negative += 1
                        sum = positive + neutral + negative

                        positive_percentage = round((positive * 100) / sum, 2)
                        neutral_percentage = round((neutral * 100) / sum, 2)
                        negative_percentage = round((negative * 100) / sum, 2)

                        rate_sum.append(sum)
                        rate_pos.append(positive_percentage)
                        rate_neu.append(neutral_percentage)
                        rate_neg.append(negative_percentage)

                        with open(file, 'a', encoding='utf-8') as hours:
                            hours.write(
                                '{} - {} : {}  {}/{}/{}\n'.format(model_start.time(), model_end.time(), sum,
                                                                  positive_percentage,
                                                                  neutral_percentage,
                                                                  negative_percentage))
                        break
                    else:
                        sum = positive + neutral + negative

                        positive_percentage = round((positive * 100) / sum, 2)
                        neutral_percentage = round((neutral * 100) / sum, 2)
                        negative_percentage = round((negative * 100) / sum, 2)

                        rate_sum.append(sum)
                        rate_pos.append(positive_percentage)
                        rate_neu.append(neutral_percentage)
                        rate_neg.append(negative_percentage)

                        with open(file, 'a', encoding='utf-8') as hours:
                            hours.write(
                                '{} - {} : {}  {}/{}/{}\n'.format(model_start.time(), model_end.time(), sum,
                                                                  positive_percentage,
                                                                  neutral_percentage,
                                                                  negative_percentage))
                        model_end += datetime.timedelta(minutes=180)
                        labels.append(model_end.strftime('%H:%M'))
                        if model_start <= date_start <= model_end:
                            if v == 1:
                                positive += 1
                            elif v == 0:
                                neutral += 1
                            elif v == -1:
                                negative += 1
                            sum = positive + neutral + negative

                            positive_percentage = round((positive * 100) / sum, 2)
                            neutral_percentage = round((neutral * 100) / sum, 2)
                            negative_percentage = round((negative * 100) / sum, 2)

                            rate_sum.append(sum)
                            rate_pos.append(positive_percentage)
                            rate_neu.append(neutral_percentage)
                            rate_neg.append(negative_percentage)

                            with open(file, 'a', encoding='utf-8') as hours:
                                hours.write(
                                    '{} - {} : {}  {}/{}/{}\n'.format(model_start.time(), model_end.time(), sum,
                                                                      positive_percentage,
                                                                      neutral_percentage,
                                                                      negative_percentage))
                            break

        rule_time(self.first_rule_tweets, 'hours_r1.txt', self.classification_label_r1,
                  self.classification_pos_r1, self.classification_neu_r1, self.classification_neg_r1, self.classification_sum_r1)
        rule_time(self.second_rule_tweets, 'hours_r2.txt', self.classification_label_r2,
                  self.classification_pos_r2, self.classification_neu_r2, self.classification_neg_r2, self.classification_sum_r2)
        rule_time(self.third_rule_tweets, 'hours_r3.txt', self.classification_label_r3,
                  self.classification_pos_r3, self.classification_neu_r3, self.classification_neg_r3, self.classification_sum_r3)
        rule_time(self.fourth_rule_tweets, 'hours_r4.txt', self.classification_label_r4,
                  self.classification_pos_r4, self.classification_neu_r4, self.classification_neg_r4, self.classification_sum_r4)

        # print(self.classification_label_r1)
        # print(self.classification_pos_r1)
        # print(self.classification_neu_r1)
        # print(self.classification_neg_r1)
        # print(self.classification_sum_r1)

        # rules_time(self.first_rule_tweets)
        # rules_time(self.second_rule_tweets)
        # rules_time(self.third_rule_tweets)
        # rules_time(self.fourth_rule_tweets)

    def time_distribution_linecharts(self):

        def rules_linecharts(chart_name, labels, rule_pos, rule_neu, rule_neg, sum):
            style.use('seaborn')
            font_t = {'fontname': 'montserrat', 'size': '14', 'color': 'black', 'weight': 'medium',
                      'verticalalignment': 'bottom'}
            font_o = {'fontname': 'montserrat', 'size': '9', 'color': 'black', 'weight': 'light'}
            font_x = {'fontname': 'montserrat', 'size': '7.5', 'color': 'black', 'weight': 'light'}

            font_path = 'C:\\Users\\paxom\\Documents\\ноВШЭсти\\Шрифты\\Montserrat&FiraSans\\Montserrat-Light.ttf'
            font_prop = font_manager.FontProperties(fname=font_path, size=10)

            x = np.arange(len(labels))
            formatter = matplotlib.ticker.NullFormatter()
            fig, ax = plt.subplots(2, 1)

            ax[0].plot(x, rule_pos, label='Positive', color='orange', linestyle='-.', marker='o', markersize=6, lw=0.7)
            ax[0].plot(x, rule_neu, label='Neutral', color='mediumseagreen', marker='D', markersize=6, lw=0.7)
            ax[0].plot(x, rule_neg, label='Negative', color='firebrick', linestyle=':', marker='X', markersize=7, lw=0.7)
            ax[0].set_ylim(0, max(rule_pos + rule_neu + rule_neg) + 20)
            ax[0].legend(bbox_to_anchor=(0., 1.0, 1., .10), loc='lower center',
                         ncol=3, mode="expand", borderaxespad=0., frameon=False, prop=font_prop)
            ax[0].set_xticks(x)
            ax[0].set_ylabel('Fraction', **font_o)
            ax[0].xaxis.set_major_formatter(formatter)

            ax[1].scatter(x, sum, s=40, color='slategrey', marker='o')
            ax[1].vlines(x, 0, sum, color='slategrey', lw=0.7)
            ax[1].set_xticks(x)
            ax[1].set_xticklabels(labels, **font_x, rotation=90)
            ax[1].set_xlabel('Time window', **font_o)
            ax[1].set_ylim(0, max(sum) + 1000)
            ax[1].set_ylabel('Number of tweets', **font_o)

            fig.suptitle(chart_name, y=0.935, **font_t)
            plt.show()

        rules_linecharts('The distribution of tweets in time based on the first rule', self.classification_label_r1,
                         self.classification_pos_r1, self.classification_neu_r1,
                         self.classification_neg_r1, self.classification_sum_r1)
        rules_linecharts('The distribution of tweets in time based on the second rule', self.classification_label_r2,
                         self.classification_pos_r2, self.classification_neu_r2,
                         self.classification_neg_r2, self.classification_sum_r2)
        rules_linecharts('The distribution of tweets in time based on the third rule', self.classification_label_r3,
                         self.classification_pos_r3, self.classification_neu_r3,
                         self.classification_neg_r3, self.classification_sum_r3)
        rules_linecharts('The distribution of tweets in time based on the fourth rule', self.classification_label_r4,
                         self.classification_pos_r4, self.classification_neu_r4,
                         self.classification_neg_r4, self.classification_sum_r4)


if __name__ == "__main__":
    start = timer()

    lab = Lab()
    print('1')
    lab.filtered_data()  # УБЕРИ ХЭШТЕГИ В СТР. 98 - 99
    print('2')
    lab.frequency_length()  # УБЕРИ ХЭШТЕГИ В СТР. 129 - 132, 153 - 156
    print('3')
    lab.classification_rules()
    print('4')
    lab.classification_rules_barplots()
    print('5')
    lab.top5_adjectives()
    print('6')
    lab.top5_adjectives_barplot()
    print('7')
    lab.time_distribution()
    print('8')
    lab.time_distribution_linecharts()
    print('9')

    end = timer()
    execTime = end - start
    print('All methods performed in {} sec.'.format(execTime))
