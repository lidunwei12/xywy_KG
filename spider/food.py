# -*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup

"""
time:6.3.2020
Author:bob.lee

"""


class SpiderXywyFoods():
    """
    基于寻医问药网食材数据收集
    """

    def __init__(self):
        self.food_url_json_path = "../data/json/food.json"
        self.food_error_path = "../data/error.txt"
        self.main_url = "http://www.xywy.com/caipu/main_1500.html"
        self.food_json_path = "../data/json/food.json"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}

    def requestRespnse(self, url):
        """
        get请求网页
        :param url: 请求网址
        :return: 网址html内容
        """
        response = requests.get(url, headers=self.headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def getFood(self, url):
        """
        收集单个食材的属性
        :param url: 食材url
        :return: 食材数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result["名字"] = ''.join(re.findall(r'(.+?)_食谱', soup.title.text))
        for element in soup.find_all(class_="food-info fl graydeep"):
            for element_one in element.find_all("p"):
                temp = element_one.get_text()
                if temp.find("原料别名") != -1:
                    result["原料别名"] = re.sub(re.compile('原料别名：'), '', temp)
                if temp.find("原料分类") != -1:
                    result["原料分类"] = re.sub(re.compile('原料分类：'), '', temp)
                if temp.find("食用提示") != -1:
                    result["食用提示"] = re.sub(re.compile('食用提示：'), '', temp)
                if temp.find("禁忌人群") != -1:
                    result["禁忌人群"] = re.sub(re.compile('禁忌人群：'), '', temp)
                if temp.find("适应人群") != -1:
                    result["适应人群"] = re.sub(re.compile('适应人群：'), '', temp)
        fitting = []
        hating = []
        for element in soup.find_all(class_="panels1 clearfix"):
            for element_one in element.find_all(class_="tab-item1 panel"):
                for element_two in element_one.find_all("dl"):
                    temp = element_two.get_text()
                    if temp[0:10].find("原料介绍") != -1:
                        result["原料介绍"] = re.sub(re.compile('\r|\n|\t|原料介绍|'), '', temp)
                    if temp[0:10].find("营养分析") != -1:
                        result["营养分析"] = re.sub(re.compile('\r|\n|\t|营养分析|'), '', temp)
                    if temp[0:10].find("食用指导") != -1:
                        result["食用指导"] = re.sub(re.compile('\r|\n|\t|食用指导|'), '', temp)
                    if temp[0:10].find("食疗作用") != -1:
                        result["食疗作用"] = re.sub(re.compile('\r|\n|\t|食疗作用|'), '', temp)
                    if temp[0:10].find("食材文化") != -1:
                        result["食材文化"] = re.sub(re.compile('\r|\n|\t|食材文化|'), '', temp)
                    if temp[0:10].find("温馨提示") != -1:
                        result["温馨提示"] = re.sub(re.compile('\r|\n|\t|温馨提示|'), '', temp)
                for element_two in element.find_all(class_="tab-item1 panel none"):
                    for element_three in element_two.find_all(class_="common-wrap1 mt10"):
                        for element_four in element_three.find_all("a"):
                            hating.append(element_four.get_text())
                    for element_three in element_two.find_all(class_="common-dl1 clearfix"):
                        if str(element_three).find("相宜") != -1:
                            for element_four in element_three.find_all("a"):
                                fitting.append(element_four.get_text())
        result["相宜"] = fitting
        result["相克"] = hating
        return result

    def getFoodAll(self):
        """
        获取全部食材网址
        :return: 
        """
        data = []
        soup = self.requestRespnse(self.main_url)
        for element in soup.find_all(class_="left_mk"):
            for element_one in element.find_all("li"):
                for element_two in element_one.find_all("a"):
                    data.append("http://www.xywy.com/caipu/" + element_two["href"])
        result = {}
        result["url"] = data
        with open(self.food_url_json_path, "w") as dump_f:
            json.dump(result, dump_f)

    def foodCollection(self):
        """
        全部食材及属性数据收集
        :return: json文件
        """
        result = []
        f = open(self.food_error_path, 'w', encoding='utf8')
        with open(self.food_url_json_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for element in data_json["url"]:
                try:
                    result.append(self.getFood(element))
                except:
                    print(element)
                    f.write(element + '\n')
        f.close()
        data = {}
        data["data"] = result
        with open(self.food_json_path, "w") as dump_f:
            json.dump(data, dump_f)


if __name__ == '__main__':
    # with open("../data/json/food.json", encoding='utf8') as dump_f:
    #     data_json = json.load(dump_f)
    #     for element in data_json["data"]:
    #         print(element['相宜'],element['相克'],element['名字'])
    print(SpiderXywyFoods().foodCollection())
