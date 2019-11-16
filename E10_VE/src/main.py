# -*- coding: utf-8 -*-
# @Author: Jed Zhang 
# @Date: 2019-11-16 10:49:40

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


# 并没有用到Util类
# class Util:
#     @staticmethod
#     def to_binary(num, len):
#         return format(num, '0' + str(len) + 'b')


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
        new_var_list = self.varList[:pos] + self.varList[pos+1:]

        new_cpt_keyset = sorted(list(set([k[:pos]+k[pos+1:] for k in self.cpt.keys()])))  # 新变量列表的组合构成的集合
        new_cpt = {}
        for new_key in new_cpt_keyset:
            new_value = 0
            for value in ['0', '1']:  # 本例中变量只有两种取值
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
    # create nodes for Bayes Net
    B = Node("B", ["B"])
    E = Node("E", ["E"])
    A = Node("A", ["A", "B","E"])
    J = Node("J", ["J", "A"])
    M = Node("M", ["M", "A"])

    # Generate cpt for each node
    B.setCpt({'0': 0.999, '1': 0.001})
    E.setCpt({'0': 0.998, '1': 0.002})
    A.setCpt({'111': 0.95, '011': 0.05, '110':0.94,'010':0.06,
    '101':0.29,'001':0.71,'100':0.001,'000':0.999})
    J.setCpt({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})
    M.setCpt({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})

    # 注意：下面evidenceList中将变量的取值统一成字符串的'1'的'0'，而不是数字。这是为了与CPT的键保持一致。
    print("P(A)", end=' ')
    VariableElimination.inference([B,E,A,J,M], ['A'], ['B', 'E', 'J','M'], {})

    print("P(J&&~M)", end=' ')
    VariableElimination.inference([B,E,A,J,M], ['J', '~M'], ['B', 'E', 'A'], {})

    print("P(A|J&&~M)", end=' ')
    VariableElimination.inference([B,E,A,J,M], ['A'], ['E', 'B'], {'J': '1', 'M': '0'})

    print("P(B|A)", end=' ')
    VariableElimination.inference([B,E,A,J,M], ['B'], ['E', 'J', 'M'], {'A': '1'})

    print("P(B|J&&~M)", end=' ')
    VariableElimination.inference([B,E,A,J,M], ['B'], ['E', 'A'], {'J': '1', 'M': '0'})

    print("P(J&&~M|~B)", end=' ')
    VariableElimination.inference([B,E,A,J,M], ['J', '~M'], ['E', 'A'], {'B': '0'})
    