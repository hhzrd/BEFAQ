# coding=UTF-8
'''
@Author: xiaoyichao
@LastEditors: xiaoyichao
@Date: 2020-05-22 12:24:06
@LastEditTime: 2020-07-23 14:28:52
@Description: 对重排序后的数据，根据q_id进行去重复，卡阈值。低于置信度阈值的数据不要
'''


class DeduplicateThreshold(object):
    def dedu_thr(self, q_ids, re_rank_sim_list, threshold):
        high_confidence_q_id_pos = []
        if len(q_ids) > 0:
            q_id_dict = {}
            # 获取 q_id和posstion关系的字典
            for position, id in enumerate(q_ids):
                if id not in q_id_dict:
                    q_id_dict[id] = [position]
                else:
                    q_id_dict[id].append(position)
            print(q_id_dict)
            # 对q_id去重复,某个q_id下存在多个数据的，取其中最高相似度的结果，某个q_id下只有一个数据的直接取这个数据，也就是第0个数据
            unique_q_ids_pos = []
            for poss in q_id_dict.values():
                max_sim_pos = poss[0]
                if len(poss) > 1:
                    for qid_pos in poss:
                        if re_rank_sim_list[qid_pos] > re_rank_sim_list[max_sim_pos]:
                            max_sim_pos = qid_pos
                unique_q_ids_pos.append(max_sim_pos)
            # 对去重复后的q_id,卡阈值,高于置信度的才要。
            for q_id_pos in unique_q_ids_pos:
                if re_rank_sim_list[q_id_pos] >= threshold:
                    high_confidence_q_id_pos.append(q_id_pos)
            return high_confidence_q_id_pos
        else:
            return high_confidence_q_id_pos

