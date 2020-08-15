# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-11 08:42:52
LastEditTime: 2020-08-15 11:53:39
@Description: BERT 处理，防止超时后报错。
'''
import numpy as np
import signal
import os
import configparser
from sentence_transformers import SentenceTransformer

dir_name = os.path.abspath(os.path.dirname(__file__))

faq_config = configparser.ConfigParser()
faq_config.read(os.path.join(dir_name, "../faq/befaq_conf.ini"))
Sentence_BERT_path = os.path.join(dir_name, "../", str(
    faq_config["AlgorithmConfiguration"]["Sentence_BERT_path"]))
print(Sentence_BERT_path)

embedder = SentenceTransformer(Sentence_BERT_path)


def MyBert():
    embedder = SentenceTransformer(Sentence_BERT_path)
    return embedder


def set_timeout(num, callback):
    def wrap(func):
        # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                r = func(*args, **kwargs)
                signal.alarm(0)  # 关闭闹钟
                return r
            except Exception:
                callback()

        return to_do

    return wrap


def after_timeout():  # 超时后的处理函数
    print("BERT服务超时")


@set_timeout(1, after_timeout)  # 限时 1 秒超时,不支持设置为浮点型数据
def get_bert(sentence_list):  # 要执行的函数
    try:
        sentences_vec = np.array(embedder.encode(sentence_list))
    except Exception:
        sentences_vec = []
        print("BERT time out")
    return sentences_vec


# # 测试 sentence Bert
# sentences_vec = get_bert(["你好"])
# print(sentences_vec)
