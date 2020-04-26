# CONTENTS
reinforcement learning

- policy-gradient_catpole:DNNを利用した方策勾配による学習
- dqn_breakout:DQN
- dqn_plot


# REFERENCE
次の変数を必要とする
- 状態S
- 行動A
- 報酬R
- 状態遷移P(r,s'|s,a)

次の概念が存在する
- 方策：どのような行動が最適か、利得を最大にするように選ぶ
- 利得：報酬の時間方向の総和

以下の２つの観点からの学習を今回は考える
- 方策学習：報酬を最大化する方策を直接学習する。ここではSGDを利用する。
- 行動価値学習：Q関数(Q(s,a))を最大化するような方策を選択する。


現在、DQNやTD誤差学習などの他に次の学習もある
- DRQN(deep reccurent Q network)
- A3C(Asynchronous Advantage Actor-Critic)
- UNREAL(UNsupervised REinforcement and Auxiliary Learning)