# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import copy
import gridworld as gw
#https://qiita.com/shiro-kuma/items/aaab6184aea7d285b103


# 方策反復法
def policy_iteration(trans_probs,reward,gamma=0.9,epsilon = 0.001):
    n_states,n_actions,_ = trans_probs.shape
    pi = np.random.randint(0,n_actions,n_states)
    pi_next = np.zeros(n_states)
    Bv = np.zeros(n_states)#np.random.rand(n_states)
    cnt = 0
    while 1:
        #方策価値関数の算出
        for s in range(n_states):
            Bv[s] = reward[s,int(pi[s])]+ gamma* np.sum(Bv*trans_probs[s,int(pi[s]),:])
        for s in range(n_states):
            pi_next[s] = np.argmax(reward[s,:] + gamma*np.sum(Bv*trans_probs[s,:,:],axis=1))        
        cnt = cnt+1
        print("{}:{}".format(cnt,pi_next))

        if all(pi_next == pi):
            return pi
        pi = copy.deepcopy(pi_next)
            

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
    pi = policy_iteration(trans_probs,reward)

    #可視化
    dist = np.zeros((env.shape))
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