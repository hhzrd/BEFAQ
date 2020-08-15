# coding=UTF-8
'''
@Author: xiaoyichao
@LastEditors: xiaoyichao
@Date: 2020-05-22 13:54:44
@LastEditTime: 2020-06-12 03:14:17
@Description: 线性模型的重排序，给予不同的算法不同的权重
'''


class ReRank(object):
    def linear_model(self, consin_sim, jaccard_sim, consine_weight, jaccard_weight):
        if consin_sim != []:
            multiple_sim = [i * consine_weight + j*jaccard_weight
                                for i, j in zip(consin_sim, jaccard_sim)]
            return multiple_sim
        else:
            multiple_sim = jaccard_sim
            return multiple_sim

