# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-03-24 13:25:41
LastEditTime: 2021-02-23 17:45:49
@Description: 对用户的FAQ问题。去掉停用词，比如，怎样，如何这些词。然后进入ES搜索
'''
import jieba
import os
dir_name = os.path.abspath(os.path.dirname(__file__))


class JiebaBEFAQ(object):

    def stopwordslist(self, filepath):
        stopwords = [line.strip() for line in open(
            filepath, 'r', encoding='utf-8').readlines()]
        return set(stopwords)

    # 对句子进行分词
    def seg_sentence(self, sentence):
        #  创建用户字典
        userdict = os.path.join(dir_name, '../es/userdict.txt')
        jieba.load_userdict(userdict)
        sentence_seged = jieba.cut(sentence.strip())
        stopwords_file = os.path.join(
            dir_name, '../es/stopwords4_process_question_dedup.txt')
        stopwords = self.stopwordslist(stopwords_file)  # 这里加载停用词的路径
        outstr = ""  # 分隔符号
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += ""  # 分隔符号
        return outstr

    def get_list(self, sentence):
        '''
        Author: xiaoyichao
        param {type}
        Description: 将句子变成切次词后的list
        '''
        sentence_terms = list(jieba.cut(sentence))
        return sentence_terms
