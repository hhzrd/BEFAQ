# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-19 19:01:17
LastEditTime: 2020-08-25 18:03:58
@Description: 删除索引，仅供测试。
'''

from es_operate import ESCURD
from elasticsearch import Elasticsearch

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import create_connection
import configparser

dir_name = os.path.abspath(os.path.dirname(__file__))
es_config = configparser.ConfigParser()
es_config.read(os.path.join(dir_name, "es.ini"))
es_server_ip_port = es_config["ServerAddress"]["es_server_ip_port"]


# 使用配置文件中的index_name，也可以自己命名，创建其他名称的索引
index_name = es_config["ServerInfo"]["index_name_1"]

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

# if __name__ == "__main__":
#     owner_names = ["领域1,领域2,领域3"]
#     for owner_name in owner_names:
#         es_faq.del_data(index_name, owner_name)
