# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import copy
import gym

'''
要検討・うまく学習できているか不明

関数近似手法による強化学習
・オンライン的な逐次更新
・基底関数にはF(s,a)とF(s)がある
・今回は各行動にパラメタの異なるF(s)があることとした。
・すなわち，行動a,状態sのQ値なら，F(s)[a]みたいなイメージ

'''

class LinearFuncApproxAgent():
    def __init__(self,numOfbase,numOfaction,mu,sigma,epsilon=0.1):
        self.mu = mu
        self.sigma = sigma
        self.params = np.zeros((numOfbase,numOfaction))
        self.numOfaction = numOfaction
        self.epsilon = epsilon

    def basic_function(self,s):
        return np.exp(-(s-self.mu)*(s-self.mu)/(2*self.sigma*self.sigma))

    def q_calc(self,s,a):
        return np.dot(self.params[:,a], self.basic_function(s))

    def policy(self,s):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.numOfaction)
        else:
            tmpQ = np.zeros(self.numOfaction)
            for a in range(self.numOfaction):
                tmpQ[a] = self.q_calc(s,a)
            return np.argmax(tmpQ)            

    def update_params(self,s,next_s,a,reward,alpha=0.05):
        nextQ = np.zeros(self.numOfaction)
        for i in range(self.numOfaction):
            nextQ[i] = self.q_calc(next_s,i)
        self.params[:,a] = self.params[:,a] + alpha*(reward + np.max(nextQ) - self.q_calc(s,a))*self.basic_function(s)



if __name__ == "__main__":

    env = gym.make('CartPole-v0')
    mu = np.array([0.1,0.3,0.5,0.7])
    sigma = np.array([1,1,1,1])
    agent = LinearFuncApproxAgent(4,env.action_space.n,mu,sigma)

    num_episodes = 500  # 総試行回数
    max_number_of_steps = 2000
    islearned = False

    for episode in range(num_episodes):  # 試行数分繰り返す
        s = env.reset()
        a = agent.policy(s)

        for t in range(max_number_of_steps):  # 1試行のループ
            env.render()

            if islearned:  # 学習終了したらcartPoleを描画する
                time.sleep(0.1)
                print(observation[0])  # カートのx位置を出力

            next_s, reward, done, info = env.step(a)
            agent.update_params(s,next_s,a,reward)
            s = next_s
            a = agent.policy(s)

            if done:
                break
