※　メモ
あとニューラル系を終わらせて終了にしましょう


# Reinforcement learning 
- basic_algo_model_known
    - モデルが既知の場合の学習
    - すなわち，行動a，状態s,報酬r,遷移確率pなどが全て既知
    - 例：価値反復法，行動反復法，(線形計画法)

- basic_algo_model_free
    - モデルフリーのオンライン学習
    - モデルフリーのバッチ学習については，行動をいろいろさせてログを取って，動的計画法に持ち込む
    - 状態sと行動aから報酬rと次の状態s_primeが分かる場合
    - 具体的な状態遷移条件がわからない
    - Actor-ctiric, SARSA,Q学習，(TD誤差学習)
    - 純粋なTD法は自分で方策を定める必要があるので，今回はなしです。

未実装
- model_unknown_estimation
    - バッチ型
        - (s,a,s_next,r)は分かっても遷移確率や報酬関数が不明な場合
            - 過去のデータから推定して，動的計画法へ(モデルフリーバッチ学習とほぼ同)
            - ベイジアン強化学習
        - 報酬rもよくわからない
            - 模倣学習/逆強化学習(別ディレクトリ)
        - ブラックボックスのまま，最適方策を探索する(model_freeとほぼ同)
            - スパースサンプリング法・UTC法・モンテカルロ法
    - オンライン型
        - Rmax法


近似Q学習のみ実装
- functional_approximation
    - 関数近似手法(NN除く)
    - 自分で適切な近似関数を設定する必要がある
    - 価値関数の近似
        - table拡張
            - バッチ学習
                - 適合価値反復法・適合Q反復法・ニューラルQ学習系
            - オンライン学習
                - 近似TD法・近似Q学習・近似SARSA法
        - 損失関数の利用
            - 勾配TD法・最小二乗TD法
    - 方策の近似
        -　モンテカルロ方策勾配法・アクター・クリティック方策勾配法

- neural RL
    - ニューラルネットを利用した関数近似手法
    - 離散テーブルはメモリを食いすぎるので，関数りを利用して削減する

- inverse_RL
    - 逆強化学習
    - 状態と行動はわかっているが，報酬設定がよくわからない
    - 事前情報や熟達者(最適である必要はない)の行動をもとに，報酬を推定して，その後強化学習をする

    
- sample_cartpole.py
- markov_decision_process.py


参考サイト他
https://www.kumilog.net/entry/openai-gym-rl
http://neuro-educator.com/rl1/
https://www.kumilog.net/entry/openai-gym-rl
https://github.com/icoxfog417/baby-steps-of-rl-ja/blob/master/DP/environment.py
