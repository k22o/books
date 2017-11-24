#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, os
import settings  # 設定の読み込み
from mini_batch_loader import DatasetPreProcessor
from fcn_squeeze_dilate import FCN

import chainer
import chainer.functions as F
from chainer import serializers
#optimizersクラス…最適化に関するクラス
#http://docs.chainer.org/en/stable/reference/core/generated/chainer.Optimizer.html#chainer.Optimizer
#cuda クラス…Device, context and memory management
#http://docs.chainer.org/en/stable/reference/util/cuda.html
from chainer import cuda, optimizers, Variable

import numpy as np
np.random.seed(555)
from skimage import io
import math


def prepare_dataset():
    # データセットのロード
    train_mini_batch_loader = \
        DatasetPreProcessor(chainer.global_config.user_train_args)
    train_it = chainer.iterators.SerialIterator(
                train_mini_batch_loader,
                chainer.global_config.user_train_args.training_params.batch_size)
    return train_mini_batch_loader, train_mini_batch_loader.__len__()


def main():
    # データセットのロード
    train_mini_batch_loader, train_data_size = prepare_dataset()
    # モデルのロード
    model = FCN(chainer.global_config.user_train_args.n_class,
                chainer.global_config.user_train_args.in_ch)

    # オプティマイザーの定義
    #Adam(Adaptive moment estimation) …AdaGradやRMSProp,AdaDeltaを改良したもの。
    #https://qiita.com/tokkuman/items/1944c00415d129ca0ee9
    optimizer = chainer.optimizers.Adam()
    #Sets a target link and initializes the optimizer states.
    optimizer.setup(model)

    #add_hockによる正則化手法
    optimizer.add_hook(
        chainer.optimizer.WeightDecay(
            chainer.global_config.user_train_args.training_params.weight_decay))

    # training
    for epoch in range(1, 100):
        print("epoch %d" % epoch)
        sum_accuracy = 0
        sum_loss     = 0
        sum_iou      = np.zeros(chainer.global_config.user_train_args.n_class)

        all_indices = np.random.permutation(train_data_size)
        batch_size = chainer.global_config.user_train_args.training_params.batch_size
        for i in range(0, train_data_size, batch_size):
            batch_indices = all_indices[i:i+batch_size]
            raw_x, raw_t = train_mini_batch_loader.load_data(batch_indices)
            x = chainer.Variable(raw_x)
            t = chainer.Variable(raw_t)

            model.zerograds()
            #ロスの計算
            loss = model(x, t)
            #ロスの勾配計算
            loss.backward()
            #パラメータ更新
            optimizer.update()

            if math.isnan(loss.data):
                raise RuntimeError("ERROR in main: loss.data is nan!")

            sum_loss += loss.data * batch_size
            sum_accuracy += model.accuracy * batch_size
            sum_iou += np.array(model.iou) * batch_size

        print("train mean loss {}, accuracy {}, IoU {}" \
                .format(sum_loss/train_data_size, sum_accuracy/train_data_size,
                        sum_iou/train_data_size))

        # モデルの保存
        snapshot_epochs = \
            chainer.global_config.user_train_args.training_params.snapshot_epochs
        if epoch % snapshot_epochs == 0:
            stor_dir = os.path.dirname(
                chainer.global_config.user_train_args.model_path.format(epoch))
            if not os.path.exists(stor_dir):
                os.makedirs(stor_dir)
            serializers.save_npz(
                chainer.global_config.user_train_args.model_path.format(epoch),
                model)

    # モデルの保存
    serializers.save_npz(
        chainer.global_config.user_train_args.model_path.format("final"), model)


if __name__ == '__main__':
    chainer.global_config.train = chainer.global_config.user_train_args.train
    start = time.time()
    main()
    end = time.time()
print("{}[m]".format((end - start)/60))
