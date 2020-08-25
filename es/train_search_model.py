# coding=UTF-8
'''
@Author: xiaoyichao
LastEditors: xiaoyichao
@Date: 2020-06-19 17:14:35
LastEditTime: 2020-08-25 18:05:41
@Description: 
'''
from read_excel import ExcelData
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from search_engines_operate import SearchEngine

exceldata = ExcelData()
sheet_names = exceldata.get_sheet_names()
search_engine = SearchEngine()

for sheet_name in sheet_names:
    search_engine.train_annoy(owner_name=sheet_name)
    search_engine.train_faiss(owner_name=sheet_name)
