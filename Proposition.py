# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Time: 2020/11/9 18:28
# @USER: 86199
# @File: Proposition
# @Software: PyCharm
# @Author: 张平路
------------------------------------------------- 
# @Attantion：
#    1、
#    2、
#    3、
-------------------------------------------------
"""
import types
import logging
import copy

logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %I:%M:%S %p')


def show(res):
    """
    delete surplus brackets
    Args:
    res string
    example；((GVH)^(HVG))
    Returns:
    (GVH)^(HVG)
    """
    if res[0] == '(' and res[-1] == ')':
        res = res[1:-1]
    return res

class Proposition():
    """the object of the class is basic unit in Proposition

    Attributes:
        name: a list involved string or object
        connection: a list involved sign
        negative: whether out the proposition having ~
        value: 1 or 0
        unit: 1 or 0 whether object or string in name

    """
    def __init__(self,name,connection = [],out_negative = 0,value = -1,unit = 1,parent = [],brother = [],child = []):
        self.name = name
        self.connection = connection
        self.out_negative = out_negative
        self.value = value
        self.unit = unit & ~out_negative
        self.result = ''
        self.result_flag = 0
        self.result_str()
        self.parent = parent
        self.child = child
        self.brother = brother
        print('the Proposition '+show(self.result) +' have been created')


    def __eq__(self,other):
        """
        overwrite the __eq__ function to judge the equality between two objects
        Args:

        Returns:
        boolen value
        """
        self.result_str()
        other.result_str()
        if type(other)==type('a'):
            logging.warning('can\'t match str and object')
            return False
        flag = 1

        if len(self.name)==len(other.name):
            if len(self.name)==1:
                if self.name[0]!=other.name[0]:
                    flag = 0
            elif (self.name[0] == other.name[0] and self.name[1]==other.name[1]) or (self.name[0]==other.name[1] and self.name[1]==other.name[0] and self.connection
                                       == other.connection != ['->']):
                flag = 1

        else:
            flag = 0

        if self.connection != other.connection:
            flag = 0
        if self.out_negative != other.out_negative:
            flag = 0
        if self.value != other.value:
            flag = 0
        if self.unit != other.unit:
            flag = 0
        return flag

    def result_str(self):
        """assemble the name and connection

        Args:
           self
        Returns:
           a visualized string
        """
        if self.result != '' and self.result_flag==1:
             return self.result

        if self.out_negative==1:
               self.result+='~'
        if self.out_negative==1 or len(self.name)!=1:
                   self.result+='('

        n = 0
        for i in self.name:
            if type('a')==type(i):
                self.result+=i
                if n!=len(self.name)-1:
                  self.result+=self.connection[n]
                  n = n+1
            else:
                self.result+=i.result_str()
                if n != len(self.name) - 1:
                    self.result += self.connection[n]
                    n = n + 1

        if self.out_negative==1 or len(self.name)!=1:
               self.result+=')'
        self.result_flag = 1
        res = str(self.result)
        return res



        return str(res)

    def check(self):
        """
        check the validity of the Proposition
        Args:

        Returns:

        """
        flag = 0
        if len(self.name)!=len(self.connection)+1:
            logging.warning("The number of connection and name in Proposition might not match")
            flag=1

        if self.unit == 1 & self.out_negative==1:
            logging.warning("There is a conflict in judging unit")
            flag =1

        sign = ['V','^','->','~','<->']
        for i in self.connection:
            if i not in sign:
                logging.warning('there might be invalid sign in Proposition')
                flag = 1

        for i in self.name:
            if type(i)==type('a'):
                if i < 'A' or i > 'Z':
                    logging.warning('the Proposition should be from A to Z')
                    flag=1
                if i == 'V':
                    logging.warning('try to not use V in Proposition')
                    flag = 1

            else:
                if False == i.check():
                    flag =1

            if self.unit == 1:
                for i in self.name:
                    if type(i)!=type('a'):
                        logging.warning('the content of unit might not be string')
                        flag = 1


            if flag==0:
                print(show(self.result)+' has been checked without problems')
                return True
            else:
                logging.warning(show(self.result)+' has been checked with problems!!!')
                return False

    def change_out_negative(self):
        """change unit while changing the out_negative

           out_negative+1
           judge unit

        Args:
           self

        Returns:
            None

        """
        new = copy.deepcopy(self)
        # new.brother = [self]
        # self.brother = [new]
        last = self.result

        new.out_negative = (self.out_negative+1)%2
        new.unit = self.unit and ~self.out_negative and len(self.name)==1

        if self.value==-1:
            new.value = -1
        else:
            new.value = (self.value+1)%2

        new.result = ''
        new.result_flag = 0
        new.parents = [self]
        new.result_str()
        print('the Proposition '+last+' has transformed into to '+show(new.result)+' through the rule change_out_negative')
        return new




    def simplication(self):
        """
        G^H =>G
        G^H =>H

        Args:
        self = G^H


        Returns:
            G and H
        """
        if len(self.name)==2 and self.connection == ['^'] and self.value == 1 and self.out_negative==0 and self.unit==0:
            print(show(self.result)+ ' reason a new Proposition ' + show(self.name[0].result) +' and '+
                  show(self.name[1].result)+' through the rule simplication')
            self.name[0].value = 1
            self.name[1].value = 1
            self.child += [self.name[0],self.name[1]]
            self.name[0].parent += [self]
            self.name[1].parent += [self]
            return self.name[0],self.name[1]
        else:
            print('the rule simplication may not match ' + show(self.result))
            pass

    def negative_have_transform(self):
        """
        ~(G->H)=>G,~H
        :return:
        """
        if len(self.name)==2 and self.out_negative == 1 and self.value==1 and self.connection==['->'] and self.unit==0:
            a = copy.deepcopy(self.name[0])
            b = copy.deepcopy(self.name[1])
            b.change_out_negative()
            self.child += [a, b]
            a.parent += [self]
            b.parent += [self]
            print(show(self.result) +' reason a new Proposition ' + show(a.result) + ' and '+
                  show(b.result)+' through the rule negative_have_transform')
            return a,b
        else:
            print('the rule negative_have_transform may not match ' + show(self.result))
            pass




    def addition(self,a):
        """
        G =>GVH
        H =>GVH

        self G
        a H

        """
        if self.value==1 or a.value==1:
            name = []
            name.append(a)
            name.append(self)
            new = Proposition(name,['V'],unit=0,value=1)
            self.child += [new]
            a.child += [new]
            new.parent += [self]
            print(
                show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' + show(new.result) + ' through the rule addition')
            return new
        else:
            print('the rule addition may not match ' + show(self.result) + ' and ' + show(a.result))
            pass

    def sum_transform(self,a):
        """
        G,H =>G^H

        self G
        a H
        """
        if self.value==1 and a.value == 1:
            name = []
            name.append(a)
            name.append(self)
            new = Proposition(name,connection=['^'],unit=0,value=1)
            self.child += [new]
            a.child += [new]
            new.parent += [self]
            print(show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule sum_transform')
            return new
        else:
            print('the rule sum_transform may not match' + show(self.result) + ' and ' + show(a.result))
            pass

        def have_transform_1(self, a):
            """
            ~G => G->H

            Args:
              ~G
            Returns:
                G->H
            """
            if self.value == 1:

                name = []
                b = copy.deepcopy(self)
                b.change_out_negative()
                name.append(b)
                name.append(a)
                new = Proposition(name, ['->'], unit=0)
                print(show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' + show(
                    new.result) + ' through the rule have_transform_1')
                return new
            else:
                print('the rule have_transform_1 may not match ' + show(self.result) + ' and ' + show(a.result))
                pass

    def have_transform_1(self,a):
        """
        ~G => G->H

        Args:
          ~G
        Returns:
            G->H
        """
        if self.value == 1:

            name = []
            b = copy.deepcopy(self)
            b.change_out_negative()
            name.append(b)
            name.append(a)
            new = Proposition(name,['->'],unit=0,value=1)
            self.child += [new]
            a.child += [new]
            new.parent += [self]
            print(show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' + show(new.result) + ' through the rule have_transform_1')
            return new
        else:
            print('the rule have_transform_1 may not match ' + show(self.result) + ' and ' + show(a.result))
            pass

    def have_transform_2(self,a):
        """
        H=>G->H
         Args:
             self H
             a G
        Returns:
            G->H
        """
        if a.value==1:
            name = []
            name.append(a)
            name.append(self)
            new = Proposition(name, connection= ['->'],unit=0,value=1)
            self.child += [new]
            a.child += [new]
            new.parent += [self]
            print(show(self.result)+' and '+show(a.result)+' reason a new Proposition '+show(new.result)+' through the rule have_transform_2')
            return new
        else:
            print('the rule have_transform_2 may not match '+show(self.result)+' and '+show(a.result))
            pass




    def disjunctive_syllogism(self,a):
        """
        ~G,GVH=>H

        self G
        a GVH
        """
        if self.value==1 and a.value==1 and a.connection == ['V'] and a.unit == 0:
            b = copy.deepcopy(self)
            b = b.change_out_negative()
            if b==a.name[0]:
                new = a.name[1]
                new.value = 1
                self.child += [new]
                a.child += [new]
                new.parent.append([self,a])
                print(show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' + show(
                    new.result) + ' through the rule disjunctive_syllogism')
                return new
            else:
                print('the opposion of'+show(self.result)+' might not equal with the former of '+
                      show(a.result)+' in rule disjunctive_syllogism')
                pass



        else:
            print('the rule disjunctive_syllogism may not match ' + show(self.result) + ' and ' + show(a.result))
            pass

    def modus_ponen(self,a):
        """
        G,G->H=>H

       self G
       a G->H
        """
        if self.value==1 and a.value == 1 and a.connection == ['->'] and a.unit ==0 and len(a.name)==2:
            if self == a.name[0]:
                new = a.name[1]
                new.value  =1
                self.child += [new]
                a.child += [new]
                new.parent.append([self,a])
                print(show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' + show(
                    new.result) + ' through the rule modus_ponen')
                return new
            else:
                print(show(self.result) + ' might not equal with the latter Proposition of ' +
                      show(a.result)+'in rule modus_ponen')
                pass

        else:
            print('the rule modus_ponen may not match ' + show(self.result) + ' and ' + show(a.result))
            pass

    def modus_tollen(self,a):
        """
        ~H,G->H=>~G

        self ~H
        a G->H
        """
        if self.value==1 and a.value == 1 and a.connection == ['->'] and a.unit == 0 and len(a.name)==2:
            b = copy.deepcopy(self)
            b = b.change_out_negative()
            if b == a.name[1]:
                new = copy.deepcopy(a.name[0])
                new = new.change_out_negative()
                new.value = []
                self.child += [new]
                a.child += [new]
                new.parent.append([self,a])
                print(show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' + show(
                    new.result) + ' through the rule modus_tollen')
                return new
            else:
                print(show(self.result) + ' might not equal with the latter Proposition of ' +
                      show(a.result) + ' in rule modus_tollen')
                pass
        else:
            print('the rule modus_tollen may not match ' + show(self.result) + ' and ' + show(a.result))
            pass

    def hypothelical_syllogism(self,a):
        """
        G->H,H->I=>G->I

        self G->H
        a H->I
        """
        if self.value == 1 and a.value == 1 and a.connection == ['->'] and len(self.name)==2 and self.name[1] == a.name[0] and self.connection == ['->']:

            new = Proposition([self.name[0],a.name[1]],connection=['->'])
            new.value = 1
            self.child += [new]
            a.child += [new]
            new.parent.append([self,a])
            print(show(self.result) + ' and ' + show(a.result) + ' reason a new Proposition ' + show(
                new.result) + ' through the rule hypothelical_syllogism')
            return new
        else:
            print('the rule hypothelical_syllogism may not match ' + show(self.result) + ' and ' + show(a.result))
            pass






    def arrow_transform_1(self):
        """
        G->H => ~GVH

        self G->H

        """
        if self.value==1 and self.connection==['->'] and len(self.name)==2:
            G = copy.deepcopy(self.name[0])
            G = G.change_out_negative()
            name = [G,self.name[1]]

            new = Proposition(name,connection=['V'],value=self.value)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule arrow_transform_1')
            return new
        else:
            print('the rule arrow_transform_1 may not match ' + show(self.result))
            pass

    def arrow_transform_2(self):
        """
        ~GVH=>G->H

        Args:
        self  ~GVH
        Returns:

        """
        if self.value==1 and len(self.name)==2 and self.unit == 0 and self.connection == ['V'] and len(self.name)==2:

            G = copy.deepcopy(self.name[0])
            G = G.change_out_negative()
            name = [G, self.name[1]]

            new = Proposition(name, connection=['->'],value =1 )
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule arrow_transform_2')
            return new
        else:
            print('the rule arrow_transform_2 may not match ' + show(self.result))
            pass

    def two_way_arrow_transform(self):
        """
        P<->Q = (~PVQ)^(~QVP)

        Args:
        self P<->Q
        Returns:
        (~PVQ)^(~QVP)
        """
        if len(self.name)==2 and self.connection == ['<->'] and self.unit == 0 and self.value == 1 and self.out_negative==0:


            P_ = copy.deepcopy(self.name[0])
            P_.change_out_negative()


            Q_ = copy.deepcopy(self.name[1])
            Q_.change_out_negative()

            new_1 = Proposition([P_,self.name[1]],connection=['V'],unit=0)
            new_2 = Proposition([Q_, self.name[0]], connection=['V'], unit=0)
            new = Proposition([new_1,new_2],connection='^',unit=0,value = self.value)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule two_way_arrow_transform')
            return new
        else:
            print('the rule two_way_arrow_transform may not match ' + show(self.result))
            pass

    def negate_transform(self):
        """
        P^Q = ~(~PV~Q)
        Args:

        Returns:

        """
        if self.value == 1 and self.connection==['^'] and self.unit == 0:
            new_P = copy.deepcopy(self.name[0])
            new_P = new_P.change_out_negative()
            new_Q = copy.deepcopy(self.name[1])
            new_Q= new_Q.change_out_negative()
            new = Proposition(name=[new_P,new_Q],unit=0,value = self.value,connection=['V'],out_negative=1)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule negate_transform')
            return new
        else:
            print('the rule negate_transform may not match ' + show(self.result))
            pass

    def De_Morgan_1(self):
        """

        ~(GVH) = ~G^~H
        """
        if self.out_negative == 1 and self.connection == ['V'] and self.unit == 0:
            G = self.name[0]
            G = G.change_out_negative()
            H = self.name[1]
            H = H.change_out_negative()

            new = Proposition([G,H],connection=['^'],value=self.value,unit=0)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule De_Morgan_1')
            return new
        else:
            print('the rule De_Morgan_1 may not match ' + show(self.result))
            pass

    def De_Morgan_2(self):
        """

         ~(G^H) = ~GV~H
        """
        if self.out_negative == 1 and self.connection == ['^'] and self.unit == 0:
            G = self.name[0]
            G = G.change_out_negative()
            H = self.name[1]
            H = H.change_out_negative()

            new = Proposition([G, H], connection=['V'], value=self.value, unit=0)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule De_Morgan_2')
            return new
        else:
            print('the rule De_Morgan_2 may not match ' + show(self.result))
            pass

    def De_Morgan_3(self):
        """

        ~G^~H = ~(GVH)
        """
        if self.out_negative == 0 and self.connection == ['^'] and self.unit == 0:
            G = self.name[0]
            G = G.change_out_negative()
            H = self.name[1]
            H = H.change_out_negative()

            new = Proposition([G,H],connection=['V'],value=self.value,unit=0,out_negative=1)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule De_Morgan_3')
            return new
        else:
            print('the rule De_Morgan_3 may not match ' + show(self.result))
            pass

    def De_Morgan_4(self):
        """

        ~GV~H = ~(G^H)
        """
        if self.out_negative == 0 and self.connection == ['V'] and self.unit == 0:
            G = self.name[0]
            G = G.change_out_negative()
            H = self.name[1]
            H = H.change_out_negative()

            new = Proposition([G, H], connection=['^'], value=self.value, unit=0,out_negative=1)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule De_Morgan_4')
            return new
        else:
            print('the rule De_Morgan_4 may not match ' + show(self.result))
            pass

    def equal_rule_1(self):
        """
        G<->H = ~H<->~G
        Args:

        Returns:

        """
        if self.out_negative == 0 and self.connection == ['<->'] and self.unit == 0 and len(self.name)==2:
            G = self.name[0]
            G = G.change_out_negative()
            H = self.name[1]
            H = H.change_out_negative()
            new = Proposition([H, G], connection=['<->'], value=self.value, unit=0, out_negative=0)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule equal_rule_1')
            return new
        else:
            print('the ruleequal_rule_1 may not match ' + show(self.result))
            pass

    def equal_rule_2(self):
        """
        G->H = ~H->~G
        Args:

        Returns:

        """
        if self.out_negative == 0 and self.connection == ['->'] and self.unit == 0 and len(self.name) == 2:
            G = self.name[0]
            G = G.change_out_negative()
            H = self.name[1]
            H = H.change_out_negative()
            new = Proposition([H, G], connection=['->'], value=self.value, unit=0, out_negative=0)
            self.brother += [new]
            new.brother += [self]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(new.result) + ' through the rule equal_rule_2')
            return new
        else:
            print('the ruleequal_rule_2 may not match ' + show(self.result))
            pass

    def split_1(self):

        """
        GVH =>G or H

        :return:
        """

        if self.value==1 and self.connection == ['V'] and self.out_negative == 0:

            G = self.name[0]
            H = self.name[1]
            G.parent += [self]
            H.parent += [self]
            self.child +=[G,H]
            G.value = -1
            H.value = -1

            print(show(self.result) + ' reason a new Proposition ' +
                show(G.result) +' and '+show(H.result) +' through the rule split_1')
            return G,H

        elif  self.value==0 and self.connection == ['V']:
            G = self.name[0]
            H = self.name[1]
            G.value = 0
            H.value = 0
            G.parent += [self]
            H.parent += [self]
            self.child += [G, H]
            print(show(self.result) + ' reason a new Proposition ' +
                  show(G.result) + ' and ' + show(H.result) + ' through the rule split_1')
            return G,H



        else:
            print('the split_1 may not match ' + show(self.result))
            pass

    def split_2(self):

        """
        G^H =>G
        G^H => H
        :return:
        """

        if self.value == 1 and self.connection == ['^'] and self.out_negative == 0 and self.unit == 0:

            G = self.name[0]
            H = self.name[1]
            G.parent += [self]
            H.parent += [self]
            self.child.append([G, H])


            return G,H

        else:
            print('the split_2 may not match ' + show(self.result))
            pass








    def mutation(self):
        """

        Args:

        Returns:

        """
        target = []
        mutation_function = [self.change_out_negative,self.arrow_transform_1,self.arrow_transform_2,
                             self.two_way_arrow_transform,self.negate_transform,self.De_Morgan_1,self.De_Morgan_2,
                             self.De_Morgan_3,self.De_Morgan_4,self.equal_rule_1,self.equal_rule_2]
        for i in mutation_function:
            new = i()
            if new:
                target.append(new)
        return target

    def generate(self,other):
        child = []
        generate_function_1 = [self.hypothelical_syllogism,self.modus_tollen,self.modus_ponen,
                               self.disjunctive_syllogism]
        generate_function_2 = [other.hypothelical_syllogism, other.modus_tollen, other.modus_ponen,
                               other.disjunctive_syllogism]
        for i in generate_function_1:
            new = i(other)
            if new:
                child.append(new)

        for i in generate_function_2:
            new = i(self)
            if new:
                child.append(new)

        return child

    def degenerate(self):
        child = []
        generate_function_1 = [self.simplication, self.negative_have_transform,self.split_1,self.split_2]

        for i in generate_function_1:
            new = i()

            if new:
                if type(new) == type((1,2)):
                    child.append(new[0])
                    child.append(new[1])
                else:
                    child.append(new)





        return child



if __name__ == "__main__":
    print("----Start----")
    G = Proposition(['G'],connection=[],out_negative=0,unit=1,value=1)
    H = Proposition(['H'],connection=[],out_negative=0,unit=1,value=1)
    G_H = Proposition([G,H],connection=['^'],unit=0,out_negative=0,value = 1)
    G__H = Proposition([H,G], connection=['^'], unit=0, out_negative=0, value=1)


    print(show(G_H.negate_transform().result_str()))
    print(G_H==G__H)









    print("----End------")
