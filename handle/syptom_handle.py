# -*- coding: utf-8 -*-
"""
time:6.3.2020
Author:bob.lee

"""
import json


class symptomHandle():
    """
        症状数据数据梳理并提取三元组关系
        """

    def __init__(self):
        self.dict = ['名称', '介绍', '病因', '预防', '检查', '诊断鉴别']
        self.origin_data = "../data/json/symptom.json"
        self.symptom_handle_path = "../data/handle/symptom.json"
        self.symptom_relationship_path = "../data/handle/symptom_relationship.json"

    def handle(self):
        all_data = []
        all_good = []
        all_bad = []
        all_project = []
        count = 0
        with open(self.origin_data, encoding='utf8') as disease_symptom_json:
            data_json = json.load(disease_symptom_json)
            for element in data_json["data"]:
                if "名称" in element:
                    if element["名称"] != '':
                        count = count + 1
                        print(count)
                        result = {}
                        for element_data in self.dict:
                            result[element_data] = ''
                        if "名称" in element:
                            result["名称"] = element["名称"]
                        if "介绍" in element:
                            result["介绍"] = element["介绍"]
                        if "病因" in element:
                            result["病因"] = element["病因"]
                        if "预防" in element:
                            result["预防"] = element["预防"]
                        if "检查" in element:
                            result["检查"] = element["检查"]
                        if "诊断鉴别" in element:
                            result["诊断鉴别"] = element["诊断鉴别"]
                        if "忌吃食物" in element:
                            if element["忌吃食物"] != []:
                                for bad_temp in element["忌吃食物"]:
                                    bad = {}
                                    if bad_temp != element["名称"]:
                                        bad["A"] = bad_temp
                                        bad["B"] = element["名称"]
                                        bad["relationship"] = "忌吃食物"
                                    if bad:
                                        all_bad.append(bad)
                        if "宜吃食物" in element:
                            if element["宜吃食物"] != []:
                                for good_temp in element["宜吃食物"]:
                                    good = {}
                                    if good_temp != element["名称"]:
                                        good["A"] = good_temp
                                        good["B"] = element["名称"]
                                        good["relationship"] = "宜吃食物"
                                    if good:
                                        all_good.append(good)
                        if "相关检查" in element:
                            if element["相关检查"] != []:
                                for project_temp in element["相关检查"]:
                                    project = {}
                                    if project_temp != element["名称"]:
                                        project["A"] = project_temp
                                        project["B"] = element["名称"]
                                        project["relationship"] = "相关检查"
                                    if project:
                                        all_project.append(project)
                        all_data.append(result)
        data_all = {}
        data_all['data'] = all_data
        with open(self.symptom_handle_path, "w") as dump_f:
            json.dump(data_all, dump_f)
        data_relationship = {}
        data_relationship['good'] = all_good
        data_relationship['project'] = all_project
        data_relationship['bad'] = all_bad
        with open(self.symptom_relationship_path, "w") as dump_f:
            json.dump(data_relationship, dump_f)


if __name__ == '__main__':
    # with open("../data/json/symptom.json", encoding='utf8') as disease_symptom_json:
    #     data_json = json.load(disease_symptom_json)
    #     for temp in data_json['data']:
    #          # print(temp)
    #          print([key for key,value in temp.items()])
    symptomHandle().handle()
