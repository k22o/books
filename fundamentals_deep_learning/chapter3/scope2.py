# -*- coding:utf-8 -*-
import tensorflow as tf

'''
get_variable(<name> <shape> <initializer>)
指定された名前のvariableが存在するか確認する。
存在しなければ、指定されtた形で新規作成する。
variable_scope(<scope name>)
名前空間を管理し、get_variableの有効範囲を判断する
'''

def layer(input, weight_shape, bias_shape):
    weight_init = tf.random_uniform_initializer(minval=-1, maxval=1)
    bias_init = tf.constant_initializer(value=0)
    W = tf.get_variable("W", weight_shape, initializer=weight_init)
    b = tf.get_variable("b", bias_shape, initializer=bias_init)
    return tf.matmul(input, W) + b


def my_network(input):
    with tf.variable_scope("layer_1"):
        output_1 = layer(input, [784, 100], [100])

    with tf.variable_scope("layer_2"):
        output_2 = layer(output_1, [100, 50], [50])

    with tf.variable_scope("layer_3"):
        output_3 = layer(output_2, [50, 10], [10])

    return output_3

#実行タイプ１
#i_2の実行時にすでにvariableが存在するためエラーを起こす
i_1 = tf.placeholder(tf.float32, [1000, 784], name="i_1")
my_network(i_1)

i_2 = tf.placeholder(tf.float32, [1000, 784], name="i_2")
# my_network(i_2)
# ValueError: Over-sharing: Variable layer_1/W already exists...


#実行タイプ2
#reuse_variableによって、存在しているvariableの名前を変えて実行できる
with tf.variable_scope("shared_variables") as scope:
    i_1 = tf.placeholder(tf.float32, [1000, 784], name="i_1")
    my_network(i_1)
    scope.reuse_variables()
    i_2 = tf.placeholder(tf.float32, [1000, 784], name="i_2")
    my_network(i_2)
