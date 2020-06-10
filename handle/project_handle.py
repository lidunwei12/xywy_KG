# -*- coding: utf-8 -*-
"""
time:6.3.2020
Author:bob.lee

"""
import json

class projectHandle():
    """
        检查项目数据数据梳理并提取三元组关系
        """
    def __init__(self):
        self.dict = ['正常值', '临床意义', '注意事项', '检查过程', '基本介绍', '检查名字', '专科分类', '检查分类', '适用性别', '是否空腹', '参考价格']
        self.origin_data = "../data/json/project_json.json"
        self.project_handle_path = "../data/handle/project.json"
        self.project_relationship_path = "../data/handle/project_relationship.json"

    def handle(self):
        all_data = []
        all_good = []
        all_bad = []
        count =0
        with open(self.origin_data, encoding='utf8') as disease_symptom_json:
            data_json = json.load(disease_symptom_json)
            for element in data_json["data"]:
                if "检查名字" in element:
                    if element["检查名字"] !='':
                        count =count+1
                        print(count)
                        result = {}
                        for element_data in self.dict:
                            result[element_data] = ''
                        result["检查名字"] = element["检查名字"]
                        if "正常值" in element:
                            result["正常值"] = element["正常值"]
                        if "临床意义" in element:
                            result["临床意义"] = element["临床意义"]
                        if "注意事项" in element:
                            result["注意事项"] = element["注意事项"]
                        if "检查过程" in element:
                            result["检查过程"] = element["检查过程"]
                        if "基本介绍" in element:
                            result["基本介绍"] = element["基本介绍"]
                        if "专科分类" in element:
                            result["专科分类"] = element["专科分类"]
                        if "检查分类" in element:
                            result["检查分类"] = element["检查分类"]
                        if "适用性别" in element:
                            result["适用性别"] = element["适用性别"]
                        if "是否空腹" in element:
                            result["是否空腹"] = element["是否空腹"]
                        if "参考价格" in element:
                            result["参考价格"] = element["参考价格"]
                        if "相宜" in element:
                            if element["相宜"] != []:
                                for good_temp in element["相宜"]:
                                    good = {}
                                    if good_temp != element["名字"]:
                                        good["A"] = good_temp
                                        good["B"] = element["名字"]
                                        good["relationship"] = "相宜"
                                    all_good.append(good)
                        if "相克" in element:
                            if element["相克"] != []:
                                for bad_temp in element["相克"]:
                                    bad = {}
                                    if bad_temp != element["名字"]:
                                        bad["A"] = bad_temp
                                        bad["B"] = element["名字"]
                                        bad["relationship"] = "相克"
                                    all_bad.append(bad)
                        all_data.append(result)
        data_all = {}
        data_all['data'] = all_data
        with open(self.project_handle_path, "w") as dump_f:
            json.dump(data_all, dump_f)
        data_relationship = {}
        data_relationship['good'] = all_good
        data_relationship['bad'] = all_bad
        with open(self.project_relationship_path, "w") as dump_f:
            json.dump(data_relationship, dump_f)


if __name__ == '__main__':
    with open("../data/json/project_json.json", encoding='utf8') as disease_symptom_json:
        data_json = json.load(disease_symptom_json)
        for temp in data_json['data']:
             # print(temp)
             print([key for key,value in temp.items()])
    # projectHandle().handle()


