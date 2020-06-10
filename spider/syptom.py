# -*- coding: utf-8 -*-
"""
time:6.3.2020
Author:bob.lee

"""

import re
import json
import requests
from bs4 import BeautifulSoup


class SpiderXywySyptom():
    """
    基于寻医问药网症状数据收集
    """

    def __init__(self):
        self.error_path = "../data/error.txt"
        self.symptom_json_path = "../data/json/symptom.json"
        self.base_url = "http://zzk.xywy.com/"
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

    def getSyptomCause(self, url):
        """
        症状病因数据收集
        :param url: 症状病因url
        :return: 症状病因数据json包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['病因'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getSyptomPrevention(self, url):
        """
        症状病因预防收集
        :param url: 预防url
        :return: 预防数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['预防'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getSyptomCheck(self, url):
        """
        症状检查数据
        :param url: 检查url
        :return: 检查json数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['检查'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        check_temp = []
        for element in soup.find_all(class_="zz-articl fr f14"):
            for element_one in element.find_all(class_="f12 mt5"):
                for element_two in element_one.find_all("a"):
                    temp = element_two.get_text()
                    check_temp.append(temp)
        result['相关检查'] = check_temp
        return result

    def getSyptomIdentify(self, url):
        """
        症状诊断数据收集
        :param url: 诊断url
        :return: json文件
        """
        soup = self.requestRespnse(url)
        result = {}
        result['诊断鉴别'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getSyptomBase(self, url):
        """
        症状基本数据收集
        :param url: 症状介绍url
        :return: json文件
        """
        soup = self.requestRespnse(url)
        result = {}
        result['名称'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all(class_="jb-name fYaHei gre")]))
        result['介绍'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getSyptomFood(self, url):
        """
        症状食物数据收集
        :param url: 食物url
        :return: 食物json
        """
        soup = self.requestRespnse(url)
        result = {}
        result["忌吃食物"] = [re.sub(re.compile('\r|\n|\t| |'), '', str(element_one.get_text())) for element in
                          soup.find_all(class_="diet-item none") for element_one in
                          element.find_all(class_="diet-opac-txt pa f12")]
        result["宜吃食物"] = [re.sub(re.compile('\r|\n|\t| |'), '', str(element_one.get_text())) for element in
                          soup.find_all(class_="diet-item clearfix") for element_one in
                          element.find_all(class_="diet-opac-txt pa f12")]
        return result

    def getSyptom(self, name):
        """
        单个症状属性数据收集
        :param name: 症状number
        :return: json数据
        """
        base_url = self.base_url + name + '_jieshao.html'
        cause_url = self.base_url + name + '_yuanyin.html'
        prevent_url = self.base_url + name + '_yufang.html'
        symptom_url = self.base_url + name + '.htm'
        check_url = self.base_url + name + '_jiancha.html'
        identify_url = self.base_url + name + '_zhenduan.html'
        food_url = self.base_url + name + '_food.html'
        result = self.getSyptomBase(base_url)
        result.update(self.getSyptomCause(cause_url))
        result.update(self.getSyptomPrevention(prevent_url))
        result.update(self.getSyptomCheck(check_url))
        result.update(self.getSyptomIdentify(identify_url))
        result.update(self.getSyptomFood(food_url))
        result.update({"id":name})
        return result

    def syptomCollection(self):
        """
        全部症状全部属性数据收集
        :return: json文件
        """
        result = []
        count = 0
        f = open(self.error_path, 'w', encoding='utf8')
        for i in range(1, 6912):
            try:
                result.append(self.getSyptom(str(i)))
                count = count + 1
                print(count)
            except:
                print(str(i) + "失败")
                f.write(str(i) + '\n')
        f.close()
        data = {}
        data["data"] = result
        with open(self.symptom_json_path, "w") as dump_f:
            json.dump(data, dump_f)


if __name__ == '__main__':
    print(SpiderXywySyptom().syptomCollection())
    # 6911
