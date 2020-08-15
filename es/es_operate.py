# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-05-21 15:31:50
LastEditTime: 2020-08-13 21:09:16
@Description: ES相关操作的类

'''
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime


class ESCURD(object):
    def __init__(self, es):
        self.es = es

    def create_index(self, index_name):
        '''
        @Author: xiaoyichao
        @param {type}
        @Description: 创建索引
        '''

        # 实现中文搜索提示
        mappings_cn = {
            "settings": {
                "index.max_ngram_diff": 10,
                "number_of_shards": 5,
                "number_of_replicas": 1,
                "analysis": {
                    "filter": {
                        "local_synonym": {
                            "type": "synonym",
                            "synonyms_path": "synonyms/synonym.txt"
                        },
                        "edge_ngram_filter": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 50
                        }
                    },
                    "analyzer": {
                        "text_ik": {
                            "type": "custom",
                            "tokenizer": "ik_smart",
                            "filter": ["lowercase"]
                        },
                        "text_ik_s": {
                            "type": "custom",
                            "tokenizer": "ik_smart",
                            "filter": [
                                "lowercase",
                                "local_synonym"
                            ]
                        },
    
                        "save_origin_split": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase"
                            ]
                        },
                        "keyword_cn": {
                            "type": "custom",
                            "tokenizer": "keyword",
                            "filter": [
                                "lowercase",
                                "edge_ngram_filter"
                            ]
                        },
                        "ngram_tokenizer_analyzer": {
                            "type": "custom",
                            "tokenizer": "ngram_tokenizer",
                            "filter": [
                                "lowercase"
                            ]
                        }

                    },
                    "tokenizer": {
                        "ngram_tokenizer": {
                            "type": "ngram",
                            "min_gram": 1,
                            "max_gram": 6,
                            "token_chars": [
                                "letter",
                                "digit"]
                        }

                    }
                }
            },
            "mappings": {
                "properties": {
                    "original_question": {
                        "type": "text",
                        "analyzer": "save_origin_split",
                        "search_analyzer": "save_origin_split"
                    },
                    "original_question_cn_left": {
                        "type": "text",
                        "analyzer": "keyword_cn",
                        "search_analyzer": "keyword"
                    },
                    "original_question_cn_middle": {
                        "type": "text",
                        "analyzer": "ngram_tokenizer_analyzer",
                        "search_analyzer": "keyword"
                    },
                    "process_question": {
                        "type": "text",
                        "analyzer": "text_ik",
                        "search_analyzer": "text_ik_s"
                    },
                    "answer": {
                        "type": "text"
                    },
                    "q_id": {
                        "type": "integer"
                    },
                    "specific_q_id": {
                        "type": "integer"
                    },
                    "id": {
                        "type": "integer"
                    },
                    "owner_name": {
                        "type": "keyword"
                    }
                }
            }
        }
        

        # 测试
        mappings_cn = {
            "settings": {
                "index.max_ngram_diff": 10,
                "number_of_shards": 5,
                "number_of_replicas": 1,
                "analysis": {
                    "filter": {
                        "local_synonym": {
                            "type": "synonym",
                            "synonyms_path": "synonyms/synonym.txt"
                        },
                        "edge_ngram_filter": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 50
                        }
                    },
                    "analyzer": {
                        "text_ik": {
                            "type": "custom",
                            "tokenizer": "ik_smart",
                            "filter": ["lowercase"]
                        },
                        "text_ik_s": {
                            "type": "custom",
                            "tokenizer": "ik_smart",
                            "filter": [
                                "lowercase",
                                "local_synonym"
                            ]
                        },
    
                        "save_origin_split": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase"
                            ]
                        },
                        "keyword_cn": {
                            "type": "custom",
                            "tokenizer": "keyword",
                            "filter": [
                                "lowercase",
                                "edge_ngram_filter"
                            ]
                        },
                        "ngram_tokenizer_analyzer": {
                            "type": "custom",
                            "tokenizer": "ngram_tokenizer",
                            "filter": [
                                "lowercase"
                            ]
                        }

                    },
                    "tokenizer": {
                        "ngram_tokenizer": {
                            "type": "ngram",
                            "min_gram": 1,
                            "max_gram": 6,
                            "token_chars": [
                                "letter",
                                "digit"]
                        }

                    }
                }
            },
            "mappings": {
                "properties": {
                    "original_question": {
                        "type": "text",
                        "analyzer": "save_origin_split",
                        "search_analyzer": "save_origin_split"
                    },
                    "original_question_cn_left": {
                        "type": "text",
                        "analyzer": "keyword_cn",
                        "search_analyzer": "keyword"
                    },
                    "original_question_cn_middle": {
                        "type": "text",
                        "analyzer": "ngram_tokenizer_analyzer",
                        "search_analyzer": "keyword"
                    },
                    "process_question": {
                        "type": "text",
                        "analyzer": "text_ik",
                        "search_analyzer": "text_ik_s"
                    },
                    "answer": {
                        "type": "text"
                    },
                    "q_id": {
                        "type": "integer"
                    },
                    "specific_q_id": {
                        "type": "integer"
                    },
                    "id": {
                        "type": "integer"
                    },
                    "owner_name": {
                        "type": "keyword"
                    }
                }
            }
        }


        if self.es.indices.exists(index=index_name) == True:
            print("索引 %s 之前已经存在" % index_name)
        else:
            self.es.indices.create(index=index_name, body=mappings_cn)
            print("成功创建索引: %s" % index_name)

    def del_index(self, index_name):
        # 删除索引
        if self.es.indices.exists(index=index_name) == True:
            res = self.es.indices.delete(index_name)
            print("删除索引:", index_name)
            return res
        else:
            print("想要删除的索引 %s 不存在" % index_name)
            return

    def del_data(self, index_name, owner_name):
        # 删除owner_name对用的数据
        query = {'query': {'match': {'owner_name': owner_name}}}

        res = self.es.delete_by_query(
            index=index_name,  body=query)
        print("删除数据:", res)

    def insert_more(self, index_name, actions, owner_name):
        '''
        @Author: xiaoyichao
        @param {type}：
        @Description: 添加多条数据

        '''
        res, _ = bulk(self.es, actions, index=index_name,
                      raise_on_error=True)
        print("%s 向ES中添加了%d条数据" % (owner_name, res))

    def search_data(self, index_name, owner_name, query_word_list, limit_num):
        '''
        @Author: xiaoyichao
        @param {type}
        @Description: 查询ES数据
        '''
        limit_num = int(limit_num)

        should_list = []
        for word in query_word_list:
            match = {
                "match": {
                    "process_question": word
                }
            }
            should_list.append(match)
        bool_inside_value = {"should": should_list}
        list_must_value_2 = {}
        list_must_value_2["bool"] = bool_inside_value

        list_must_value_1 = [
            {
                "match_phrase": {
                    "owner_name": owner_name
                }
            }
        ]

        must_list = []
        must_list.append(list_must_value_1)
        must_list.append(list_must_value_2)

        dic_bool_value = {}
        dic_bool_value["must"] = must_list

        dic_bool = {}
        dic_bool["bool"] = dic_bool_value

        doc = {}
        doc["query"] = dic_bool
        doc["_source"] = ["q_id", "process_question",
                          "original_question", "answer", "specific_q_id"]
        doc["size"] = limit_num

        print("ES查询语句：", doc)

        res = self.es.search(
            index=index_name, body=doc)
        return res

    def search_cn(self, index_name, owner_name, current_question, search_limit_num, if_middle=True):
        '''
        @Author: xiaoyichao
        @param {type}
        @Description: 查询中文提示词
        '''
        search_limit_num = int(search_limit_num)

        doc = {}
        if if_middle:  # 从中间开始搜索

            doc["query"] = {
                "bool": {
                    "must": [
                        [
                            {
                                "match": {
                                    "owner_name": owner_name
                                }
                            },
                            {
                                "match": {"original_question_cn_middle": current_question}
                            }

                        ]]
                }
            }

        else:

            doc["query"] = {
                "bool": {
                    "must": [
                        [
                            {
                                "match": {
                                    "owner_name": owner_name
                                }
                            },
                            {
                                "match": {"original_question_cn_left": current_question}
                            }

                        ]]
                }
            }
        doc["_source"] = ["original_question", "q_id"]
        doc["size"] = search_limit_num

        # print("ES查询语句：", doc)

        res = self.es.search(
            index=index_name, body=doc)
        return res

    def search4search_engine(self, index_name,  owner_name, question):
        '''
        @Author: xiaoyichao
        @param {type}
        @Description: 查询annoy或faiss检索出的question的对应信息，例如q_id等
        '''
        doc = {}

        doc["query"] = {
            "bool": {
                "must": [
                        [
                            {
                                "match": {
                                    "owner_name": owner_name
                                }
                            },
                            {
                                "match_phrase": {"original_question": question}
                            }

                        ]]
            }
        }

        doc["_source"] = ["q_id", "specific_q_id","process_question",
                          "original_question", "answer"]

        print("ES查询语句：", doc)

        res = self.es.search(
            index=index_name,  body=doc)
        return res

    def es_put_alias(self, index_name, alias_name):
        '''
        Author: xiaoyichao
        param {type}
        Description: 添加别名和索引的连接
        '''
        res = self.es.indices.put_alias(index=index_name, name=alias_name)
        print("添加别名%s和索引%s的连接" % (alias_name, index_name))
        return res

    def es_get_alias(self, alias_name):
        '''
        Author: xiaoyichao
        param {type}
        Description: 获取当前别名下的索引
        '''
        try:
            res = self.es.indices.get_alias(name=alias_name)
            current_index = list(res.keys())[0]
            print("获取当前别名%s下的索引" % alias_name)
            return current_index
        except Exception:
            return

    def es_del_alias(self, index_name, alias_name):
        '''
        Author: xiaoyichao
        param {type}
        Description: 删除别名和索引的连接
        '''
        try:
            res = self.es.indices.delete_alias(
                index=index_name, name=alias_name)
            print("删除别名%s和索引%s的连接" % (alias_name, index_name))
            return res
        except Exception:
            return
