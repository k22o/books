# -*- coding:utf-8 -*-

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib.pyplot as plt

'''
当然、勾配降下法による最適解の探索では、極小値に陥って最適解が
得られない可能性がある。その対策として、
GoodFellowら(2014)は、以下の式を勾配降下法に取り入れた。
θ_α = α * θ_f + (1-α) * θ_i
θ_f:SGDによる解
θ_i:ランダムなパラメタベクトル

詳細は、次の論文を参照。
"Qualitatively characterizing neural network potimization problem"
arXiv preprint arXiv:1412.6544(2014)
'''

n_hidden_1 = 256
n_hidden_2 = 256


def layer(input, weight_shape, bias_shape):
    weight_init = tf.random_normal_initializer(stddev=(2.0/weight_shape[0])**0.5)
    bias_init = tf.constant_initializer(value=0)
    W = tf.get_variable("W", weight_shape, initializer=weight_init)
    b = tf.get_variable("b", bias_shape, initializer=bias_init)
    return tf.nn.relu(tf.matmul(input, W) + b)


def inference(x):
    with tf.variable_scope("hidden_1"):
        hidden_1 = layer(x, [784, n_hidden_1], [n_hidden_1])     
    with tf.variable_scope("hidden_2"):
        hidden_2 = layer(hidden_1, [n_hidden_1, n_hidden_2], [n_hidden_2])
    with tf.variable_scope("output"):
        output = layer(hidden_2, [n_hidden_2, 10], [10])
    return output


def loss(output, y):
    xentropy = tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y)    
    loss = tf.reduce_mean(xentropy)
    return loss


mnist = input_data.read_data_sets("data", one_hot=True)

x = tf.placeholder("float", [None, 784])
y = tf.placeholder("float", [None, 10])
sess = tf.Session()

#SGDによる解を見つける
with tf.variable_scope("mlp_model") as scope:
    output_opt = inference(x)
    cost_opt = loss(output_opt, y)
    saver = tf.train.Saver()
    scope.reuse_variables()
    var_list_opt = [
        "hidden_1/W", "hidden_1/b",
		"hidden_2/W", "hidden_2/b",
        "output/W", "output/b"
    ]
    var_list_opt = [tf.get_variable(v) for v in var_list_opt]
    saver.restore(sess, "frozen_mlp_checkpoint/model-checkpoint-550000")


#ランダムパラメータによる解を見つける
with tf.variable_scope("mlp_init") as scope:
    output_rand = inference(x)
    cost_rand = loss(output_rand, y)
    scope.reuse_variables()
    var_list_rand = [
        "hidden_1/W", "hidden_1/b",
        "hidden_2/W", "hidden_2/b",
        "output/W", "output/b"
    ]
    var_list_rand = [tf.get_variable(v) for v in var_list_rand]
    init_op = tf.variables_initializer(var_list_rand)
    sess.run(init_op)


#線形補完する
with tf.variable_scope("mlp_inter") as scope:
    alpha = tf.placeholder("float", [1, 1])
    beta = 1 - alpha
    h1_W_inter = var_list_opt[0] * beta + var_list_rand[0] * alpha
    h1_b_inter = var_list_opt[1] * beta + var_list_rand[1] * alpha
    h2_W_inter = var_list_opt[2] * beta + var_list_rand[2] * alpha
    h2_b_inter = var_list_opt[3] * beta + var_list_rand[3] * alpha
    o_W_inter = var_list_opt[4] * beta + var_list_rand[4] * alpha
    o_b_inter = var_list_opt[5] * beta + var_list_rand[5] * alpha
    h1_inter = tf.nn.relu(tf.matmul(x, h1_W_inter) + h1_b_inter)
    h2_inter = tf.nn.relu(tf.matmul(h1_inter, h2_W_inter) + h2_b_inter)
    o_inter = tf.nn.relu(tf.matmul(h2_inter, o_W_inter) + o_b_inter)
    cost_inter = loss(o_inter, y)
    tf.summary.scalar("cost", cost_inter)


#可視化
summary_writer = tf.summary.FileWriter("linear_interp_logs", graph_def=sess.graph_def)
summary_op = tf.summary.merge_all()
results = []
for a in np.arange(-2, 2, 0.1):
    feed_dict = {
        x: mnist.test.images,
        y: mnist.test.labels,
        alpha: [[a]],
    }
    cost, summary_str = sess.run([cost_inter, summary_op], feed_dict=feed_dict)
    summary_writer.add_summary(summary_str, (a + 2)/0.1)
    results.append(cost)

plt.plot(np.arange(-2, 2, 0.1), results, "ro")
plt.grid()
plt.ylabel("error")
plt.xlabel("alpha")
plt.show()
