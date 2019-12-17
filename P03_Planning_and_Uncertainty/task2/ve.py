# -*- coding: utf-8 -*-
# @Author: Jed Zhang 
# @Date: 2019-11-24 13:22:57

class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
        # Step 1: 用证据取代factor中相关变量的值
        for ev in evidenceList:
            for i, factor in enumerate(factorList):
                if ev in factor.varList:  # 因子中有变量在证据中
                    factorList[i] = factor.restrict(ev, evidenceList[ev])
            
        # Step 2: 按顺序依次消除变量
        for var in orderedListOfHiddenVariables:  # var就是课件里的Zj
            corresponding_factors = [factor for factor in factorList if var in factor.varList]
            if corresponding_factors:
                new_factor = corresponding_factors[0]
                factorList.remove(new_factor)
                for factor in corresponding_factors[1:]:  # 从第二个开始累乘
                    new_factor = new_factor.multiply(factor)
                    factorList.remove(factor)
                new_factor = new_factor.sumout(var)  # 对变量求和从而消除该变量
            factorList.append(new_factor)

        # Step 3: 归一化并显示结果
        print("RESULT:")
        res = factorList[0]
        for factor in factorList[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())  # 归一化分母
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        res.printInf()

    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.printInf()


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}  # 由setCpt函数输入

    def setCpt(self, cpt):
        self.cpt = cpt

    def printInf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print("")

    def multiply(self, factor):
        """function that multiplies with another factor"""
        # 使用了类似关系型数据库中“自然连接”的操作
        var_intersection = sorted(list(set(self.varList) & set(factor.varList)))  # 两个factor的变量交集
        new_var_list = self.varList + [var for var in factor.varList if var not in var_intersection]
        tup_index1 = [self.varList.index(x) for x in var_intersection]
        tup_index2 = [factor.varList.index(x) for x in var_intersection]
        
        merge_tup = list(zip(tup_index1, tup_index2))
        new_cpt = {}
        for key1 in self.cpt:
            for key2 in factor.cpt:
                flag = True
                for m in merge_tup:
                    if key1[m[0]] != key2[m[1]]:  # 不符合自然连接条件，跳过当前key对
                        flag = False
                        break
                if flag:
                    # key1+temp组成新的key
                    temp = key2
                    for m in merge_tup:
                        temp = list(key2)
                        temp[m[1]] = 'x'  # 用x标记该字符将要删除
                        temp = ''.join(temp).replace('x', '')
                    new_cpt[key1+temp] = self.cpt[key1] * factor.cpt[key2]

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

    def sumout(self, variable):
        """function that sums out a variable given a factor"""
        pos = self.varList.index(variable)  # 要求和的变量的序号
        var_dom =  set([key[pos] for key in self.cpt])  # 要求和的变量的取值范围Dom
        new_var_list = self.varList[:pos] + self.varList[pos+1:]

        new_cpt_keyset = sorted(list(set([k[:pos]+k[pos+1:] for k in self.cpt.keys()])))  # 新变量列表的组合构成的集合
        new_cpt = {}
        for new_key in new_cpt_keyset:
            new_value = 0
            for value in var_dom:
                new_value += self.cpt[new_key[:pos] + value + new_key[pos:]]  # 在原来的CPT中进行累加
            new_cpt[new_key] = new_value

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node
        
    def restrict(self, variable, value):
        """function that restricts a variable to some value in a given factor"""
        pos = self.varList.index(variable)  # 要限制的变量的序号
        new_var_list = self.varList[:pos] + self.varList[pos+1:]

        new_cpt_keyset = sorted(list(set([k[:pos]+k[pos+1:] for k in self.cpt.keys()])))  # 新变量列表的组合构成的集合
        new_cpt = {}
        for new_key in new_cpt_keyset:
            new_cpt[new_key] = self.cpt[new_key[:pos] + value + new_key[pos:]]

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

