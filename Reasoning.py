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
import pandas as pd
from Proposition import *

P_total =[]
P_true = []

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

        generate_2 = degenerate_append(generate_1)
        premise_total += generate_2

        generate_1 = generate_2
        if last_premise==premise_total:
            break
        else:
            last_premise = premise_total

    generate_1 = target
    while True:

        generate_1 += mutation_append(generate_1)
        target_total += (generate_1)

        generate_2 = degenerate_append(generate_1)
        target_total += generate_2

        generate_1 = generate_2
        if last_premise == target_total:
            break
        else:
            last_premise = target_total

    return premise_total,target_total















if __name__ == "__main__":
    print("----Start----")

    G = Proposition(['G'], connection=[], out_negative=1, unit=0, value=1)
    H = Proposition(['H'], connection=[], out_negative=0, unit=0, value=1)
    G_H = Proposition([G, H], connection=['->'], unit=0, out_negative=0, value=1)
    G__H = Proposition([G_H, H], connection=['V'], unit=0, out_negative=0, value=1)

    premise = [G__H]

    premise,target = Reasoning(premise,premise)
    for i in premise:

        print(show(i.result))

    print("----End------")
