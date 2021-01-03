# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Time: 2020/11/19 10:46
# @USER: 86199
# @File: Reasoning
# @Software: PyCharm
# @Author: 张平路
------------------------------------------------- 
# @Attantion：
#    1、
#    2、
#    3、
-------------------------------------------------
"""
import numpy as np

from Proposition import *
import sys

sys.setrecursionlimit(10000)  # 例如这里设置为一百万

P_total =[]
P_true = []

def merge(old,new):

    for i in new:
        flag = 1
        for j in old:
            if i.result == j.result:
                flag = 0
        if flag==1:
            old.append(i)



def mutation_append(premise):

    target = []

    for i in premise:
       res = i.mutation()
       for new in res:
           if new:

                   target.append(new)
                   print(show(new.result) + 'has been added into P_total')




    return target

def generate_append(premise):
    """

    Args:

    Returns:

    """
    target = []

    for i in range(len(premise)-1):
        for j in range(i+1,len(premise)):
            target+=premise[i].generate(premise[j])
    return target


def degenerate_append(premise):
    """

    Args:

    Returns:

    """
    target = []

    for i in range(len(premise)):
        target+=premise[i].degenerate()
    return target



def Reasoning(premise,target):
    """

    Args:

    Returns:

    """
    premise_total = []
    target_total = []
    last_premise = []

    generate_1 = premise

    while True:

        generate_1 += mutation_append(generate_1)
        premise_total += (generate_1)
        merge(premise_total,generate_1)

        generate_2 = degenerate_append(generate_1)
        premise_total += generate_2
        merge(premise_total, generate_2)

        generate_1 = generate_2
        if last_premise==premise_total:
            break
        else:
            last_premise = premise_total

    generate_1 = target
    while True:

        generate_1 += mutation_append(generate_1)
        target_total += (generate_1)
        merge(premise_total, generate_1)

        generate_2 = degenerate_append(generate_1)
        target_total += generate_2
        merge(premise_total, generate_2)

        generate_1 = generate_2
        if last_premise == target_total:
            break
        else:
            last_premise = target_total

    return premise_total,target_total


def Prove(target,premise):
    if target.child == []:
        for i in premise:
            if i.equal(target):
                return 1;
    for i in target.brother:
        if Prove(i,premise)==1:
            return 1;

    for i in target.child:
        if Prove(i,premise)==1:
            return 1;

















if __name__ == "__main__":
    print("----Start----")

    G = Proposition(['G'], connection=[], out_negative=1, unit=1, value=1)


    H = Proposition(['H'], connection=[], out_negative=0, unit=1, value=1)
    G_H = Proposition([G, H], connection=['V'], unit=0, out_negative=0, value=1)
    G__H = Proposition([G, H], connection=['->'], unit=0, out_negative=0, value=1)

    premise = [G_H]

    premise,target = Reasoning(premise,premise)
    for i in premise:
        # if i.value == 1:

          print(show(i.result))

    print(premise[2]==premise[3])


    print("----End------")
