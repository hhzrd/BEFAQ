# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-12 07:19:00
LastEditTime: 2020-08-14 14:28:32
@Description: 用于实现搜索框的中文提示词的类
'''

from es_operate import ESCURD
from elasticsearch import Elasticsearch
import configparser
import os

dir_name = os.path.abspath(os.path.dirname(__file__))
es_config = configparser.ConfigParser()
es_config.read(os.path.join(dir_name, "es.ini"))
es_server_ip_port = es_config["ServerAddress"]["es_server_ip_port"]

index_name = es_config["ServerInfo"]["alias_name"]

if_es_use_passwd = es_config["ServerAddress"]["if_es_use_passwd"]
if if_es_use_passwd == "1":
    http_auth_user_name = es_config["ServerAddress"]["http_auth_user_name"]
    http_auth_password = es_config["ServerAddress"]["http_auth_password"]
    es_connect = Elasticsearch(
        es_server_ip_port, http_auth=(http_auth_user_name, http_auth_password))
else:

    es_connect = Elasticsearch(
        es_server_ip_port)

    
es_faq = ESCURD(es_connect)


class SearchData(object):
    # 实现搜索框的中文提示词的类
    def search_question_cn(self, owner_name, current_question, limit_num, if_middle):
        current_question = current_question.lower()
        search_limit_num = 100

        retrieve_data = es_faq.search_cn(
            index_name, owner_name, current_question, search_limit_num, if_middle)

        retrieve_results = retrieve_data["hits"]
        max_result_len = retrieve_results["total"]["value"]
        hits = retrieve_results["hits"]
        maybe_original_questions = []
        q_ids = []
        print("max_result_len", max_result_len)
        if limit_num < max_result_len:
            result_len = limit_num
        else:
            result_len = max_result_len
        for i in range(result_len):
            qu_an_id = hits[i]["_source"]
            original_question = qu_an_id["original_question"]
            q_id = qu_an_id["q_id"]
            maybe_original_questions.append(original_question)
            q_ids.append(q_id)
        q_id_set = set()
        deduplication_maybe_questions = []
        # q_id去重复并根据相关度排序
        for q_id, maybe_original_question in zip(q_ids, maybe_original_questions):
            if q_id not in q_id_set:
                deduplication_maybe_questions.append(maybe_original_question)

        return deduplication_maybe_questions


# if __name__ == "__main__":
#     search_data = SearchData()
#     maybe_original_questions = search_data.search_question_cn(owner_name="测试用副本", current_question="设计师", limit_num=3,if_middle="True")
#     print(maybe_original_questions)
