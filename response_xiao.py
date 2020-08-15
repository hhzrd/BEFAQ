# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-04-23 15:52:51
LastEditTime: 2020-08-15 11:55:02
@Description: 用于接口返回数据，加入headers
'''

from sanic.response import json


def res_xiao(data_json):
    '''
    Author: xiaoyichao
    param {type} 
    Description: 用于接口返回数据，加入headers
    '''
    return json(
        data_json,
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,HEAD,GET,POST',
            'Access-Control-Allow-Headers': 'x-requested-with'},
        status=200
    )
