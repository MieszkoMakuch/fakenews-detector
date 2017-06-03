"""
    function:
    k-fold cross validation
    """

# sentence length(# of char)
# sentence length(# of words)
# # of punctuations
# # of illegal punctuations
import re
import string

import nltk
import numpy as np


def extract_adjective(sentences):
    adj_sentences = list()
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        adj_tags = nltk.pos_tag(words)
        one_adj_sentence = ""
        for index, tag in enumerate(adj_tags, start=0):
            one_tag = tag[1]
            if one_tag in ['JJ', 'JJR', 'JJS']:
                one_adj_sentence += words[index]
                one_adj_sentence += " "
        adj_sentences.append(one_adj_sentence)
        # print(one_adj_sentence)
    return adj_sentences


def removePunc(input):
    '''
    :param input: string
    :return: string, without the punctuations
    '''
    # return input.translate(string.maketrans("",""), string.punctuation)
    return re.sub("[\.\t\,\:;\(\)\.]", "", input, 0, 0)


def numOfWords(input):
    '''
    :param input: string
    :return: number of words, number of continuous space
    '''
    splitted = input.split(" ")
    res = 0
    for i in splitted:
        if len(i) > 0:
            res += 1
    return res


def numOfChar(input):
    '''
    :param input: string
    :return: number of char
    '''
    return len(input)


def numOfPunc(input):
    '''
    :param input: string
    :return: number of punctuations
    '''
    return len(input) - len(removePunc(input))


def numOfContPunc(input):
    res = 0;
    state = False
    for i in range(1, len(input)):
        if input[i] in string.punctuation:
            if input[i - 1] in string.punctuation:
                if state:
                    pass
                else:
                    state = True
                    res += 1
            else:
                state = False
                pass
        else:
            state = False
    return res


def numOfContUpperCase(input):
    res = 0;
    state = False
    for i in range(1, len(input)):
        if input[i].isupper():
            if input[i - 1].isupper():
                if state:
                    pass
                else:
                    state = True
                    res += 1
            else:
                state = False
                pass
        else:
            state = False
    return res
    pass


def constructMat(file, label):
    '''
    :param file: input file
    :param label: the label of the data in the file
    :return: ndarray
    '''
    res = np.array([])
    line1 = True
    with open(file) as data:
        for line in data:
            if line1:
                line1 = False
                cleaned = line.lower().strip()
                original = line.strip()
                fea1 = numOfWords(cleaned)
                fea2 = numOfChar(cleaned)
                fea3 = numOfPunc(cleaned)
                fea4 = numOfContPunc(cleaned)
                fea5 = numOfContUpperCase(original)
                res = np.array([[fea1, fea2, fea3, fea4, fea5, label]])
            else:
                cleaned = line.lower().strip()
                original = line.strip()
                fea1 = numOfWords(cleaned)
                fea2 = numOfChar(cleaned)
                fea3 = numOfPunc(cleaned)
                fea4 = numOfContPunc(cleaned)
                fea5 = numOfContUpperCase(original)
                newrow = np.array([[fea1, fea2, fea3, fea4, fea5, label]])
                res = np.append(res, newrow, axis=0)
    return res


def constructRealFea(headline):
    cleaned = headline.lower().strip()
    original = headline.strip()
    fea1 = numOfWords(cleaned)
    fea2 = numOfChar(cleaned)
    fea3 = numOfPunc(cleaned)
    fea4 = numOfContPunc(cleaned)
    fea5 = numOfContUpperCase(original)
    res = np.array([[fea1, fea2, fea3, fea4, fea5]])
    return res


if __name__ == '__main__':
    # print numOfContUpperCase("huhAAiAihiuhAAAAuhuhAAAAA")
    print(constructMat('./fake.txt', 1))
