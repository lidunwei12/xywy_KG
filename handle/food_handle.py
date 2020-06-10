# -*- coding: utf-8 -*-
"""
time:6.3.2020
Author:bob.lee

"""
import json


class foodHandle():
    """
        食物数据数据梳理并提取三元组关系
        """

    def __init__(self):
        self.dict = ['名字', '原料别名', '原料分类', '食用提示', '禁忌人群', '适应人群', '原料介绍', '食用指导', '食疗作用', '食材文化', "营养分析"]
        self.origin_data = "../data/json/food.json"
        self.food_handle_path = "../data/handle/food.json"
        self.food_relationship_path = "../data/handle/food_relationship.json"

    def handle(self):
        all_data = []
        all_good = []
        all_bad = []
        with open(self.origin_data, encoding='utf8') as disease_symptom_json:
            data_json = json.load(disease_symptom_json)
            for element in data_json["data"]:
                result = {}
                for element_data in self.dict:
                    result[element_data] = ''
                if "名字" in element:
                    result["名字"] = element["名字"]
                if "原料别名" in element:
                    result["原料别名"] = element["原料别名"]
                if "原料分类" in element:
                    result["原料分类"] = element["原料分类"]
                if "食用提示" in element:
                    result["食用提示"] = element["食用提示"]
                if "禁忌人群" in element:
                    result["禁忌人群"] = element["禁忌人群"]
                if "适应人群" in element:
                    result["适应人群"] = element["适应人群"]
                if "原料介绍" in element:
                    result["原料介绍"] = element["原料介绍"]
                if "营养分析" in element:
                    result["营养分析"] = element["营养分析"]
                if "食用指导" in element:
                    result["食用指导"] = element["食用指导"]
                if "食疗作用" in element:
                    result["食疗作用"] = element["食疗作用"]
                if "食材文化" in element:
                    result["食材文化"] = element["食材文化"]
                if "相宜" in element:
                    if element["相宜"] != []:
                        for good_temp in element["相宜"]:
                            good = {}
                            if good_temp != element["名字"]:
                                good["A"] = good_temp
                                good["B"] = element["名字"]
                                good["relationship"] = "相宜"
                            print(good)
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
        with open(self.food_handle_path, "w") as dump_f:
            json.dump(data_all, dump_f)
        data_relationship = {}
        data_relationship['good'] = all_good
        data_relationship['bad'] = all_bad
        with open(self.food_relationship_path, "w") as dump_f:
            json.dump(data_relationship, dump_f)


if __name__ == '__main__':
    # with open("../data/json/food.json", encoding='utf8') as disease_symptom_json:
    #     data_json = json.load(disease_symptom_json)
    #     for temp in data_json['data']:
    #          # print(temp)
    #          print([key for key,value in temp.items()])
    foodHandle().handle()
