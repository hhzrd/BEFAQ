# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-09 14:45:34
LastEditTime: 2020-08-15 18:36:24
@Description: 获取问题集合的BERT向量
'''


import numpy as np

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from es.read_excel import ExcelData

exceldata = ExcelData()
sheet_names = exceldata.get_sheet_names()
dir_name = os.path.abspath(os.path.dirname(__file__))


class ReadVec2bin(object):
    def __init__(self):
        self.owner_name_sentence = {}
        self.owner_name_bert_vecs = {}
        for sheet_name in sheet_names:
            bert_vecs_path = os.path.join(
                dir_name, './bert_vect/%s_bert_vecs.bin' % (sheet_name))
            bert_sentences_path = os.path.join(
                dir_name, './bert_vect/%s_bert_sentences.txt' % (sheet_name))

            with open(bert_sentences_path, "r", encoding="utf8")as sent:
                sentences = sent.read()
                sentences = sentences.strip("\n")
                sentences = sentences.split("\n")
            self.owner_name_sentence[sheet_name] = sentences[1:]

            bert_vecs = np.fromfile(bert_vecs_path, dtype=np.float)
            bert_vecs = bert_vecs.reshape((-1, 512))
            self.owner_name_bert_vecs[sheet_name] = bert_vecs[1:]

    def read_bert_sents(self, owner_name):
        return self.owner_name_sentence[owner_name]

    def read_bert_vecs(self, owner_name):
        return self.owner_name_bert_vecs[owner_name]

