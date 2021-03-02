# coding=UTF-8
'''
Author: xiaoyichao
LastEditors: xiaoyichao
Date: 2020-08-13 11:34:47
LastEditTime: 2021-03-02 14:28:15
Description: 用于读取excel表格的类
'''
import os
import sys
import xlrd
import configparser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

dir_name = os.path.abspath(os.path.dirname(__file__))


class ExcelData(object):

    def __init__(self):
        self.excel_config = configparser.ConfigParser()
        self.excel_config.read(os.path.join(dir_name, "../sheetname.conf"))
        self.sheet_names = self.excel_config["QA_sheets"]["sheets"].split(",")
        self.excel_name = self.excel_config["excel_name"]["name"]
        self.synonyms_sheet = self.excel_config["Synonyms"]["sheet"]
        self.stopwords_sheet = self.excel_config["Stopwords"]["sheet"]
        self.excel_file = os.path.join(dir_name, "../data/", self.excel_name)
        self.id = 0

    def get_sheet_names(self):
        '''
        Author: xiaoyichao
        param {type}
        Description: 返回要读取的sheet的名称组成的list
        '''
        return self.sheet_names

    def read_sheet(self, sheet_name):
        '''
        Author: xiaoyichao
        param {type}
        Description: 读取excel中某个sheet的数据
        '''
        try:
            book = xlrd.open_workbook(filename=self.excel_file)
            table = book.sheet_by_name(sheet_name)
            nrows = table.nrows
            ncols = table.ncols
            sheet_list = []
            for row in range(1, nrows):
                for col in range(2, ncols):
                    cell_value = table.cell(row, col).value
                    if cell_value != "":
                        q_id = row
                        original_question = cell_value
                        answer = table.cell(row, 1).value
                        self.id += 1
                        owner_name = sheet_name
                        sheet_list.append(
                            [q_id, original_question, answer, self.id, owner_name])
            return sheet_list
        except Exception:
            print("Exception")
            return []

    def read_QA_data(self):
        '''
        Author: xiaoyichao
        param {type}
        Description: 读取excel中的问答数据
        '''
        excel_list = []
        for sheet_name in self.sheet_names:
            sheet_list = self.read_sheet(sheet_name)
            excel_list.append(sheet_list)
        return excel_list


# exceldata = ExcelData()
# excel_list = exceldata.read_QA_data()
# print(excel_list)
