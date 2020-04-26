# CONTENTS
seq2seq問題(シーケンスtoシーケンス)
英文の英語文への変換をする

1)シーケンスをトークン化し、埋め込み表現にする
2)トークンをエンコーダ(RNN)に入れる
3)RNNへの入力終了タグEOMを感知する
4)デコーダがEOMを受け取り、変換先の値を出す
5)1ステップ前の出力を次の入力として、文を生成する

-seq2seq_model:データを成型
-translate:翻訳
-seq2seq:関数群
-data_util:関数群

 #REFERENCE
 ・スキップソートベクターを利用した手法<br>
 Kiros,Ryan, et al. "Skip-Thought Vectors".
 ・アテンションを利用した手法<br>
 Bahdanau et al. "Nerural Machine Translation by Jointly Learning
 to Align and Translate"
 ・TenserFlowのサンプル
 https://github.com/tensorflow/tensorflow/tree/r0.7/tensorflow/models/rnn/translate
