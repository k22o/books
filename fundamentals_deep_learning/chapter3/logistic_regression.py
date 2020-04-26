# -*- coding:utf-8 -*-
import tensorflow as tf
import time, shutil, os
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("data", one_hot=True)

# Parameters
learning_rate = 0.01
training_epochs = 100
batch_size = 100
display_step = 1

# 与えられたミニバッチに対して出力クラスの確率分布を生成する
def inference(x):
    init = tf.constant_initializer(value=0)
    W = tf.get_variable("W", [784, 10], initializer=init)
    b = tf.get_variable("b", [10], initializer=init)
    output = tf.nn.softmax(tf.matmul(x, W) + b)
    tf.summary.histogram("weights", W)
    tf.summary.histogram("biases", b)
    tf.summary.histogram("output", output)
    return output


# loss-functionを計算(今回はcross-entropy)
def loss(output, y):
    dot_product = y * tf.log(output)
    # Reduction along axis 0 collapses each column into a single
    # value, whereas reduction along axis 1 collapses each row 
    # into a single value. In general, reduction along axis i 
    # collapses the ith dimension of a tensor to size 1.
    xentropy = -tf.reduce_sum(dot_product, axis=1)
    loss = tf.reduce_mean(xentropy)
    return loss


#訓練
def training(cost, global_step):
    tf.summary.scalar("cost", cost)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_op = optimizer.minimize(cost, global_step=global_step)
    return train_op


#テスト
def evaluate(output, y):
    correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar("validation error", (1.0 - accuracy))
    return accuracy


if __name__ == "__main__":
    # Remove old summaries and checkpoints
    # ログを生成するための準備(tf.summaryの部分がlogに記録される)
    if os.path.exists("logistic_logs"):
        shutil.rmtree("logistic_logs")

    with tf.Graph().as_default():
        x = tf.placeholder("float", [None, 784]) # mnist data image of shape 28*28=784
        y = tf.placeholder("float", [None, 10]) # 0-9 digits recognition => 10 classes
        output = inference(x)
        cost = loss(output, y)
        global_step = tf.Variable(0, name="global_step", trainable=False)
        train_op = training(cost, global_step)
        eval_op = evaluate(output, y)
        summary_op = tf.summary.merge_all()#すべてのsummaryする値を集める
        saver = tf.train.Saver()#モデルのパラメタを保存する
        sess = tf.Session()
        summary_writer = tf.summary.FileWriter(
            "logistic_logs",
            graph_def=sess.graph_def
        )#merge_allしたデータを保存する
        
        #初期化
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(mnist.train.num_examples/batch_size)
            # Loop over all batches
            for i in range(total_batch):
                minibatch_x, minibatch_y = mnist.train.next_batch(batch_size)
                # Fit training using batch data
                sess.run(train_op, feed_dict={x: minibatch_x, y: minibatch_y})
                # Compute average loss
                avg_cost += sess.run(
                    cost, feed_dict={x: minibatch_x, y: minibatch_y}
                ) / total_batch
            # Display logs per epoch step
            if epoch % display_step == 0:
                print("Epoch: {:04d} cost: {:.9f}".format(epoch+1, avg_cost))
                accuracy = sess.run(eval_op, feed_dict={x: mnist.validation.images, y: mnist.validation.labels})
                print("Validation Error: {}".format(1 - accuracy))
                summary_str = sess.run(summary_op, feed_dict={x: minibatch_x, y: minibatch_y})
                summary_writer.add_summary(summary_str, sess.run(global_step))
                saver.save(sess, os.path.join("logistic_logs", "model-checkpoint"), global_step=global_step)

        print("Optimization Finished!")
        accuracy = sess.run(eval_op, feed_dict={x: mnist.test.images, y: mnist.test.labels})
        print("Test Accuracy: {}".format(accuracy))
