# -*- coding:utf-8 -*-
# https://qiita.com/shiro-kuma/items/aaab6184aea7d285b103#maximum-entropy-irl

import numpy as np
import copy
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import gridworld as gw

# 最適な行動を既知として，そこから報酬を求めよう
# 線形計画法を利用する
# basic_algo_model_knownからの発展形

def lp_irl(trans_probs, policy, gamma=0.2, l1=1.5, Rmax=5.0):
    n_states, n_actions, _ = trans_probs.shape
    A = set(range(n_actions))
    tp = np.transpose(trans_probs, (1, 0, 2))
    ones_s = np.ones(n_states)
    eye_ss = np.eye(n_states)
    zero_s = np.zeros(n_states)
    zero_ss = np.zeros((n_states, n_states))
    T = lambda a, s: np.dot(tp[int(policy[s]), s] - tp[a, s], np.linalg.inv(eye_ss - gamma * tp[int(policy[s])]))

    c = -np.r_[zero_s, ones_s, -l1 * ones_s]
    zero_stack = np.zeros((n_states * (n_actions - 1), n_states))
    T_stack = np.vstack([-T(a, s) for s in range(n_states) for a in A - {policy[s]}])
    I_stack = np.vstack([np.eye(1, n_states, s) for s in range(n_states) for a in A - {policy[s]}])

    A_ub = np.bmat([[T_stack, I_stack, zero_stack],    # -TR <= t
                    [T_stack, zero_stack, zero_stack], # -TR <= 0
                    [-eye_ss, zero_ss, -eye_ss],  # -R <= u
                    [eye_ss, zero_ss, -eye_ss],   # R <= u
                    [-eye_ss, zero_ss, zero_ss],  # -R <= Rmax
                    [eye_ss, zero_ss, zero_ss]])  # R <= Rmax
    b = np.vstack([np.zeros((n_states * (n_actions-1) * 2 + 2 * n_states, 1)),
                   Rmax * np.ones((2 * n_states, 1))])
    results = linprog(c, A_ub, b)

    return results["x"][:n_states]


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

    
if __name__ == '__main__':
    '''
    強化学習で求めた方策から，逆強化学習で報酬を推定する
    '''
    
    env = gw.GridworldEnv()
    env.reset()

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

    #方策の計算
    V = value_iteration(trans_probs, reward)
    pi = best_policy(trans_probs, V,reward)

    #方策から逆に報酬を求めてみる
    inverse_reward = lp_irl(trans_probs, pi)
    print(inverse_reward)

    dst = np.zeros(env.shape)
    for i, v in enumerate(inverse_reward):
        dst[int(i / env.shape[1]), i % env.shape[1]] = v
    plt.matshow(dst)
    plt.show()