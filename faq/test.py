# coding=UTF-8
'''
Author: xiaoyichao
LastEditors: xiaoyichao
Date: 2021-03-10 11:31:23
LastEditTime: 2021-03-10 11:34:40
Description: 
'''
import docker_host_ip

print(docker_host_ip.get_ip_within_host())
print(docker_host_ip.get_docker_host_ip())