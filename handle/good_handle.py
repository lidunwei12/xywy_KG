# -*- coding: utf-8 -*-
"""
time:6.3.2020
Author:bob.lee

"""
import json


class goodHandle():
    """
        药品数据数据梳理并提取三元组关系
        """

    def __init__(self):
        self.dict = ['名字', '批准文号', '功能主治', '生产企业', '通用名称', '用法用量', '剂型', '不良反应', '禁忌', '注意事项', '成份', '性状', '药物相互作用',
                     '药理作用', '药物过量', '贮藏', '执行标准']
        self.origin_data = "../data/json/good.json"
        self.good_handle_path = "../data/handle/good.json"
        self.good_relationship_path = "../data/handle/good_relationship.json"

    def handle(self):
        all_data = []
        all_good = []
        all_bad = []
        count = 0
        with open(self.origin_data, encoding='utf8') as disease_symptom_json:
            data_json = json.load(disease_symptom_json)
            for element in data_json["data"]:
                if "名字" in element:
                    if element["名字"] != '':
                        count = count + 1
                        print(count)
                        result = {}
                        for element_data in self.dict:
                            result[element_data] = ''
                        result["名字"] = element["名字"]
                        if "批准文号" in element:
                            result["批准文号"] = element["批准文号"]
                        if "功能主治" in element:
                            result["功能主治"] = element["功能主治"]
                        if "生产企业" in element:
                            result["生产企业"] = element["生产企业"]
                        if "通用名称" in element:
                            result["通用名称"] = element["通用名称"]
                        if "用法用量" in element:
                            result["用法用量"] = element["用法用量"]
                        if "剂型" in element:
                            result["剂型"] = element["剂型"]
                        if "不良反应" in element:
                            result["不良反应"] = element["不良反应"]
                        if "禁忌" in element:
                            result["禁忌"] = element["禁忌"]
                        if "注意事项" in element:
                            result["注意事项"] = element["注意事项"]
                        if "成份" in element:
                            result["成份"] = element["成份"]
                        if "性状" in element:
                            result["性状"] = element["性状"]
                        if "药物相互作用" in element:
                            result["药物相互作用"] = element["药物相互作用"]
                        if "药理作用" in element:
                            result["药理作用"] = element["药理作用"]
                        if "药物过量" in element:
                            result["药物过量"] = element["药物过量"]
                        if "贮藏" in element:
                            result["贮藏"] = element["贮藏"]
                        if "执行标准" in element:
                            result["执行标准"] = element["执行标准"]
                        if "相宜" in element:
                            if element["相宜"] != []:
                                good = {}
                                for good_temp in element["相宜"]:
                                    if good_temp != element["名字"]:
                                        good["A"] = good_temp
                                        good["B"] = element["名字"]
                                        good["relationship"] = "相宜"
                                all_good.append(good)
                        if "相克" in element:
                            if element["相克"] != []:
                                bad = {}
                                for bad_temp in element["相克"]:
                                    if bad_temp != element["名字"]:
                                        bad["A"] = bad_temp
                                        bad["B"] = element["名字"]
                                        bad["relationship"] = "相克"
                                all_bad.append(bad)
                        all_data.append(result)
        data_all = {}
        data_all['data'] = all_data
        with open(self.good_handle_path, "w") as dump_f:
            json.dump(data_all, dump_f)
        data_relationship = {}
        data_relationship['good'] = all_good
        data_relationship['bad'] = all_bad
        with open(self.good_relationship_path, "w") as dump_f:
            json.dump(data_relationship, dump_f)


if __name__ == '__main__':
    with open("../data/json/good.json", encoding='utf8') as disease_symptom_json:
        data_json = json.load(disease_symptom_json)
        for temp in data_json['data']:
            print(temp["名字"],temp["通用名称"])
            # print([key for key, value in temp.items()])
            # goodHandle().handle()
