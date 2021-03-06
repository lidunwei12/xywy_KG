# -*- coding: utf-8 -*-
"""
time:6.3.2020
Author:bob.lee

"""
import json


class diseaseHandle():
    """
    疾病数据数据梳理并提取三元组关系
    """

    def __init__(self):
        self.dict = ['疾病简介', '医保疾病', '患病比例', '易感人群', '传染方式', '就诊科室', '治疗方式', '治疗周期', '治愈率', '治疗费用', '病因', '预防', '症状',
                     '检查', '诊断鉴别', '治疗', '护理', '名字']
        self.origin_data = "../data/disease.json"
        self.disease_handle_path = "../data/handle/disease.json"
        self.disease_relationship_path = "../data/handle/disease_relationship.json"

    def handle(self):
        all_data = []
        all_good = []
        all_bad = []
        all_and_disease = []
        all_drug = []
        all_syptom = []
        all_project = []
        with open(self.origin_data, encoding='utf8') as disease_symptom_json:
            data_json = json.load(disease_symptom_json)
            for element in data_json["data"]:
                result = {}
                for element_data in self.dict:
                    result[element_data] = ''
                if "名字" in element:
                    result["名字"] = element["名字"]
                if "疾病简介" in element:
                    result["疾病简介"] = element["疾病简介"]
                if "医保疾病" in element:
                    result["医保疾病"] = element["医保疾病"]
                if "患病比例" in element:
                    result["患病比例"] = element["患病比例"]
                if "易感人群" in element:
                    result["易感人群"] = element["易感人群"]
                if "传染方式" in element:
                    result["传染方式"] = element["传染方式"]
                if "就诊科室" in element:
                    result["就诊科室"] = element["就诊科室"]
                if "治疗方式" in element:
                    result["治疗方式"] = element["治疗方式"]
                if "治疗周期" in element:
                    result["治疗周期"] = element["治疗周期"]
                if "治愈率" in element:
                    result["治愈率"] = element["治愈率"]
                if "治疗费用" in element:
                    result["治疗费用"] = element["治疗费用"]
                if "病因" in element:
                    result["病因"] = element["病因"]
                if "预防" in element:
                    result["预防"] = element["预防"]
                if "症状" in element:
                    result["症状"] = element["症状"]
                if "检查" in element:
                    result["检查"] = element["检查"]
                if "诊断鉴别" in element:
                    result["诊断鉴别"] = element["诊断鉴别"]
                if "治疗" in element:
                    result["治疗"] = element["治疗"]
                if "护理" in element:
                    result["护理"] = element["护理"]
                if "宜吃食物" in element:
                    if element["宜吃食物"] != []:
                        for good_temp in element["宜吃食物"]:
                            good = {}
                            if good_temp != element["名字"]:
                                good["A"] = good_temp
                                good["B"] = element["名字"]
                                good["relationship"] = "宜吃食物"
                            if good:
                                all_good.append(good)
                if "并发症" in element:
                    if element["并发症"] != []:
                        for and_disease_temp in element["并发症"]:
                            and_disease = {}
                            if and_disease_temp != element["名字"]:
                                and_disease["A"] = and_disease_temp
                                and_disease["B"] = element["名字"]
                                and_disease["relationship"] = "并发症"
                            if and_disease:
                                all_and_disease.append(and_disease)
                if "常用药品" in element:
                    if element["常用药品"] != []:
                        for drug_temp in element["常用药品"]:
                            drug = {}
                            if drug_temp != element["名字"]:
                                drug["A"] = drug_temp
                                drug["B"] = element["名字"]
                                drug["relationship"] = "常用药品"
                            if drug:
                                all_drug.append(drug)
                if "相关症状" in element:
                    if element["相关症状"] != []:
                        for syptom_temp in element["相关症状"]:
                            syptom = {}
                            if syptom_temp != element["名字"]:
                                syptom["A"] = syptom_temp
                                syptom["B"] = element["名字"]
                                syptom["relationship"] = "相关症状"
                            if syptom:
                                all_syptom.append(syptom)
                if "相关检查" in element:
                    if element["相关检查"] != []:
                        for project_temp in element["相关检查"]:
                            project = {}
                            if project_temp != element["名字"]:
                                project["A"] = project_temp
                                project["B"] = element["名字"]
                                project["relationship"] = "相关检查"
                            if project:
                                all_project.append(project)
                if "忌吃食物" in element:
                    if element["忌吃食物"] != []:
                        for bad_temp in element["忌吃食物"]:
                            bad = {}
                            if bad_temp != element["名字"]:
                                bad["A"] = bad_temp
                                bad["B"] = element["名字"]
                                bad["relationship"] = "忌吃食物"
                            if bad:
                                all_bad.append(bad)
                all_data.append(result)
        data_all = {}
        data_all['data'] = all_data
        with open(self.disease_handle_path, "w") as dump_f:
            json.dump(data_all, dump_f)
        data_relationship = {}
        data_relationship['good'] = all_good
        data_relationship['bad'] = all_bad
        data_relationship['drug'] = all_drug
        data_relationship['and_disease'] = all_and_disease
        data_relationship['syptom'] = all_syptom
        data_relationship['project'] = all_project
        with open(self.disease_relationship_path, "w") as dump_f:
            json.dump(data_relationship, dump_f)


if __name__ == '__main__':
    with open("../data/disease.json", encoding='utf8') as disease_symptom_json:
        data_json = json.load(disease_symptom_json)
        for temp in data_json['data']:
             # print(temp)
             print([key for key,value in temp.items()])
    # diseaseHandle().handle()
