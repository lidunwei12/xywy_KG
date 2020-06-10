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
        for element in soup.find_all(class_="baby-target ops-content"):
            for element_one in element.find_all(class_="target-bt f20 deepgray pl20 mt25 step"):
                temp = element_one.get_text()
                if temp.find("基本信息") != -1:
                    status.append(0)
                if temp.find("正常值") != -1:
                    status.append(1)
                if temp.find("临床意义") != -1:
                    status.append(2)
                if temp.find("注意事项") != -1:
                    status.append(3)
                if temp.find("检查过程") != -1:
                    status.append(4)
                if temp.find("不适宜人群") != -1:
                    status.append(5)
                if temp.find("不良反应与风险") != -1:
                    status.append(6)
            for element_two in element.find_all(class_="target-txt pl20 pr20"):
                text_temp.append(re.sub(re.compile('\r|\n|\t|​'), '', str(element_two.get_text()).replace(' ', "")))
        for i in range(len(text_temp)):
            if status[i] == 1:
                result["正常值"] = text_temp[i]
            if status[i] == 2:
                result["临床意义"] = text_temp[i]
            if status[i] == 3:
                result["注意事项"] = text_temp[i]
            if status[i] == 4:
                result["检查过程"] = text_temp[i]
            if status[i] == 5:
                result["不适宜人群"] = text_temp[i]
            if status[i] == 6:
                result["不良反应与风险"] = text_temp[i]
        result["基本介绍"] = re.sub(re.compile('\r|\n|\t| '), '',
                                ''.join([str(element.get_text()) for element in
                                         soup.find_all(
                                             class_="baby-weeks-infor mt20 t2 lh28 f13 graydeep")]))
        result["检查名字"] = re.sub(re.compile('\r|\n|\t| '), '', ''.join(
            [str(element_one.get_text()) for element in soup.find_all(class_="baby-weeks") for element_one in
             element.find_all(class_="clearfix")]))
        count = 0
        for element in soup.find_all(class_="target-txt pl20 pr20"):
            count = count + 1
            if count > 1:
                break
            for element_one in element.find_all("p"):
                temp_text = re.sub(re.compile('\r|\n|\t| |​'), '', str(element_one.get_text())) + "&"
                if temp_text.find("专科分类") != -1:
                    result["专科分类"] = ''.join(re.findall(r'专科分类：(.+?)检查分类：', temp_text))
                if temp_text.find("检查分类") != -1:
                    result["检查分类"] = ''.join(re.findall(r'检查分类：(.+?)&', temp_text))
                if temp_text.find("适用性别") != -1:
                    result["适用性别"] = ''.join(re.findall(r'适用性别：(.+?)是否空腹：', temp_text))
                if temp_text.find("是否空腹") != -1:
                    result["是否空腹"] = ''.join(re.findall(r'是否空腹：(.+?)&', temp_text))
                if temp_text.find("参考价格") != -1:
                    result["参考价格"] = ''.join(re.findall(r'参考价格：(.+?)&', temp_text))
        relaction_syptom =[]
        relaction_disease = []
        for element in soup.find_all(class_="easy-send mt10"):
            if str(element).find("相关疾病")!=-1:
                for element_one in element.find_all("a"):
                    relaction_disease.append(re.sub(re.compile('\r|\n|\t| |​'), '', str(element_one.get_text())))
            if str(element).find("相关症状")!=-1:
                for element_one in element.find_all("a"):
                    relaction_syptom.append(re.sub(re.compile('\r|\n|\t| |​'), '', str(element_one.get_text())))
        result["相关症状"] =relaction_syptom
        result["相关疾病"] =relaction_disease
        result["url"] = url
        return result

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