if __name__ == '__main__':
    """
    # 节点和取值的编码方法
    # PA: PatientAge:     ['0 −30'(0) ,'31−65'(1) ,'65+'(2)]
    # CT: CTScanResult:   ['Ischemic Stroke'(0) ,'Hemmorraghic Stroke'(1) ]
    # MR: MRIScanResult:  ['Ischemic Stroke'(0) ,'Hemmorraghic Stroke'(1) ]
    # AN: Anticoagulants: ['Used'(1) ,'Not used'(0) ]
    # ST: StrokeType:     ['Ischemic Stroke'(0) ,'Hemmorraghic Stroke'(1) ,'Stroke Mimic'(2) ]
    # MO: Mortality:      ['True'(1) ,'False'(0) ]
    # DI: Disability:     ['Negligible'(0) ,'Moderate'(1) ,'Severe'(2) ]
    """
    
    PA = Node('PA', ['PA'])              # PatientAge
    CT = Node('CT', ['CT'])              # CTScanResult
    MR = Node('MR', ['MR'])              # MRIScanResult
    AN = Node('AN', ['AN'])              # Anticoagulants
    ST = Node('ST', ['ST', 'CT', 'MR'])  # StrokeType
    MO = Node('MO', ['MO', 'ST', 'AN'])  # Mortality
    DI = Node('DI', ['DI', 'ST', 'PA'])    # Disability

    # Generate cpt for each node
    PA.setCpt({'0': 0.1, '1': 0.3, '2': 0.6})
    CT.setCpt({'0': 0.7, '1': 0.3})
    MR.setCpt({'0': 0.7, '1': 0.3})
    AN.setCpt({'0': 0.5, '1': 0.5})
    ST.setCpt({
        '000': 0.8, '001': 0.5, '010': 0.5, '011': 0.0,
        '100': 0.0, '101': 0.4, '110': 0.4, '111': 0.9,
        '200': 0.2, '201': 0.1, '210': 0.1, '211': 0.1
    })
    MO.setCpt({
        '001': 0.28, '011': 0.99, '021': 0.1, '000': 0.56, '010': 0.58, '020': 0.05,
        '101': 0.72, '111': 0.01, '121': 0.9, '100': 0.44, '110': 0.42, '120': 0.95
    })
    DI.setCpt({
        '000': 0.80, '010': 0.70, '020': 0.90,
        '001': 0.60, '011': 0.50, '021': 0.40,
        '002': 0.30, '012': 0.20, '022': 0.10,

        '100': 0.10, '110': 0.20, '120': 0.05,
        '101': 0.30, '111': 0.40, '121': 0.30,
        '102': 0.40, '112': 0.20, '122': 0.10,

        '200': 0.10, '210': 0.10, '220': 0.05,
        '201': 0.10, '211': 0.10, '221': 0.30,
        '202': 0.30, '212': 0.60, '222': 0.80
    })

    # 注意：下面evidenceList中将变量的取值统一成字符串的'1'的'0'，而不是数字。这是为了与CPT的键保持一致。
    factorList = [PA, CT, MR, AN, ST, MO, DI]  # 注意传参时要传入拷贝，否则原列表会被inference函数修改
    print("p1", end=' ')
    VariableElimination.inference(factorList[:], ['MO, CT'], ['MR', 'AN', 'DI', 'ST'], {'PA': '1'})

    print("p2", end=' ')
    VariableElimination.inference(factorList[:], ['DI, CT'], ['AN', 'MO', 'ST'], {'PA': '2', 'MR': '1'})

    print("p3", end=' ')
    VariableElimination.inference(factorList[:], ['ST'], ['AN', 'DI', 'MO'], {'PA': '2', 'CT': '1', 'MR': '0'})

    print("p4", end=' ')
    VariableElimination.inference(factorList[:], ['AN'], ['MR', 'CT', 'DI', 'MO', 'ST'], {'PA': '1'})

    print("p5", end=' ')
    VariableElimination.inference(factorList[:], ['DI'], ['PA', 'CT', 'MR', 'AN', 'MO', 'ST'], {})
