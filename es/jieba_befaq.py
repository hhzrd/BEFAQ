# coding=UTF-8
'''
@Author: xiaoyichao
@LastEditors: xiaoyichao
@Date: 2020-03-24 13:25:41
@LastEditTime: 2020-06-15 02:50:35
@Description:  用于写入ES的process_question字段时去掉同义词。比如，怎样，如何这些词。
'''
import jieba
import os
dir_name = os.path.abspath(os.path.dirname(__file__))


class StopwordsBEFAQ(object):

    def stopwordslist(self, filepath):
        stopwords = [line.strip() for line in open(
            filepath, 'r', encoding='utf-8').readlines()]
        return set(stopwords)

    # 对句子进行分词
    def seg_sentence4faq(self, sentence ):
        #  创建用户字典
        userdict = os.path.join(dir_name, 'userdict.txt')
        jieba.load_userdict(userdict)
        sentence_seged = jieba.cut(sentence.strip())
        stopwords_file = os.path.join(
            dir_name, 'stopwords4_process_question_dedup.txt')
        stopwords = self.stopwordslist(stopwords_file)  # 这里加载停用词的路径
        outstr = ""  # 分隔符号
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += ""  # 分隔符号
        return outstr
    def seg_sentence4customer_service(self, sentence ):
        #  创建用户字典
        userdict = os.path.join(dir_name, 'userdict.txt')
        jieba.load_userdict(userdict)
        sentence_seged = jieba.cut(sentence.strip())
        # stopwords_file = os.path.join(
        #     dir_name, 'stopwords4_process_question_dedup.txt')
        # stopwords = self.stopwordslist(stopwords_file)  # 这里加载停用词的路径
        outstr = ""  # 分隔符号
        for word in sentence_seged:
            # if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += ""  # 分隔符号
        return outstr

# if __name__ == '__main__':
#     stopwords = StopwordsBEFAQ()
#     line = "下拉刷新的时候有个bug"
#     line_seg = stopwords.seg_sentence(line)
#     print(line_seg)
