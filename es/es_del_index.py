# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-01-02 16:55:23
LastEditTime: 2020-08-21 17:49:09
@Description: 删除ES的索引， del_index_name 是要删除的索引的名字

'''

from es_operate import ESCURD
from elasticsearch import Elasticsearch
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import configparser
import create_connection
import json
import os
import sys
import datetime


dir_name = os.path.abspath(os.path.dirname(__file__))
es_config = configparser.ConfigParser()
es_config.read(os.path.join(dir_name, "es.ini"))
es_server_ip_port = es_config["ServerAddress"]["es_server_ip_port"]


index_name_1 = es_config["ServerInfo"]["index_name_1"]
index_name_2 = es_config["ServerInfo"]["index_name_2"]

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
#     es_faq.del_index(index_name=index_name_1)
#     es_faq.del_index(index_name=index_name_2)
