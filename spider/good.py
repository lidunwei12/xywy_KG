# -*- coding: utf-8 -*-

"""
time:6.3.2020
Author:bob.lee

"""
import re
import json
import requests
from bs4 import BeautifulSoup


class SpiderXywyGoods():
    """
    基于寻医问药网药品数据收集
    """

    def __init__(self):
        self.good_json_path = "../data/json/good.json"
        self.good_url_json_path = "../data/json/good_url.json"
        self.main_url = "http://jck.xywy.com/"
        self.error_path = "../data/error.txt"
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

    def getGoods(self, url):
        """
        单个药品属性数据收集
        :param url: 药品url
        :return: 单个药品数据包
        """
        result = {}
        soup = self.requestRespnse(url)
        result["名字"] = ''.join(re.findall(r'(.+?)说明书_', soup.title.text))
        for element in soup.find_all(class_="d-info-dl mt20"):
            for element_one in element.find_all(class_="clearfix"):
                temp = element_one.get_text()
                if temp[0:10].find("批准文号") != -1:
                    result["批准文号"] = re.sub(re.compile('批准文号：'), '', temp)
                if temp[0:10].find("功能主治") != -1:
                    result["功能主治"] = re.sub(re.compile('功能主治：'), '', temp)
                if temp[0:10].find("生产企业") != -1:
                    result["生产企业"] = re.sub(re.compile('生产企业：'), '', temp)
                if temp[0:10].find("相关疾病") != -1:
                    result["相关疾病"] = [element_two.get_text() for element_two in element_one.find_all('a')]
                    # result["相关疾病"] = re.sub(re.compile('相关疾病：'), '', temp)
        for element in soup.find_all(class_="d-tab-con-box"):
            for element_one in element.find_all(class_="d-tab-con padd20"):
                for element_two in element_one.find_all("p"):
                    temp = re.sub(re.compile('\r|\n|\t​'), '', str(element_two.get_text()).replace(' ', ""))
                    if temp[0:10].find("通用名称") != -1:
                        result["通用名称"] = temp.replace("通用名称：", "")
                    if temp[0:10].find("功能主治") != -1:
                        result["功能主治"] = temp.replace("功能主治：", "")
                    if temp[0:10].find("用法用量") != -1:
                        result["用法用量"] = temp.replace("用法用量：", "")
                    if temp[0:10].find("剂型") != -1:
                        result["剂型"] = temp.replace("剂型：", "")
                    if temp[0:10].find("不良反应") != -1:
                        result["不良反应"] = temp.replace("不良反应：", "")
                    if temp[0:10].find("禁忌") != -1:
                        result["禁忌"] = temp.replace("禁忌：", "")
                    if temp[0:10].find("注意事项") != -1:
                        result["注意事项"] = temp.replace("注意事项：", "")
                    if temp[0:10].find("成份") != -1:
                        result["成份"] = temp.replace("成份：", "")
                    if temp[0:10].find("性状") != -1:
                        result["性状"] = temp.replace("性状：", "")
                    if temp[0:10].find("药物相互作用") != -1:
                        result["药物相互作用"] = temp.replace("药物相互作用：", "")
                    if temp[0:10].find("贮藏") != -1:
                        result["贮藏"] = temp.replace("贮藏：", "")
                    if temp[0:10].find("执行标准") != -1:
                        result["执行标准"] = temp.replace("执行标准：", "")
                    if temp[0:10].find("药理作用") != -1:
                        result["药理作用"] = temp.replace("药理作用：", "")
                    if temp[0:10].find("药物相互作用") != -1:
                        result["药物相互作用"] = temp.replace("药物相互作用：", "")
                    if temp[0:10].find("药物过量") != -1:
                        result["药物过量"] = temp.replace("药物过量：", "")
        result["url"] = url
        return result

    def getUrlGood(self):
        """
        全部药品url数据收集
        :return: 
        """
        for i in range(1, 367):
            soup = SpiderXywyGoods().requestRespnse("http://yao.xywy.com/class/4-0-0-1-0-" + str(i) + ".htm")
            for element in soup.find_all(class_="fl h-drugs-pic bor"):
                for element_one in element.find_all("a"):
                    result.append("http://yao.xywy.com" + element_one["href"])
        data = {}
        data["data"] = result
        with open(self.good_url_json_path, "w") as dump_f:
            json.dump(data, dump_f)

    def goodCollection(self):
        """
        获取全部药品全部属性数据
        :return: json文件
        """
        result = []
        count = 0
        f = open(self.error_path, 'w', encoding='utf8')
        with open(self.good_url_json_path, encoding="utf8") as dump_f:
            data_json = json.load(dump_f)
            for element in data_json["data"]:
                try:
                    temp = self.getGoods(element)
                    if temp["名字"] != "":
                        result.append(temp)
                        count = count + 1
                        print(count)
                except:
                    print(element)
                    f.write(element + '\n')
        f.close()
        data = {}
        data["data"] = result
        with open(self.good_json_path, "w") as dump_f:
            json.dump(data, dump_f)


if __name__ == '__main__':
    print(SpiderXywyGoods().getGoods("http://yao.xywy.com/goods/41942.htm"))
