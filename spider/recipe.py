# -*- coding: utf-8 -*-

"""
time:6.3.2020
Author:bob.lee

"""
import re
import requests
from bs4 import BeautifulSoup
import json



class SpiderXywyProjects():
    """
    基于寻医问药网检查项目数据收集
    """

    def __init__(self):
        self.project_json_path = "../data/project.json"
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
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def getProjects(self, url):
        """
        收集单个检查项目的属性
        :param url: 检查项目url
        :return: 检查项目数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        status = []
        text_temp = []
        for element in soup.find_all(class_="food-info fl graydeep green-a"):
            result["名字"]=[re.sub(re.compile("\r|\t|\n| |"),"",str(element_one.get_text())) for element_one in element.find_all(class_="food-name f18 orange fb fYaHei")]
            for element_two in element.find_all("p"):
                if str(element_two).find("工艺：")!=-1:
                    result["名字"] =[re.sub(re.compile("\r|\t|\n| |"),"",str(element_three.get_text())) for element_three in element_two.find_all("a")]
                if str(element_two).find("口味：")!=-1:
                    result["口味"] =[re.sub(re.compile("\r|\t|\n| |"),"",str(element_three.get_text())) for element_three in element_two.find_all("a")]
                if str(element_two).find("菜系：")!=-1:
                    result["菜系"] =[re.sub(re.compile("\r|\t|\n| |"),"",str(element_three.get_text())) for element_three in element_two.find_all("a")]
                if str(element_two).find("功效：")!=-1:
                    result["功效"] =[re.sub(re.compile("\r|\t|\n| |"),"",str(element_three.get_text())) for element_three in element_two.find_all("a")]
                if str(element_two).find("主料：")!=-1:
                    result["主料"] =[re.sub(re.compile("\r|\t|\n| |"),"",str(element_three.get_text())) for element_three in element_two.find_all("a")]
                if str(element_two).find("辅料：")!=-1:
                    result["辅料"] =[re.sub(re.compile("\r|\t|\n| |"),"",str(element_three.get_text())) for element_three in element_two.find_all("a")]
                if str(element_two).find("调料：")!=-1:
                    result["调料"] =re.sub(re.compile("\r|\t|\n| |"),"",str(element_two.get_text()))
        for element in soup.find_all(class_="text-intro f14 graydeep"):
            for element_two in element.find_ll("dl"):





    def projectCollection(self):
        """
        全部检查项目数据收集
        :return: 检查项目json文件
        """
        result = []
        count=0
        f = open(self.error_path, 'w', encoding='utf8')
        for i in range(1,3684):
            try:
                result.append(self.getProjects("http://jck.xywy.com/jc_"+str(i)+".html"))
                count =count+1
                print(count)
            except:
                print("http://jck.xywy.com/jc_"+str(i)+".html")
                f.write("http://jck.xywy.com/jc_"+str(i)+".html" + '\n')
        f.close()
        data = {}
        data["data"] = result
        with open(self.project_json_path, "w") as dump_f:
            json.dump(data, dump_f)


if __name__ == '__main__':
    print(SpiderXywyProjects().projectCollection())
