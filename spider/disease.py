# -*- coding: utf-8 -*-
"""
time:6.3.2020
Author:bob.lee

"""
import re
import json
import requests
from bs4 import BeautifulSoup


class SpiderXywyDisease():
    """
    基于寻医问药网疾病数据收集
    """

    def __init__(self):
        self.disease_json_path = "../data/json/disease.json"
        self.error_path = "../data/error.txt"
        self.base_url = "http://jib.xywy.com/il_sii/gaishu/"
        self.cause_url = "http://jib.xywy.com/il_sii/cause/"
        self.prevent_url = "http://jib.xywy.com/il_sii/prevent/"
        self.symptom_url = "http://jib.xywy.com/il_sii/symptom/"
        self.check_url = "http://jib.xywy.com/il_sii/inspect/"
        self.identify_url = "http://jib.xywy.com/il_sii/diagnosis/"
        self.treat_url = "http://jib.xywy.com/il_sii/treat/"
        self.nurse_url = "http://jib.xywy.com/il_sii/nursing/"
        self.food_url = "http://jib.xywy.com/il_sii/food/"
        self.main_url = "http://jib.xywy.com/html/"
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

    def getDiseaseBase(self, url):
        """
        收集疾病的基础信息
        :param url: 疾病url
        :return: 疾病基础信息数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        for element in soup.find_all(class_="jib-articl fr f14"):
            for element_one in element.find_all(class_="jib-articl-con jib-lh-articl"):
                result["疾病简介"] = re.sub(re.compile('\r|\n|\t|'), '', str(element_one.get_text()))
            for element_two in element.find_all(class_="mt20 articl-know"):
                for element_three in element_two.find_all(class_="clearfix"):
                    temp = re.sub(re.compile('\r|\t|'), '', str(element_three.get_text()))
                    if temp[0:10].find("医保疾病") != -1:
                        result["医保疾病"] = re.sub(re.compile('\n| |医保疾病：| |'), '', temp)
                    if temp[0:10].find("患病比例") != -1:
                        result["患病比例"] = re.sub(re.compile('\n| |患病比例：| |'), '', temp)
                    if temp[0:10].find("易感人群") != -1:
                        result["易感人群"] = re.sub(re.compile('\n| |易感人群：| |'), '', temp)
                    if temp[0:10].find("传染方式") != -1:
                        result["传染方式"] = re.sub(re.compile('\n| |传染方式：| |'), '', temp)
                    if temp[0:10].find("并发症") != -1:
                        result["并发症"] = [i for i in re.sub(re.compile('并发症：| |'), '', temp).split('\n') if i != '']
                    if temp[0:10].find("就诊科室") != -1:
                        result["就诊科室"] = re.sub(re.compile('\n| |就诊科室：| |'), '', temp)
                    if temp[0:10].find("治疗方式") != -1:
                        result["治疗方式"] = re.sub(re.compile('\n| |治疗方式：| |'), '', temp)
                    if temp[0:10].find("治疗周期") != -1:
                        result["治疗周期"] = re.sub(re.compile('\n| |治疗周期：| |'), '', temp)
                    if temp[0:10].find("治愈率") != -1:
                        result["治愈率"] = re.sub(re.compile('\n| |治愈率：| |'), '', temp)
                    if temp[0:10].find("常用药品") != -1:
                        result["常用药品"] = [i for i in re.sub(re.compile('常用药品：| |'), '', temp).split('\n') if i != '']
                    if temp[0:10].find("治疗费用") != -1:
                        result["治疗费用"] = re.sub(re.compile('\n| |治疗费用：| |'), '', temp)
        result['名字'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all(class_="jb-name fYaHei gre")]))
        return result

    def getDiseaseCause(self, url):
        """
        收集疾病病因数据
        :param url: 病因yrl
        :return: 疾病病因数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['病因'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getDiseasePrevention(self, url):
        """
        收集疾病预防数据
        :param url: 预防url
        :return: 疾病预防数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['预防'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getDiseaseSyptom(self, url):
        """
        收集疾病症状数据
        :param url: 症状url
        :return: 症状数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['症状'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        result['相关症状'] = [str(element_one.get_text()) for element in soup.find_all(class_="db f12 lh240 mb15") for
                          element_one in element.find_all("a")]
        return result

    def getDiseaseCheck(self, url):
        """
        疾病检查数据收集
        :param url: 检查url
        :return: 疾病检查数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['检查'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        check_temp = []
        for element in soup.find_all(class_="more-zk pr"):
            for element_one in element.find_all(class_="clearfix jib-check"):
                for element_two in element_one.find_all(class_="gre"):
                    temp = element_two.get_text()
                    if temp != "详情":
                        check_temp.append(temp)
        result['相关检查'] = check_temp
        return result

    def getDiseaseIdentify(self, url):
        """
        疾病诊断数据收集
        :param url: 诊断url
        :return: 疾病诊断数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['诊断鉴别'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getDiseaseTreatment(self, url):
        """
        疾病治疗数据收集
        :param url: 疾病治疗url
        :return: 治疗数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        result['治疗'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getDiseaseNursing(self, url):
        """
        疾病护理数据收集
        :param url: 护理url
        :return: 
        """
        soup = self.requestRespnse(url)
        result = {}
        result['护理'] = re.sub(re.compile('\r|\n|\t| |'), '', ''.join(
            [str(element.get_text()) for element in soup.find_all("p")]))
        return result

    def getDiseaseFood(self, url):
        """
        疾病食物数据收集
        :param url: 食物数据url
        :return: 食物数据包
        """
        soup = self.requestRespnse(url)
        result = {}
        for element in soup.find_all(class_="diet-item none"):
            temp = str(element.get_text())
            if temp.find('忌') != -1:
                result["忌吃食物"] = [i for i in ''.join([str(element_one.get_text()) for element_one in
                                                      element.find_all(class_="diet-img clearfix mt20")]).split('\n') if
                                  i != '']
            if temp.find('宜') != -1:
                result["推荐食谱"] = [i for i in ''.join([str(element_one.get_text()) for element_one in
                                                      element.find_all(class_="diet-img clearfix mt20")]).split('\n') if
                                  i != '']
        for element in soup.find_all(class_="diet-item none clearfix"):
            temp = str(element.get_text())
            result["宜吃食物"] = [i for i in ''.join([str(element_one.get_text()) for element_one in
                                                  element.find_all(class_="diet-img clearfix mt20")]).split('\n') if
                              i != '']

        return result

    def getDisease(self, name):
        """
        获取单个疾病的全部属性
        :param name: 疾病number
        :return: 全部属性数据包
        """
        base_url = self.base_url + name + '.htm'
        cause_url = self.cause_url + name + '.htm'
        prevent_url = self.prevent_url + name + '.htm'
        symptom_url = self.symptom_url + name + '.htm'
        check_url = self.check_url + name + '.htm'
        identify_url = self.identify_url + name + '.htm'
        treat_url = self.treat_url + name + '.htm'
        nurse_url = self.nurse_url + name + '.htm'
        food_url = self.food_url + name + '.htm'
        result = self.getDiseaseBase(base_url)
        result.update(self.getDiseaseCause(cause_url))
        result.update(self.getDiseasePrevention(prevent_url))
        result.update(self.getDiseaseSyptom(symptom_url))
        result.update(self.getDiseaseCheck(check_url))
        result.update(self.getDiseaseIdentify(identify_url))
        result.update(self.getDiseaseTreatment(treat_url))
        result.update(self.getDiseaseNursing(nurse_url))
        result.update(self.getDiseaseFood(food_url))
        return result

    def diseaseCollection(self):
        """
        寻医问药网全部疾病全部属性收集
        :return: 保存数据json
        """
        result = []
        count = 0
        f = open(self.error_path, 'w', encoding='utf8')
        for i in range(1, 10140):
            try:
                result.append(self.getDisease(str(i)))
                count = count + 1
                print(count)
            except:
                print(str(i) + "失败")
                f.write(str(i) + '\n')
        f.close()
        data = {}
        data["data"] = result
        with open(self.disease_json_path, "w") as dump_f:
            json.dump(data, dump_f)


if __name__ == '__main__':
    print(SpiderXywyDisease().diseaseCollection())
