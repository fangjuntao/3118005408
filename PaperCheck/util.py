
import jieba
import jieba.analyse

import numpy as np

def get_keywords(context1,context2):
    # 读入停用词
    stopwords = [line.strip() for line in open('StopWords.txt',encoding='UTF-8').readlines()]
    stopwords.append("\n")
    # 对两文档分别分词
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

    length  = len(word_dict)
    # 根据词袋模型统计词在每篇文档中出现的次数，形成向量
    k1_cut_freq = [0] * length
    k2_cut_freq = [0] * length

    for word in keywords1:
        if word in word_dict:
            k1_cut_freq[word_dict[word]] += 1
    for word in keywords2:
        if word in word_dict:
            k2_cut_freq[word_dict[word]] += 1



    return k1_cut_freq,k2_cut_freq

def CosineSimilarity(k1_cut_freq, k2_cut_freq):
    # 余弦相似度计算
    sim= float(np.dot(k1_cut_freq,k2_cut_freq) / (np.linalg.norm(k1_cut_freq) * np.linalg.norm(k2_cut_freq)))
    return sim



