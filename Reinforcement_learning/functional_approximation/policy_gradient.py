# coding:utf-8
# https://github.com/YutaroOgawa/Deep-Reinforcement-Learning-Book/blob/master/program/2_3_Policygradient.ipynb

'''
方策勾配法：Q(s,a)のような評価関数を必要としない。
連続空間での扱いが容易
本ソースコードでは，離散として扱っているが，関数を導入して連続化可能
勾配を計算するところがやや謎。
流れを掴む程度でこれを参照して。
「スタートからゴールまで動かして更新」を1エピソードとして繰り返す。
'''

import numpy as np
import matplotlib.pyplot as plt

# 方策パラメータthetaを行動方策piにソフトマックス関数で変換
def softmax_convert_into_pi_from_theta(theta):
    beta = 1.0
    [m, n] = theta.shape  # thetaの行列サイズを取得
    pi = np.zeros((m, n))
    exp_theta = np.exp(beta * theta)  # thetaをexp(theta)へと変換
    for i in range(0, m):
        pi[i, :] = exp_theta[i, :] / np.nansum(exp_theta[i, :])
    pi = np.nan_to_num(pi)  # nanを0に変換
    #pi[s,a] = 状態sで行動aをとる確率


# 行動aと1step移動後の状態sを求める関数を定義
def get_action_and_next_s(pi, s):
    direction = ["up", "right", "down", "left"]
    next_direction = np.random.choice(direction, p=pi[s, :])

    if next_direction == "up":
        action = 0
        s_next = s - 3  # 上に移動するときは状態の数字が3小さくなる
    elif next_direction == "right":
        action = 1
        s_next = s + 1  # 右に移動するときは状態の数字が1大きくなる
    elif next_direction == "down":
        action = 2
        s_next = s + 3  # 下に移動するときは状態の数字が3大きくなる
    elif next_direction == "left":
        action = 3
        s_next = s - 1  # 左に移動するときは状態の数字が1小さくなる

    return [action, s_next]

# 迷路を解く関数の定義、状態と行動の履歴を出力
def goal_maze_ret_s_a(pi):
    s = 0 
    s_a_history = [[0, np.nan]]

    while (1):  # ゴールするまでループ
        [action, next_s] = get_action_and_next_s(pi, s)
        s_a_history[-1][1] = action
        # 現在の状態（つまり一番最後なのでindex=-1）の行動を代入
        s_a_history.append([next_s, np.nan])
        # 次の状態を代入。行動はまだ分からないのでnanにしておく
        if next_s == 8:  # ゴール地点なら終了
            break
        else:
            s = next_s
    return s_a_history


# thetaの更新
def update_theta(theta, pi, s_a_history,eta=0.1):
    T = len(s_a_history) - 1  # ゴールまでの総ステップ数
    [m, n] = theta.shape  # thetaの行列サイズを取得
    delta_theta = theta.copy() 

    for i in range(0, m):
        for j in range(0, n):
            if not(np.isnan(theta[i, j])):  # thetaがnanでない場合

                SA_i = [SA for SA in s_a_history if SA[0] == i]
                SA_ij = [SA for SA in s_a_history if SA == [i, j]]
                N_i = len(SA_i)  # 状態iで行動した総回数
                N_ij = len(SA_ij)  # 状態iで行動jをとった回数
                
                #ここの更新則が謎
                #ソフトマックスの偏微分でこうなります？
                #報酬Rとベースラインbも未定義では？
                delta_theta[i, j] = (N_ij - pi[i, j] * N_i) / T
    new_theta = theta + eta * delta_theta
    return new_theta


if __name__ == "__main__":

    # 方策勾配法で迷路を解く
    stop_epsilon = 10**-3  # 方策に変化が少なくなったら学習終了とする

    # 方策を決定するパラメータthetaを設定
    # 行は状態0～7、列は移動方向で↑、→、↓、←を表す
    theta = np.array([[np.nan, 1, 1, np.nan],  # s0
                        [np.nan, 1, np.nan, 1],  # s1
                        [np.nan, np.nan, 1, 1],  # s2
                        [1, 1, 1, np.nan],  # s3
                        [np.nan, np.nan, 1, 1],  # s4
                        [1, np.nan, np.nan, np.nan],  # s5
                        [1, np.nan, np.nan, np.nan],  # s6
                        [1, 1, np.nan, np.nan],  # s7、※s8はゴールなので、方策はなし
                        ])
    pi = softmax_convert_into_pi_from_theta(theta_0)

    is_continue = True
    count = 1
    while is_continue: 
        s_a_history = goal_maze_ret_s_a(pi)  # 方策πで迷路内を探索した履歴を求める
        new_theta = update_theta(theta, pi, s_a_history)  # パラメータΘを更新
        new_pi = softmax_convert_into_pi_from_theta(new_theta)  # 方策πの更新

        print(np.sum(np.abs(new_pi - pi)))  # 方策の変化を出力
        print("迷路を解くのにかかったステップ数は" + str(len(s_a_history) - 1) + "です")

        if np.sum(np.abs(new_pi - pi)) < stop_epsilon:
            is_continue = False
        else:
            theta = new_theta
            pi = new_pi


# 最終的な方策を確認
np.set_printoptions(precision=3, suppress=True)  # 有効桁数3、指数表示しないという設定
print(pi)



'''
# 初期位置での迷路の様子
fig = plt.figure(figsize=(5, 5))
ax = plt.gca()

plt.plot([1, 1], [0, 1], color='red', linewidth=2)
plt.plot([1, 2], [2, 2], color='red', linewidth=2)
plt.plot([2, 2], [2, 1], color='red', linewidth=2)
plt.plot([2, 3], [1, 1], color='red', linewidth=2)

plt.text(0.5, 2.5, 'S0', size=14, ha='center')
plt.text(1.5, 2.5, 'S1', size=14, ha='center')
plt.text(2.5, 2.5, 'S2', size=14, ha='center')
plt.text(0.5, 1.5, 'S3', size=14, ha='center')
plt.text(1.5, 1.5, 'S4', size=14, ha='center')
plt.text(2.5, 1.5, 'S5', size=14, ha='center')
plt.text(0.5, 0.5, 'S6', size=14, ha='center')
plt.text(1.5, 0.5, 'S7', size=14, ha='center')
plt.text(2.5, 0.5, 'S8', size=14, ha='center')
plt.text(0.5, 2.3, 'START', ha='center')
plt.text(2.5, 0.3, 'GOAL', ha='center')

ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
plt.tick_params(axis='both', which='both', bottom='off', top='off',
                labelbottom='off', right='off', left='off', labelleft='off')
line, = ax.plot([0.5], [2.5], marker="o", color='g', markersize=60)
'''