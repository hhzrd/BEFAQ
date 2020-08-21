# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-01-02 16:55:23
LastEditTime: 2020-08-15 16:00:17
@Description: 使用ES召回数据和Faiss(annoy)召回数据

'''

from elasticsearch import Elasticsearch
from annoy import AnnoyIndex
import numpy as np
import faiss
from get_question_vecs import ReadVec2bin
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from es.es_operate import ESCURD
import configparser
from bert_server.multi_bert_server import MyBert


dir_name = os.path.abspath(os.path.dirname(__file__))
es_config = configparser.ConfigParser()
es_config.read(os.path.join(dir_name, "../es/es.ini"))
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
bc = MyBert()
read_vec2bin = ReadVec2bin()


class SearchData(object):
    '''
    Author: xiaoyichao
    param {type}
    Description: 用于召回数据，会使用ES，Annoy，Faiss,具体使用哪些可以自己配置
    '''
    def search_es(self, owner_name, query_word_list, ES_limit_num):
        '''
        Author: xiaoyichao
        param {type}
        Description: 使用ES召回
        '''
        retrieve_data = es_faq.search_data(
            index_name=index_name, owner_name=owner_name, query_word_list=query_word_list, limit_num=ES_limit_num)
        retrieve_results = retrieve_data["hits"]
        max_result_len = retrieve_results["total"]["value"]
        # max_score = retrieve_results["max_score"]
        hits = retrieve_results["hits"]
        maybe_original_questions = []
        maybe_process_questions = []
        maybe_answers = []
        specific_q_ids = []
        q_ids = []
        if ES_limit_num < max_result_len:
            result_len = ES_limit_num
        else:
            result_len = max_result_len
        for i in range(result_len):
            qu_an_id = hits[i]["_source"]
            original_question = qu_an_id["original_question"]
            process_question = qu_an_id["process_question"]
            answer = qu_an_id["answer"]
            q_id = qu_an_id["q_id"]
            specific_q_id = qu_an_id["specific_q_id"]
            maybe_original_questions.append(original_question)
            maybe_process_questions.append(process_question)
            maybe_answers.append(answer)
            q_ids.append(q_id)
            specific_q_ids.append(specific_q_id)
        return maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids

    def search_annoy(self, owner_name, question, num=5):
        '''
        Author: xiaoyichao
        param {type}
        Description: 使用Annoy 召回
        '''
        sentences = read_vec2bin.read_bert_sents(owner_name=owner_name)
        annoy_index_path = os.path.join(
            dir_name, '../es/search_model/%s_annoy.index' % owner_name)
        encodearrary = np.array(bc.encode([question]))
        tc_index = AnnoyIndex(f=512, metric='angular')
        tc_index.load(annoy_index_path)
        items = tc_index.get_nns_by_vector(
            encodearrary[0], num, include_distances=True)
        sim_questions = [sentences[num_annoy] for num_annoy in items[0]]
        # sims = items[1]
        # index_nums = items[0]
        return sim_questions

    def search_faiss(self, owner_name, question, num=5):
        '''
        Author: xiaoyichao
        param {type}
        Description: 使用Faiss 召回
        '''
        sentences = read_vec2bin.read_bert_sents(owner_name=owner_name)
        faiss_index_path = os.path.join(
            dir_name, '../es/search_model/%s_faiss.index' % owner_name)
        index = faiss.read_index(faiss_index_path)
        question_vec = np.array(bc.encode([question])).astype('float32')
        index.nprobe = 1
        sims, index_nums = index.search(question_vec, num)
        sim_questions = [sentences[num_faiss] for num_faiss in index_nums[0]]
        # index_nums = index_nums[0].tolist()
        # sims = sims[0].tolist()
        return sim_questions

    def merge_op(self, question, owner_name, maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids, use_faiss, use_annoy, engine_limit_num):
        '''
        Author: xiaoyichao
        param {type}
        Description: 合并ES与faiss或（和）annoy的结果
        '''
        if use_faiss == 1 and use_annoy == 0:
            print("use_faiss")
            mayey_search_questions = self.search_faiss(
                owner_name, question, num=engine_limit_num)
        elif use_faiss == 0 and use_annoy == 1:
            print("use_annoy")
            mayey_search_questions = self.search_annoy(
                owner_name, question, num=engine_limit_num)
        elif use_faiss == 1 and use_annoy == 1:
            print("use_annoy and use_faiss ")
            mayey_search_questions_faiss = self.search_faiss(
                owner_name, question, num=engine_limit_num)
            mayey_search_questions_annoy = self.search_annoy(
                owner_name, question, num=engine_limit_num)
            mayey_search_questions = list(
                set(mayey_search_questions_faiss+mayey_search_questions_annoy))
        else:
            return maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids
        print("ES检索出的数据", maybe_original_questions)
        # 再去查ES的数据，跟ES的数据做合并。去重复。
        for sim_question in mayey_search_questions:
            if sim_question not in set(maybe_original_questions):
                print("faiss、annoy 检索出的新数据", sim_question)
                retrieve_data = es_faq.search4search_engine(
                    index_name, owner_name, question=sim_question)
                retrieve_results = retrieve_data["hits"]
                max_result_len = retrieve_results["total"]["value"]
                # max_score = retrieve_results["max_score"]
                hits = retrieve_results["hits"]

                if max_result_len >= 1:
                    for i in range(1):
                        qu_an_id = hits[i]["_source"]
                        original_question = qu_an_id["original_question"]
                        process_question = qu_an_id["process_question"]
                        answer = qu_an_id["answer"]
                        q_id = qu_an_id["q_id"]
                        specific_q_id = qu_an_id["specific_q_id"]
                        maybe_original_questions.append(original_question)
                        maybe_process_questions.append(process_question)
                        maybe_answers.append(answer)
                        q_ids.append(q_id)
                        specific_q_ids.append(specific_q_id)
        # 合并数据
        return maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids

    def search_merge(self, owner_name, question, query_word_list, use_other_when_es_none, use_faiss=0, use_annoy=0, engine_limit_num=5, ES_limit_num=10):
        # 首先用ES检索
        maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids = self.search_es(
            owner_name=owner_name, query_word_list=query_word_list, ES_limit_num=ES_limit_num)
        if use_other_when_es_none is False:
            if len(maybe_original_questions) == 0:  # ES没有数据的时候才用faiss或(和)annoy
                # 推荐使用这种方式，因为faiss和annoy一定会召回指定数量的数据。这其中很可能会出现你不想看到的数据。当ES召回数据量为0的时候，再利用Fasis或（和）annoy召回数据
                maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids = self.merge_op(
                    question, owner_name, maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids, use_faiss, use_annoy, engine_limit_num)
        else:  # ES有数据的时候也用faiss或(和)annoy。
            maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids = self.merge_op(
                question, owner_name, maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids, use_faiss, use_annoy, engine_limit_num)

        return maybe_original_questions, maybe_process_questions, maybe_answers, q_ids, specific_q_ids
