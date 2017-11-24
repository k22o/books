# -*- coding: utf-8 -*-

import chainer
from chainer import Variable
#Linkクラス…重みやバイアスなどのパラメータを持つクラス。Functionクラスの関数使える
import chainer.links as L
#Functionクラス…フォワード・バックワードなどの計算に関するクラス
import chainer.functions as F
import numpy as np
import math
import cv2
from evaluate import Evaluator

#Chainクラス…ニューラルネットワークの各要素をつなぐためのクラス。Linkの子クラス
class Fire(chainer.Chain):
    def __init__(self, in_size, s1, e1, e3):
        super().__init__()
        with self.init_scope():
            '''
            convention2D(入力,出力,フィルタサイズ,stride=,pad=,)
            として、畳込み層における計算をしてくれるLinkクラスの関数。
            ChainクラスはLinkクラスの子クラスなので、関数を継承している。
            '''
            self.conv1=L.Convolution2D(in_size, s1, 1)
            self.conv2=L.Convolution2D(s1, e1, 1)
            self.conv3=L.Convolution2D(s1, e3, 3, pad=1)

    #callがあることで、関数のようにしてinstanceを動かせる
    #https://qiita.com/kyo-bad/items/439d8cc3a0424c45214a
    def __call__(self, x):
        #活性化関数ReLUは、Functionsクラスにある。
        #http://docs.chainer.org/en/stable/reference/generated/chainer.functions.elu.html
        h = F.elu(self.conv1(x))
        h_1 = self.conv2(h)
        h_3 = self.conv3(h)
        #axisにそって、鎖状につなぐ,functionsクラスの関数
        #http://docs.chainer.org/en/stable/reference/generated/chainer.functions.concat.html
        h_out = F.concat([h_1, h_3], axis=1)
        return F.elu(h_out)


#上のFireクラスで作ったものを積み重ねていく
class FCN(chainer.Chain):
    def __init__(self, n_class, in_ch):
        super().__init__()
        with self.init_scope():
            self.conv1=L.Convolution2D(in_ch, 96, 7, stride=2, pad=3)
            self.fire2=Fire(96, 16, 64, 64)
            self.fire3=Fire(128, 16, 64, 64)
            self.fire4=Fire(128, 16, 128, 128)
            self.fire5=Fire(256, 32, 128, 128)
            self.fire6=Fire(256, 48, 192, 192)
            self.fire7=Fire(384, 48, 192, 192)
            self.fire8=Fire(384, 64, 256, 256)
            self.fire9=Fire(512, 64, 256, 256)

            self.score_pool1=L.Convolution2D(96, n_class, 1, stride=1, pad=0)
            self.score_pool4=L.Convolution2D(256, n_class, 1, stride=1, pad=0)
            self.score_pool9=L.Convolution2D(512, n_class, 1, stride=1, pad=0)

            self.add_layer=L.Convolution2D(n_class*3, n_class, 1, stride=1, pad=0)

            # デコンボリューション(解像度上げを行う)
            self.upsample_pool4=L.Deconvolution2D(n_class, n_class, ksize= 4, stride=2, pad=1)
            self.upsample_pool9=L.Deconvolution2D(n_class, n_class, ksize= 8, stride=4, pad=2)
            self.upsample_final=L.Deconvolution2D(n_class, n_class, ksize=16, stride=4, pad=(6,6))

        self.n_class = n_class
        self.active_learn = False
        self.evaluator = Evaluator(False, n_class)

    def clear(self):
        self.loss = None
        self.accuracy = None

    def __call__(self, x, t):
        h = F.elu(self.conv1(x))
        h = F.max_pooling_2d(h, 3, stride=2)
        p1 = self.score_pool1(h)

        h = self.fire2(h)
        h = self.fire3(h)
        h = self.fire4(h)
        h = F.max_pooling_2d(h, 3, stride=2)
        u4 = self.upsample_pool4(self.score_pool4(h))

        h = self.fire5(h)
        h = self.fire6(h)
        h = self.fire7(h)
        h = self.fire8(h)

        #マックスプーリングに関する操作　(入力,プーリングフィルタのサイズ,stride=,pad=)
        #http://docs.chainer.org/en/stable/reference/generated/chainer.functions.max_pooling_2d.html
        h = F.max_pooling_2d(h, 3, stride=2)
        h = self.fire9(h)
        u9 = self.upsample_pool9(self.score_pool9(h))

        h = F.concat((p1, u4, u9), axis=1)
        h = self.add_layer(h)
        h = self.upsample_final(h)

        self.h = h
        #ソフトマックス関数と交差エントロピーによる損失関数の定義
        #http://docs.chainer.org/en/stable/reference/generated/chainer.functions.softmax_cross_entropy.html?highlight=softmax_cross_entropy
        self.loss = F.softmax_cross_entropy(h, t)

        self.evaluator.preparation(h, t)
        self.accuracy = self.evaluator.get_accuracy()
        self.iou = self.evaluator.get_iou()

return self.loss
