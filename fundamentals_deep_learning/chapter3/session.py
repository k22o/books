# -*- coding:utf-8 -*-

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

'''
目的：tensorflow の session機能を理解すること。
session:初期状態の計算グラフの構築をする
'''
'''
変数の初期設定について
・入力データのメモリをplaceholderによって用意する
  これをもちいることで、ミニバッチ学習が容易になる
・重み,バイアスをVariableで用意する。
'''
#784次元から10次元に変換するための計算グラフの設計
x = tf.placeholder(tf.float32, name='x', shape=[None,784])
W = tf.Variable(tf.random_uniform([784,10],-1,1),name='w')
b = tf.Variable(tf.zeros([10]),name='biases')
#outputを計算する
output = tf.matmul(x,W) + b

#計算グラフを構築
init_op = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init_op)

#MINSTのDLとバッチ化, xはデータ,yはラベル
mnist = input_data.read_data_sets("data", one_hot=True)
minibatch_x, minibatch_y = mnist.train.next_batch(32)

#部分グラフを実行する
feed_dict = {x: minibatch_x}
sess.run(output, feed_dict=feed_dict)