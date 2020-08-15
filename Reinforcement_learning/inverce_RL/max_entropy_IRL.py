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

def expected_svf(trans_probs, trajs, policy):
    n_states, n_actions, _ = trans_probs.shape
    n_t = len(trajs[0])
    mu = np.zeros((n_states, n_t))
    for traj in trajs:
        mu[traj[0][0], 0] += 1
    mu[:, 0] = mu[:, 0] / len(trajs)
    for t in range(1, n_t):
        for s in range(n_states):
            mu[s, t] = sum([mu[pre_s, t - 1] * trans_probs[pre_s, int(policy[pre_s]), s] for pre_s in range(n_states)])
    return np.sum(mu, 1)
            
def max_ent_irl(feature_matrix, trans_probs, trajs,
                gamma=0.9, n_epoch=20, alpha=0.5):
    n_states, d_states = feature_matrix.shape
    _, n_actions, _ = trans_probs.shape

    feature_exp = np.zeros((d_states))
    for episode in trajs:
        for step in episode:
            feature_exp += feature_matrix[step[0], :]
    feature_exp = feature_exp / len(trajs)

    theta = np.random.uniform(size=(d_states,))
    for _ in range(n_epoch):
        r = feature_matrix.dot(theta)
        v = value_iteration(trans_probs, r, gamma)
        pi = best_policy(trans_probs, v,reward)
        exp_svf = expected_svf(trans_probs, trajs, pi)
        grad = feature_exp - feature_matrix.T.dot(exp_svf)
        theta += alpha * grad

    return feature_matrix.dot(theta)

# 経路を生成
def generate_demos(env, policy, n_trajs=100, len_traj=5):
    trajs = []
    for _ in range(n_trajs):
        episode = []
        env.reset()
        for i in range(len_traj):
            cur_s = env.s
            state, reward, done, _ = env.step(policy[cur_s])
            episode.append((cur_s, policy[cur_s], state))
            if done:
                for _ in range(i + 1, len_traj):
                    episode.append((state, 0, state))
                break
        trajs.append(episode)
    return trajs

def value_iteration(trans_probs,reward,gamma=0.9,epsilon = 0.001):
    n_states,n_actions,_ = trans_probs.shape
    Vnext = np.zeros(n_states)
    while 1:
        V = copy.deepcopy(Vnext)   
        delta = 0 
        for s in range(n_states):
            Vnext[s] = max(reward[s] + gamma * np.sum(V*trans_probs[s,:,:],axis=1))
            delta = max(delta,abs(Vnext[s]-V[s]))
        if delta < epsilon * (1-gamma)/gamma:
            return V

def best_policy(trans_probs,V,reward,gamma=0.9):
    n_states,n_actions,_ = trans_probs.shape
    pi = np.zeros(n_states)
    for s in range(n_states):
        pi[s] = np.argmax(reward[s] + gamma * np.sum(V*trans_probs[s,:,:],axis=1))
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

    reward = np.ones((env.nS))*-1
    reward[0] = 1
    reward[env.nS-1]=1

    #方策の計算
    V = value_iteration(trans_probs, reward)
    pi = best_policy(trans_probs, V,reward)

    #方策から逆に報酬を求めてみる
    trajs = generate_demos(env, pi)
    inverse_reward = max_ent_irl(np.eye(env.nS), trans_probs, trajs)
    print(inverse_reward)

    dst = np.zeros(env.shape)
    for i, v in enumerate(inverse_reward):
        dst[int(i / env.shape[1]), i % env.shape[1]] = v
    plt.matshow(dst)
    plt.show()