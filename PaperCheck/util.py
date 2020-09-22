
import jieba
import jieba.analyse

import numpy as np

def get_keywords(context1,context2):
    # 去除停用词
    stopwords = [line.strip() for line in open('StopWords.txt',encoding='UTF-8').readlines()]
    stopwords.append("\n")
    # 分词
    keywords1 = [i for i in jieba.cut(context1, cut_all=True) if i != '' and i != ' ']
    keywords2 = [i for i in jieba.cut(context2, cut_all=True) if i != '' and i != ' ']
    # 对两个关键词列表进行合并去重
    word_set = set(keywords1).union(set(keywords2)) - set(stopwords)
    return keywords1,keywords2,word_set


def get_freq(keywords1,keywords2,word_set):
    # 用字典保存两篇文章中出现的所有词并编上号
    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1
    # 根据词袋模型统计词在每篇文档中出现的次数，形成向量
    k1_cut_freq = [0] * len(word_dict)
    k2_cut_freq = [0] * len(word_dict)

    for word in keywords1:
        if word in word_dict:
            k1_cut_freq[word_dict[word]] += 1
    for word in keywords2:
        if word in word_dict:
            k2_cut_freq[word_dict[word]] += 1

    print("freq1: length")
    print("{}".format(len(k1_cut_freq)))
    print("freq2:length")
    print("{}".format(len(k2_cut_freq)))

    return k1_cut_freq,k2_cut_freq

def CosineSimilarity(k1_cut_freq, k2_cut_freq):
    # 余弦相似度计算
    sim= float(np.dot(k1_cut_freq,k2_cut_freq) / (np.linalg.norm(k1_cut_freq) * np.linalg.norm(k2_cut_freq)))
    return sim


def check_contain_chinese(check_str):
    # 中文字符的编码范围是：
    # \u4e00 - \u9fff
    # 只要编码在此范围就可判断为中文字符
    for ch in check_str.decode('utf-8'):
         if u'\u4e00' <= ch <= u'\u9fff':
             return False
    return True

