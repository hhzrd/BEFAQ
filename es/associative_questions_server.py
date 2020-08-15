# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-12 08:15:51
LastEditTime: 2020-08-15 17:51:14
@Description: 
'''
import time
from sanic import Sanic
import sanic
import configparser
from es_search_cn import SearchData
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from response_xiao import res_xiao
from get_ip import get_host_ip

dir_name = os.path.abspath(os.path.dirname(__file__))
search_data = SearchData()


def print_usetime(begin_time, question, module):
    current_time = time.time()
    use_time = current_time - begin_time
    if use_time > 0.5:
        print("time more than 0.5")
    print("Q:%s,%s用时%f秒" % (question, module, use_time))


def kill_port(port):

    find_kill = "kill -9 $(lsof -i:%d -t)" % port
    print(find_kill)
    result = os.popen(find_kill)
    return result.read()


# 接口会返回json数据
app = Sanic()
app = Sanic("associative questions")


@app.route("/associative_questions", methods=["POST", "HEAD"])
async def associative_questions(request):

    begin_time = time.time()
    # 接收到的参数
    current_question = str(request.form.get("current_question"))
    limit_num = int(request.form.get("limit_num"))
    owner_name = str(request.form.get("owner_name"))
    if_middle = int(request.form.get("if_middle", default=1))
    if if_middle == 1:
        if_middle = True
    if if_middle == 0:
        if_middle = False
    else:
        if_middle = True

    maybe_original_questions = search_data.search_question_cn(
        owner_name=owner_name, current_question=current_question, limit_num=limit_num, if_middle=if_middle)

    print_usetime(begin_time=begin_time,
                  question=current_question, module="ES联想词")

    answer_json = {}
    answer_json["code"] = "1"
    answer_json["msg"] = "OK"
    answer_json["data"] = {
        "message": maybe_original_questions}
    return res_xiao(answer_json)


@app.route("/", methods=["GET", "HEAD"])
async def alibaba_operator_check(request):
    print("alibaba SLB checking server status")
    return sanic.response.text(200)


if __name__ == "__main__":
    this_ip = get_host_ip()

    root_config = configparser.ConfigParser()
    root_config.read(os.path.join(
        dir_name, "associative_questions_config.ini"))

    kill_port(int(root_config["ServerAddress"]["port"]))

    app.run(host=this_ip,
            port=int(root_config["ServerAddress"]["port"]),
            workers=int(root_config["ServerInfo"]["work_number"]),
            debug=True, access_log=True)
