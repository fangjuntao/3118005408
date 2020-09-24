# -*- coding: utf-8 -*-


import os
import argparse
from  util import *
from  FileException import *


def main():
    #输入文件绝对路径，arg1，arg2为要查重的文件，arg3为答案文件
    parser = argparse.ArgumentParser(description="基于python实现论文查重")
    parser.add_argument('l1',  type=str, help='标准文件')
    parser.add_argument('l2',  type=str, help='要查重的文件')
    parser.add_argument('l3',  type=str, help='答案文件')
    args = parser.parse_args()
    arg1, arg2, arg3 = args.l1, args.l2, args.l3


    if not os.path.exists(arg1):
        print("标准文件不存在！")
        exit()
    if not os.path.exists(arg2):
        print("要查重文件不存在！")
        exit()


    text1 = open(arg1, 'rb')
    text2 = open(arg2, 'rb')
    orig = text1.read()  # 读取文件
    orig_check = text2.read()
    # 空文本异常
    if(len(orig)==0 or len(orig_check)==0):
        text1.close()
        text2.close()
        raise empty_error
    ans = open(arg3, 'w+')  # 如果输出文件不存在则创建，存在则覆盖
    # 获取关键词
    keywords1,keywords2,word_set=get_keywords(orig,orig_check)
    # 获取词频向量
    freq1,freq2=get_freq(keywords1,keywords2,word_set)
    # 计算余弦值
    similarity = CosineSimilarity(freq1,freq2)
    # # 获取文件名
    # orig_filename = arg1[len(os.path.dirname(arg1)) + 1:]
    # orig_check_filename = arg2[len(os.path.dirname(arg2)) + 1:]
    #sim = "{}和{}的重复率为:{:.2f}".format(orig_filename,orig_check_filename, similarity)
    # print(sim)
    sim = "两文件的重复率为：{:.2f}".format(similarity)
    print(sim)
    ans.write(sim)
    text1.close()
    text2.close()
    ans.close()
    return 0


if __name__ == '__main__':
  main()
