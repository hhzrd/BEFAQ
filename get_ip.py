# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-02-05 14:35:28
LastEditTime: 2020-08-13 21:37:43
@Description: 查询本机ip地址
'''
import socket


def get_host_ip():
    '''
    Author: xiaoyichao
    param {type}
    Description: 查询本机ip地址
    '''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
