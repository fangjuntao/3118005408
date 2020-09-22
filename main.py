# -*- coding: utf-8 -*-

import jieba
import jieba.analyse
import os
import numpy as np
import argparse



def get_keywords(context1,context2):
    # 去除停用词
    stopwords = [line.strip() for line in open('StopWords.txt',encoding='UTF-8').readlines()]
    stopwords.append("\n")
    # 分词
    keywords1 = [i for i in jieba.cut(context1, cut_all=True) if(i not in stopwords) and i != '']

    keywords2 = [i for i in jieba.cut(context2, cut_all=True) if(i not in stopwords) and i != '']
    # 对两个关键词列表进行合并去重(set会去重复元素)
    word_set = set(keywords1).union(set(keywords2))
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
        k1_cut_freq[word_dict[word]] += 1
    for word in keywords2:
        k2_cut_freq[word_dict[word]] += 1

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


def main():
    #输入文件绝对路径，arg1，arg2为要查重的文件，arg3为答案文件
    parser = argparse.ArgumentParser(description="基于python实现论文查重")
    parser.add_argument('--l1',  type=str, help='标准文件')
    parser.add_argument('--l2',  type=str, help='要查重的文件')
    parser.add_argument('--l3',  type=str, help='答案文件')
    args = parser.parse_args()
    # arg1, arg2, arg3 = args.l1, args.l2, args.l3
    arg1  ="E:\\我的资源\\大学课件\\软件工程导论\\作业之论文查重\\test\\orig.txt"
    arg2  ="E:\\我的资源\\大学课件\\软件工程导论\\作业之论文查重\\test\\orig_0.8_dis_10.txt"
    arg3  ="E:\\我的资源\\大学课件\\软件工程导论\\作业之论文查重\\test\\answer.txt"
    text1 = open(arg1, 'rb')
    text2 = open(arg2, 'rb')
    orig = text1.read()  # 读取文件
    orig_check = text2.read()

    ans = open(arg3, 'w+')  # 如果输出文件不存在则创建，存在则覆盖
    # 获取关键词
    keywords1,keywords2,word_set=get_keywords(orig,orig_check)
    # 获取词频向量
    freq1,freq2=get_freq(keywords1,keywords2,word_set)
    # 计算余弦值
    similarity = CosineSimilarity(freq1,freq2)
    # 获取文件名
    orig_filename = arg1[len(os.path.dirname(arg1)) + 1:]
    orig_check_filename = arg2[len(os.path.dirname(arg2)) + 1:]
    sim = "{}和{}的重复率为:{:.2f}".format(orig_filename,orig_check_filename, similarity)
    print(sim)
    ans.write(sim)
    text1.close()
    text2.close()
    ans.close()
    return 0


if __name__ == '__main__':
  main()
