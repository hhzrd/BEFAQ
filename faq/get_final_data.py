# coding=UTF-8
'''
@Author: xiaoyichao
@LastEditors: xiaoyichao
@Date: 2020-05-23 16:21:51
@LastEditTime: 2020-07-23 14:45:05
@Description: FAQ模块。根据去重复，卡阈值之后留下的q_id，取出对应的question,answer,相似度
'''


class FinalData(object):
    def get_json_confidence(self, json_data):
        return json_data["confidence"]

    def get_qa(self, high_confidence_q_id_pos, maybe_questions, maybe_answers, re_rank_sim, get_num, retrieval_q_ids, specific_q_ids):
        return_data = []
        for q_id_pos in high_confidence_q_id_pos:
            single_json = {}
            single_json["q_id"] = retrieval_q_ids[q_id_pos]
            single_json["specific_q_id"] = specific_q_ids[q_id_pos]
            single_json["question"] = maybe_questions[q_id_pos]
            single_json["answer"] = maybe_answers[q_id_pos]
            single_json["confidence"] = round(re_rank_sim[q_id_pos], 2)
            return_data.append(single_json)
        return_data.sort(reverse=True, key=self.get_json_confidence)
        # 对返回数据的数量进行限制。
        if len(high_confidence_q_id_pos) > get_num:
            return return_data[:get_num]
        else:
            return return_data
