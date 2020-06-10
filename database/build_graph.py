# -*- coding: utf-8 -*-
"""
author:boblee
time:6.3.2020
"""
import xlrd
from py2neo import Graph, Node, Relationship
from config import Config
import json


class buildGraph():
    """"
    数据导入neo4j数据库
    """

    def __init__(self):
        self.neo4j_graph = Graph(Config.host, user=Config.user, password=Config.password)
        self.food_json_path = "../data/handle/food.json"
        self.food_relationship_path = "../data/handle/food_relationship.json"
        self.good_json_path = "../data/handle/good.json"
        self.good_relationship_path = "../data/handle/good_relationship.json"
        self.disease_json_path = "../data/handle/disease.json"
        self.disease_relationship_path = "../data/handle/disease_relationship.json"
        self.project_json_path = "../data/handle/project.json"
        self.project_relationship_path = "../data/handle/project_relationship.json"
        self.syptom_json_path = "../data/handle/symptom.json"
        self.syptom_relationship_path = "../data/handle/symptom_relationship.json"

    def getDict(self, dict_data):
        key_list = []
        value_list = []
        for key.value in dict_data.items():
            key_list.append(key)
            value_list.append(value)
        return key_list, value_list

    def createProjectNode(self):
        """
        创建节点
        :param label: 节点标签
        :param nodes: 节点
        :return: 
        """
        count = 0
        label = "project"
        with open(self.project_json_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["data"]:
                node = Node(label, name=data_dict['检查名字'], project_introduce=data_dict["基本介绍"],
                            project_normal=data_dict["正常值"],
                            project_meaning=data_dict['临床意义'], project_attention=data_dict['注意事项'],
                            project_process=data_dict['检查过程'],
                            project_specialized_classification=data_dict['专科分类'],
                            project_check_classification=data_dict['检查分类'],
                            project_sex=data_dict['适用性别'], project_stomach=data_dict['是否空腹'],
                            project_price=data_dict['参考价格'])
                self.neo4j_graph.create(node)
                count += 1
            print(label + "的全部数量是 %d " % (len(data_json["data"])))

    def createSyptomNode(self):
        """
        创建节点
        :param label: 节点标签
        :param nodes: 节点
        :return: 
        """
        count = 0
        label = "symptom"
        with open(self.syptom_json_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["data"]:
                node = Node(label, name=data_dict['名称'], symptom_introduce=data_dict["名称"],
                            symptom_cause=data_dict["病因"],
                            symptom_prevention=data_dict['预防'], symptom_check=data_dict['检查'],
                            symptom_identify=data_dict['诊断鉴别'])
                self.neo4j_graph.create(node)
                count += 1
            print(label + "的全部数量是 %d " % (len(data_json["data"])))
    def createDiseaseNode(self):
        """
        创建节点
        :param label: 节点标签
        :param nodes: 节点
        :return: 
        """
        count = 0
        label = "disease"
        with open(self.disease_json_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["data"]:
                node = Node(label, name=data_dict['名字'], disease_introuce=data_dict["疾病简介"],
                            disease_health_care=data_dict["医保疾病"],
                            disease_rate=data_dict['患病比例'], disease_susceptible_population=data_dict['易感人群'],
                            disease_transmission_way=data_dict['传染方式'],
                            disease_department=data_dict['就诊科室'], disease_treat_way=data_dict['治疗方式'],
                            disease_treat_rime=data_dict['治疗周期'], disease_recovery_rate=data_dict['治愈率'],
                            disease_treat_price=data_dict['治疗费用']
                            , disease_cause=data_dict['病因'], disease_prevention=data_dict['预防'],
                            disease_symptom=data_dict['症状']
                            , disease_check=data_dict['检查'], disease_idifity=data_dict['诊断鉴别'],
                            disease_treatment=data_dict['治疗'], disease_nuring=data_dict['护理'])
                self.neo4j_graph.create(node)
                count += 1
        print(label + "的全部数量是 %d " % (len(data_json["data"])))

    def createGoodNode(self):
        """
        创建节点
        :param label: 节点标签
        :param nodes: 节点
        :return: 
        """
        count = 0
        label = "goods"
        with open(self.good_json_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["data"]:
                node = Node(label, name=data_dict['名字'], goods_approve=data_dict["批准文号"],
                            goods_function=data_dict["功能主治"],
                            goods_production=data_dict['生产企业'], goods_use_name=data_dict['通用名称'],
                            goods_method=data_dict['用法用量'],
                            goods_dosage=data_dict['剂型'], goods_bad=data_dict['不良反应'],
                            goods_taboo=data_dict['禁忌'], goods_attention=data_dict['注意事项'],
                            goods_ingredients=data_dict['成份']
                            , goods_charactor=data_dict['性状'], goods_interact=data_dict['药物相互作用'],
                            goods_pharmacological_effects=data_dict['药理作用']
                            , goods_drug_overdose=data_dict['药物过量'], goods_storage=data_dict['贮藏'],
                            goods_standard=data_dict['执行标准'])
                self.neo4j_graph.create(node)
                count += 1
        print(label + "的全部数量是 %d " % (len(data_json["data"])))

    def createFoodNode(self):
        """
        创建节点
        :param label: 节点标签
        :param nodes: 节点
        :return: 
        """
        count = 0
        label = "foods"
        with open(self.food_json_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["data"]:
                node = Node(label, name=data_dict['名字'], foods_alias=data_dict["原料别名"],
                            foods_classification=data_dict["原料分类"],
                            foods_prompt=data_dict['食用提示'], foods_taboo_crowd=data_dict['禁忌人群'],
                            foods_adapt_crowd=data_dict['适应人群'],
                            foods_introduce=data_dict['原料介绍'], foods_nutritional_analysis=data_dict['营养分析'],
                            foods_guidance=data_dict['食用指导'], foods_culture=data_dict['食材文化'],
                            foods_dietotherapy_role=data_dict['食疗作用'])
                self.neo4j_graph.create(node)
                count += 1
        print(label + "的全部数量是 %d " % (len(data_json["data"])))

    def createRelationShip(self, start_node, end_node, edges, rel_type, rel_name):
        """
        创建实体关系边
        :param start_node:
        :param end_node:
        :param edges:
        :param rel_type:
        :param rel_name:
        :return:
        """
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.neo4j_graph.run(query)
                count += 1
                # print(rel_type, count, all)
            except Exception as e:
                print(e)
        print(rel_type + "的全部数量是 %d " % (count))
        return

    def createFoodRelationShip(self):
        food_bad = []
        food_good = []
        with open(self.food_relationship_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["bad"]:
                food_bad.append([data_dict["B"], data_dict["A"]])
            for data_dict_good in data_json["good"]:
                food_good.append([data_dict_good["B"], data_dict_good["A"]])
        self.createRelationShip("foods", "foods", food_bad, "相克食物", "foodPhaseGrams")
        self.createRelationShip("foods", "foods", food_good, "相宜食物", "foodFitting")

    def createDiseaseRelationShip(self):
        all_good = []
        all_bad = []
        all_and_disease = []
        all_drug = []
        all_syptom = []
        all_project = []
        with open(self.disease_relationship_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["bad"]:
                if data_dict:
                   all_bad.append([data_dict["B"], data_dict["A"]])
            for data_dict_good in data_json["good"]:
                if data_dict_good:
                   all_good.append([data_dict_good["B"], data_dict_good["A"]])
            for data_disease in data_json["and_disease"]:
                if data_disease:
                    all_and_disease.append([data_disease["B"], data_disease["A"]])
            for data_drug in data_json["drug"]:
                if data_drug:
                    all_drug.append([data_drug["B"], data_drug["A"]])
            for data_syptom in data_json["syptom"]:
                if data_syptom:
                   all_syptom.append([data_syptom["B"], data_syptom["A"]])
            for data_project in data_json["project"]:
                if data_project:
                   all_project.append([data_project["B"], data_project["A"]])
        self.createRelationShip("disease", "foods", all_bad, "疾病忌吃", "diseaseBadFood")
        self.createRelationShip("disease", "foods", all_good, "疾病宜吃", "diseaseGoodFood")
        self.createRelationShip("disease", "disease", all_and_disease, "疾病并发疾病", "diseaseRelated")
        self.createRelationShip("disease", "goods", all_drug, "疾病推荐药品", "diseaseGoods")
        self.createRelationShip("disease", "symptom", all_syptom, "疾病症状", "diseaseSymptm")
        self.createRelationShip("disease", "project", all_project, "疾病相关检查", "diseaseProject")
    def createSyptomRelationShip(self):
        all_good = []
        all_bad = []
        all_project = []
        with open(self.syptom_relationship_path, encoding='utf8') as dump_f:
            data_json = json.load(dump_f)
            for data_dict in data_json["bad"]:
                if data_dict:
                   all_bad.append([data_dict["B"], data_dict["A"]])
            for data_dict_good in data_json["good"]:
                if data_dict_good:
                   all_good.append([data_dict_good["B"], data_dict_good["A"]])
            for data_project in data_json["project"]:
                if data_project:
                   all_project.append([data_project["B"], data_project["A"]])
        self.createRelationShip("symptom", "foods", all_bad, "症状忌吃", "symptomBadFood")
        self.createRelationShip("symptom", "foods", all_good, "症状宜吃", "symptomGoodFood")
        self.createRelationShip("symptom", "project", all_project, "症状相关检查", "symptomProject")




if __name__ == '__main__':
    build_graph =buildGraph()
    build_graph.createDiseaseNode()
    build_graph.createSyptomNode()
    build_graph.createFoodNode()
    build_graph.createGoodNode()
    build_graph.createProjectNode()
    build_graph.createDiseaseRelationShip()
    build_graph.createSyptomRelationShip()
    build_graph.createFoodRelationShip()