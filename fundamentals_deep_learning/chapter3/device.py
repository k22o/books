# -*- coding:utf-8 -*-
import tensorflow as tf

'''
計算環境の切り替え
GPUが利用可能の場合は、特に指定しなければ自動で使ってくれる。
'''

#もし使う計算環境を指定する場合は、以下のようにしてデバイスを作成する
with tf.device("/gpu:2"):
    a = tf.constant([1.0, 2.0, 3.0, 4.0], shape=[2, 2], name="a")
    b = tf.constant([1.0, 2.0], shape=[2, 1], name="b")
    c = tf.matmul(a, b)

sess = tf.Session(
    config=tf.ConfigProto(
        allow_soft_placement=True,#もし指定した環境がなければ別を探す
        log_device_placement=True
    )
)

sess.run(c)
#########################

#例２GPU0とGPU1の計算結果をもとにCPU0で計算させる

c = []

for d in ["/gpu:0", "/gpu:1"]:
    with tf.device(d):
        a = tf.constant([1.0, 2.0, 3.0, 4.0], shape=[2, 2], name="a")
        b = tf.constant([1.0, 2.0], shape=[2, 1], name="b")
        c.append(tf.matmul(a, b))

with tf.device("/cpu:0"):
    sum = tf.add_n(c)

sess = tf.Session(
    config=tf.ConfigProto(
        allow_soft_placement=True,
        log_device_placement=True
    )
)
sess.run(sum)