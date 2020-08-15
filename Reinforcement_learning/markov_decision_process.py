# -*- coding:utf-8 -*-

'''
マルコフ決定過程の例
N個のボタンをどの順番で押すかで報酬が異なる
等確率で押されていないボタンを押す
'''

import numpy as np

class Environment():
    def __init__(self,num):
        self.state = np.zeros(num)
        self.num = num
        self.can_move_num = num
        self.reward = 0
        self.move_prob =  1/self.can_move_num

    def transit_func(self):        
        idx = np.random.randint(0,self.can_move_num,1)
        cnt = 0
        for i in range(self.num):
            if self.state[i] ==0:
                if cnt == idx:
                    self.reward += self.reward_calc(i)
                    self.can_move_num -= 1                    
                    self.move_prob_calc()
                    self.state[i] = 1
                    break
                else:
                    cnt = cnt + 1

    def move_prob_calc(self):
        if self.can_move_num != 0:
            self.move_prob = 1/self.can_move_num
        else:
            self.move_prob = 0

    def reward_calc(self,idx):
        if int(np.sum(self.state))%2 == 1:
            return idx + 1
        elif int(np.sum(self.state))%2==0:
            return  self.num*2/(idx+1)

    def reward_get(self):
        print(self.reward)


if __name__ == "__main__":
    mdp_env = Environment(4)
    for i in range(4):
        mdp_env.transit_func()
        mdp_env.reward_get()