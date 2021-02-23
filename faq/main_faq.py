# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-05-12 20:46:56
@Description: FAQ功能的主程序文件
'''
import time
import jieba
from retrieval_es import SearchData
from matching_operate import Matching
from deduplicate_threshold_op import DeduplicateThreshold
from re_rank import ReRank
from get_final_data import FinalData
from sanic import Sanic
from sanic.response import json
from sanic import response
from jieba4befaq import JiebaBEFAQ
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configparser
from get_ip import get_host_ip


dir_name = os.path.abspath(os.path.dirname(__file__))

faq_config = configparser.ConfigParser()
faq_config.read(os.path.join(dir_name, "befaq_conf.ini"))
consine_weight = float(faq_config["AlgorithmConfiguration"]["consine"])
jaccard_weight = float(faq_config["AlgorithmConfiguration"]["jaccard"])
BM25_weight = float(faq_config["AlgorithmConfiguration"]["BM25"])
edit_distance_weight = float(faq_config["AlgorithmConfiguration"]["edit_distance"])
use_faiss = int(faq_config["AlgorithmConfiguration"]["use_faiss"])
use_annoy = int(faq_config["AlgorithmConfiguration"]["use_annoy"])
engine_num = int(faq_config["Faiss_Annoy_Configuration"]["engine_num"])
ES_num = int(faq_config["ESConfiguration"]["ES_num"])
use_other_when_es_none = int(faq_config["AlgorithmConfiguration"]["use_other_when_es_none"])
if use_other_when_es_none == 1:
    use_other_when_es_none = True
else:
    use_other_when_es_none = False


def kill_port(port):

    find_kill = "kill -9 $(lsof -i:%d -t)" % port
    try:
        result = os.popen(find_kill)
        print("%d端口程序kill 成功" % port)
        return result.read()
    except Exception:
        print("%d端口程序kill 失败" % port)


jiebaBEFAQ = JiebaBEFAQ()
search_data = SearchData()
match_ing = Matching()
rerank = ReRank()
final_data = FinalData()
deduplicate_threshold = DeduplicateThreshold()

app = Sanic()
app = Sanic("Feedback BEFAQ")


@app.route("/BEFAQ", methods=["POST", "HEAD"])
async def myfaq(request):
    orgin_query = str(request.form.get("question"))
    owner_name = str(request.form.get("owner_name"))
    get_num = int(request.form.get("get_num", default=3))
    threshold = float(request.form.get("threshold", default=0.5))

    # 给ES使用的结巴分词
    process_query = jiebaBEFAQ.seg_sentence(
        sentence=orgin_query)
    print("process_query", process_query)
    query_terms = jieba.cut(process_query)
    # print("query_terms",query_terms)
    query_word_list = list(query_terms)
    print("query_word_list", query_word_list)

    begin_time = time.time()

    def print_usetime(query, module):
        current_time = time.time()
        use_time = current_time - begin_time
        if use_time > 1.0:
            print("time more than 1")
        print("Q:%s,%s用时%f秒" % (query, module, use_time))

    maybe_original_questions, maybe_process_questions, maybe_answers, retrieval_q_ids, specific_q_ids = search_data.search_merge(
        owner_name=owner_name, question=orgin_query, query_word_list=query_word_list, use_faiss=use_faiss, use_annoy=use_annoy, engine_limit_num=engine_num, ES_limit_num=ES_num, use_other_when_es_none=use_other_when_es_none)

    print_usetime(query=orgin_query, module="召回阶段")
    print(maybe_original_questions)

    if len(retrieval_q_ids) > 0:  # ES（或faiss 或 annoy ）中检索到了数据
        # cosine_sim的retrieval_questions使用的maybe_original_questions，orgin_query使用的没有处理过的query
        consin_sim = match_ing.cosine_sim(
            orgin_query=orgin_query, retrieval_questions=maybe_original_questions, owner_name=owner_name)
        print_usetime(query=orgin_query, module="Matching cosine_sim")
        print("consin_sim:", consin_sim)

        # jaccard_sim的retrieval_questions使用的maybe_process_questions,orgin_query使用的是去掉停用词的query
        jaccard_sim = match_ing.jaccard_sim(
            orgin_query=process_query, retrieval_questions=maybe_process_questions)
        print("jaccard_sim:", jaccard_sim)

        bm25_sim = match_ing.bm25_sim(
            orgin_query=process_query, retrieval_questions=maybe_process_questions)
        print("bm25_sim:", bm25_sim)

        edit_distance_sim = match_ing.edit_distance_sim(
            orgin_query=process_query, retrieval_questions=maybe_process_questions)
        print("edit_distance_sim:", edit_distance_sim)

        re_rank_sim = rerank.linear_model(
            consin_sim=consin_sim, jaccard_sim=jaccard_sim, bm25_sim=bm25_sim, edit_distance_sim=edit_distance_sim,
            consine_weight=consine_weight, jaccard_weight=jaccard_weight, BM25_weight=BM25_weight, edit_distance_weight=edit_distance_weight)

        print("retrieval_q_ids:", retrieval_q_ids)
        print("maybe_original_questions:", maybe_original_questions)
        print("maybe_process_questions:", maybe_process_questions)
        print("re_rank_sim:", re_rank_sim)

        high_confidence_q_id_pos = deduplicate_threshold.dedu_thr(
            q_ids=retrieval_q_ids, re_rank_sim_list=re_rank_sim, threshold=threshold)
        print_usetime(query=orgin_query, module="Deduplicate and Threshold")
        print("high_confidence_q_id_pos:", high_confidence_q_id_pos)

        begin_time = time.time()

        return_data = final_data.get_qa(
            high_confidence_q_id_pos, maybe_original_questions, maybe_answers, re_rank_sim=re_rank_sim, get_num=get_num, retrieval_q_ids=retrieval_q_ids, specific_q_ids=specific_q_ids)

        print(return_data)
        return json(return_data)
    else:  # ES中没有检索到数据
        return_data = []
        return json(return_data)


@app.route("/", methods=["GET", "HEAD"])
async def alibaba_operator_check(request):
    print("alibaba SLB checking server status")
    return response.text(200)


if __name__ == "__main__":

    this_ip = get_host_ip()
    port = int(faq_config["ServerAddress"]["port"])
    kill_port(port)
    # 启动http 服务
    app.run(host=this_ip,
            port=int(faq_config["ServerAddress"]["port"]),
            workers=int(faq_config["ServerInfo"]["work_number"]),
            debug=True, access_log=True)
