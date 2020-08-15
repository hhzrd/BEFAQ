(一)BEFAQ
BEFAQ(BERT Embedding FAQ) 开源项目是好好住面向FAQ集合的问答系统框架

开发者可以使用BEFAQ系统快速构建和定制适用于特定业务场景的FAQ问答系统，并加速迭代和升级。
BEFAQ的优点有：
（1）使用了ES、Faiss、Annoy 作为召回引擎
（2）使用了Sentence BERT向量
（3）对同义问题有更好的支持
（4）支持多领域语料（同样的问题，不同的用户角色，可以得到不同的答案）


(二)详细介绍
1、安装ES7.6.1和配套的kibana，配置ES的IK分词器和同义词功能，请参考我的博客：https://blog.csdn.net/weixin_37792714/article/details/108025200


2、创建BEFAQ的虚拟环境
    conda create -n befaq python=3.6 
    source activate befaq
    <!-- 进入BEFAQ的根目录，然后 -->
    pip install -r requirements.txt

3、sentence-transformers 多语言预训练模型的下载
    首先进入到项目的根目录，然后
    cd data/model
    wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/distiluse-base-multilingual-cased.zip
    unzip distiluse-base-multilingual-cased.zip


4、如何开启BEFAQ服务
    进入项目的根目录，然后
    cd es
    <!-- 将数据从excel 写到ES -->
    python write_data2es.py
    <!-- 将问题处理成Sentence BERT 向量，保存到bin类型文件中，便于后期读取问题的向量。 -->
    python write_vecs2bin.py
    <!-- 训练Faiss和Annoy模型 -->
    python train_search_model.py
    进入项目的根目录(cd  ..)，然后
    <!-- 启动BEFAQ服务 （如果数据没有发生变化，后期启动服务只需要进行这一步） -->
    cd faq
    python main_faq.py 
    <!-- 在终端中测试BEFAQ。BEFAQ的服务是post请求。(将xxx.xx.xx.xx替换成自己的ip) -->
    curl -d "question=忘记原始密码怎么修改密码&get_num=3&threshold=0.5&owner_name=领域1"   http://xxx.xx.xx.xx:8129/BEFAQ
    
    接口url:
    http://xxx.xx.xx.xx:8129/BEFAQ
    接口参数说明
    question：用户的问题。必需
    get_num：接口最多返回几条数据。非必需，默认为3
    threshold：阈值，相似度高于这个阈值的数据才会被接口返回。非必需，默认为0.5
    owner_name：数据所有者的名称，用来区分多领域数据。必需
    
    返回的数据格式：
    [
        {
            "q_id": 5,
            "specific_q_id": 10,
            "question": "忘记原始密码如何修改密码？",
            "answer": "您可在登录界面，密码登录，使用找回密码功能进行验证。",
            "confidence": 0.99
        }
    ]


5、BEFAQ的配置文件
    es/stopwords4_process_question_dedup.txt 是BEFAQ的停用词表。
    es/userdict.txt  是BEFAQ的用户字典表。
    es/es.ini 是BEFAQ关于ES的配置文件。
    faq/befaq_conf.ini 是BEFAQ的配置文件。


6、如何开启BEFAQ 的联想词接口服务
    如何想要启动根据当前输入联想问题的功能，支持多进程。
    进入项目根目录，然后
    cd es
    python associative_questions_server.py

    在终端中测试联想功能。服务是post请求。(将xxx.xx.xx.xx替换成自己的ip)
    curl -d "current_question=设计师&limit_num=3&owner_name=领域1&if_middle=1"   http://xxx.xx.xx.xx:8128/associative_questions
    
    接口url:
    http://xxx.xx.xx.xx:8128/associative_questions
    接口参数说明
    current_question:
    limit_num：接口最多返回几条数据。必需
    owner_name：数据所有者的名称，用来区分多领域数据。必需
    if_middle:是否允许用户当前输入的内容在中间的位置。非必需。默认为1，1为允许，0为不允许。


    返回的数据格式：
    {
        "code": "1",
        "msg": "OK",
        "data": {
            "message": [
                "按地区找设计师",
                "设计师可以选择同城吗",
                "怎样把个人设计师转成机构设计师"
            ]
        }
    }

Authors

该项目的主要贡献者是:
    肖轶超（好好住）
    徐忠杰（好好住）
    王得祥（好好住）
    向泳州（好好住）
    辛少普（好好住）

参考文献：
    百度AnyQ  https://github.com/baidu/AnyQ

Copyright and License
BEFAQ is provided under the Apache-2.0 license.