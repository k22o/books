# メモリ強化型ネットワーク
RNNはチューリング完全(適切な設定で計算可能な問題はすべて解決可能)だが、
実際に実装するのは極めて困難。
ここで、作業記憶の概念を取り入れた、NTM(neural turing machine)を導入する。<br>
(https://arxiv.org/abs/1410.5401)<br>
具体的には、RNNに対して、外部記憶を加えることで、探索空間を枝刈りできる。
これの発展形として、DNCを扱う。<br>
("hybrid computing using a neural network with dynamic external memory")<br>
DNCは、NTMのデータ間の干渉や、メモリの再利用不可性を解消したものである。



# CONTENTS
- lt_loop_vs_vectorize:for文とベクトルの違いの説明
- while_loop:tf.while_loopの使い方
- dnc
    - mem_pos:実装のメインとなるファイル
    - train_babi:訓練部分
    - test_babi:テスト部分
    - preprocess

