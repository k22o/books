# -*- coding:utf-8 -*-
#https://qiita.com/shiro-kuma/items/aaab6184aea7d285b103

import numpy as np
import matplotlib.pyplot as plt
import copy
import gridworld as gw

# 価値反復法
'''
V(s) = max_a(R(s,a) + \gamma \sum_sp P(sp|s,a)V(sp))
\pi(s) = argmax_a (R(s,a) + gamma*\sum_sp P(sp|s,a)V(sp))
'''
def value_iteration(trans_probs,reward,gamma=0.9,epsilon = 0.001):
    n_states,n_actions,_ = trans_probs.shape
    Vnext = np.zeros(n_states)
    while 1:
        V = copy.deepcopy(Vnext)   
        delta = 0 
        for s in range(n_states):
            Vnext[s] = max(reward[s,:] + gamma * np.sum(V*trans_probs[s,:,:],axis=1))
            delta = max(delta,abs(Vnext[s]-V[s]))
        if delta < epsilon * (1-gamma)/gamma:
            return V

def best_policy(trans_probs,V,reward,gamma=0.9):
    n_states,n_actions,_ = trans_probs.shape
    pi = np.zeros(n_states)
    for s in range(n_states):
        pi[s] = np.argmax(reward[s,:] + gamma * np.sum(V*trans_probs[s,:,:],axis=1))
    return pi

if __name__ == "__main__":

    env = gw.GridworldEnv()
    env.reset()
    env.render(mode='human')

    #初期設定 [0]と[15]のマスは報酬1,他は-1
    #4方向にランダムに進む(進めないときはその場に留まる)    
    trans_probs = np.zeros((env.nS,env.nA,env.nS))    
    edge = env.shape[1]
    for i in range(env.nS):
        trans_probs[i,gw.UP,i-edge if i-edge>=0 else i] = 1/4
        trans_probs[i,gw.DOWN,i+edge if i+edge<env.nS else i] = 1/4
        trans_probs[i,gw.RIGHT,i+1 if i%edge !=edge-1 else i] = 1/4
        trans_probs[i,gw.LEFT,i-1 if i%edge !=0 else i] = 1/4

    reward = np.ones((env.nS,env.nA))*-1
    reward[0,:] = 1
    reward[env.nS-1,:]=1

    #計算
    V = value_iteration(trans_probs,reward)#最適価値関数
    pi = best_policy(trans_probs,V,reward)#最適方策

    #可視化
    dist = np.zeros((env.shape))
    for k,v in enumerate(V):
        dist[int(k/env.shape[1]),k%env.shape[1]] = v
    print(dist)
    plt.matshow(dist)
    for k,v in enumerate(pi):
        if v == gw.UP:
            plt.arrow(int(k/env.shape[1]),k%env.shape[1],-0.4,0,head_width=0.05)
        elif v == gw.RIGHT:
            plt.arrow(int(k/env.shape[1]),k%env.shape[1],0,0.4,head_width=0.05)
        elif v == gw.DOWN:
            plt.arrow(int(k/env.shape[1]),k%env.shape[1],0.4,0,head_width=0.05)
        elif v == gw.LEFT:
            plt.arrow(int(k/env.shape[1]),k%env.shape[1],0,-0.4,head_width=0.05)
    plt.show()