# BEFAQ

**BEFAQ(BERT Embedding FAQ)** 开源项目是好好住面向FAQ集合的问答系统框架。</br>
<br>我们将Sentence BERT模型应用到FAQ问答系统中。开发者可以使用BEFAQ系统快速构建和定制适用于特定业务场景的FAQ问答系统。</br>

## BEFAQ的优点有：

<br>（1）使用了Elasticsearch、Faiss、Annoy 作为召回引擎</br>
<br>（2）使用了Sentence BERT 语意向量（Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks）</br>
<br>（3）对同义问题有很好的支持</br>
<br>（4）支持多领域语料（保证了召回的数据是对应领域的，即使是同样的问题，也可以得到不同的答案。）</br>


## BEFAQ的框架结构如下图
![image](https://github.com/hhzrd/BEFAQ/blob/master/image/BEFAQ%20%E6%A1%86%E6%9E%B6.png)


## 如何使用

docker方式和非docker方式
### 1、安装Es7.6.1和配套的kibana，配置Es的IK分词器和同义词功能
### 1.1、使用docker(其中已经安装Es7.6.1、kibana、IK分词器和同义词功能)
通过docker的方式来使用ES，IK分词器的自定义词典和同义词功能需要用户进入到docker中来自行添加字典和同义词。

#### 1.2、在本机安装Es7.6.1和配套的kibana，配置Es的IK分词器和同义词功能
请参考博客[ES（Elasticsearch）7.6.1安装教程](https://blog.csdn.net/weixin_37792714/article/details/108025200)进行安装。如何已经配置过Es、IK分词器和同义词功能，可以略过这一步。但是记得把同义词同步到你的Es中。为了方便大家。相关文件的下载，都放在了百度网盘中，欢迎大家使用。链接:https://pan.baidu.com/s/1PxgINf6Q1UZBtcsYw6FU0w  密码:4q9h

在BEFAQ中，为了方便大家的使用，我们提供两种Elasticsearch的连接方式：使用用户名和密码的方式与不使用用户名密码的方式。如何修改请参看项目根目录下的es/es.ini 配置文件中的说明。在我们的博客中，我们提供了Elasticsearch配置用户名和密码的方式。


### 2、下载项目代码并创建BEFAQ的虚拟环境

    conda create -n befaq python=3.6 -y
    source activate befaq
    git clone https://github.com/hhzrd/BEFAQ.git
    进入BEFAQ的根目录，然后
    pip install -r requirements.txt

### 3、sentence-transformers 多语言预训练模型的下载

    首先进入到项目的根目录，然后
    cd model
    wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/distiluse-base-multilingual-cased.zip
    unzip distiluse-base-multilingual-cased.zip

### 4、excel数据格式
    如果你想要先跑通代码尝试一下。可以先不配置自己的数据。

    excel表格请放置在项目根目录下的 data/文件下，例如目前是示例文件名为“线上用户反馈回复.xls” excel数据是QA数据的来源，其中的数据会被写入到Es中。大家下载源码后，可以打开这个文件具体看一下数据示例。

    sheet的名称表示不同的领域，比如，我的第一个领域，叫做“领域1”。其中，第一列是“数据填写人姓名”，可以为空。第二列是“答案”，不允许为空。第三列是“原始问题”，不允许为空。第三列以后是“同义问题”，同义问题的数量没有限制。可以有很多同义问题，也可以一个同义问题都没有。一行一条数据。

    sheet名为“词典”的，放置的是用户词典。比如，我不想让“好好住”这个词在分词的过程中被切开。就把这个词放置在词典中。一行一条数据。程序会自动读取到指定位置(用于jieba分词)，但是Es中IK分词器的自定义词典需要自己添加
    sheet名为“停用词”的，放置的是停用词词典。一行一条数据。程序会自动读取到指定位置。
    sheet名为“同义词”的，是放置同义词的sheet。第一列是原义词，第二列及其之后是同义词。比如，番茄和西红柿是同义词。第一行列放番茄，第二列放西红柿。一行一条数据。同义词的数据需要自己写到Es的同义词表中，具体参看我上边提到ES（Elasticsearch）7.6.1安装教程的博客。因为你当下的服务器未必是Es的服务器，所以这里并没有用程序直接写入。

    同义词，词典，停用词。多个领域共用。词典，停用词是给BEFAQ的jieba分词使用的。同义词是给Es使用的。

    你可以在Excel中写上很多领域的数据，但是具体读取哪些领域的数据，项目根目录下的sheetname.conf中可以配置。

### 5、修改BEFAQ的配置文件

    项目根目录下的data/线上用户反馈回复.xls 是QA数据的来源，其中的数据会被写入到Es中。如果你想要先跑通代码尝试一下。可以先不配置自己的数据。
    项目根目录下的sheetname.conf 是读取Excel文档数据的配置文件。如果你想要先跑通代码尝试一下。可以先不修改这里的配置。
    项目根目录下的es/es.ini 是BEFAQ关于ES的配置文件。这个配置文件即使是想要先跑通代码尝试一下，也是需要修改的。这个配置文件里需要配置Es的IP（域名）和端口号，Es的登陆的用户名和密码。一定要根据自己的Es的配置进行修改，才能让BEFAQ连接上你的Es。
    项目根目录下的faq/befaq_conf.ini 是BEFAQ的配置文件。如果你想要先跑通代码尝试一下。可以先不修改这里的配置。


### 6、如何开启BEFAQ服务

    进入项目的根目录，然后
    cd es

    将数据从excel 写到ES
    python write_data2es.py

    将问题处理成Sentence BERT 向量，保存到bin类型文件中，便于后期读取问题的向量。
    python write_vecs2bin.py

    训练Faiss和Annoy模型
    python train_search_model.py

    进入项目的根目录(cd ..)，然后
    cd faq

    启动BEFAQ服务 （如果数据没有发生变化，后期启动服务只需要进行这一步）
    python main_faq.py
    或者在后台中启动
    nohup python -u main_faq.py > "logs/log$(date +"%Y-%m-%d-%H").txt" 2>&1 &
    

    在终端中测试BEFAQ。BEFAQ的服务是post请求。(将xxx.xx.xx.xx替换成自己的ip)
    
    curl -d "question=忘记原始密码怎么修改密码&get_num=3&threshold=0.5&owner_name=领域3"   http://xxx.xx.xx.xx:8129/BEFAQ
    
    接口url:
    http://xxx.xx.xx.xx:8129/BEFAQ
    接口参数说明
    question：用户的问题。必需
    get_num：接口最多返回几条数据。非必需，默认为3
    threshold：阈值，相似度高于或等于这个阈值的数据才会被接口返回。非必需，默认为0.5
    owner_name：数据所有者的名称，也就是excel中每个领域的数据对应的sheet name。用来区分多领域数据。必需
    
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


### 7、如何开启BEFAQ 的联想词接口服务

    如果想要启动根据当前输入联想问题的功能。
    进入项目根目录，然后
    cd es
    python associative_questions_server.py

    在终端中测试联想功能。服务是post请求。(将xxx.xx.xx.xx替换成自己的ip)
    curl -d "current_question=设计师&limit_num=3&owner_name=领域1&if_middle=1"  http://xxx.xx.xx.xx:8128/associative_questions
    
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

## Authors

<br>该项目的主要贡献者有:</br>
* [肖轶超](https://github.com/xiaoyichao)（好好住）
* [徐忠杰](https://github.com/461025412)（好好住）
* [王得祥](https://github.com/oksite)（好好住）
* [向泳州](https://github.com/XiangYongzhou)（好好住）
* [辛少普](https://github.com/hhzrd)（好好住）

## 参考文献：

<br>[1] [百度AnyQ](https://github.com/baidu/AnyQ)</br>
<br>[2] [sentence-transformers](https://github.com/UKPLab/sentence-transformers)</br>
<br>[3] [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)</br>

## Copyright and License

BEFAQ is provided under the [Apache-2.0 license](https://github.com/baidu/AnyQ/blob/master/LICENSE).