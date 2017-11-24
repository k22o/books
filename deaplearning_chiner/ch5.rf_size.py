# -*- coding: utf-8 -*-
import numpy as np

# [filter size, stride, padding]で層を表し、listに格納
# 最外リストのintex = 0が最初の畳み込み層
convnet =[[3,1,1], [3,1,1], [2,2,0],
          [3,1,1], [3,1,1], [2,2,0],
          [3,1,1], [3,1,1], [3,1,1], [2,2,0],
          [3,1,1], [3,1,1], [3,1,1], [2,2,0],
          [3,1,1], [3,1,1], [3,1,1], [2,2,0],
          [7,1,3], [1,1,0],]


# 出力用に層の名前を定義
# printの際に使用
#c,c*-convは畳み込み層、pはプーリング層
layer_name = ['c1_1', 'c1_2','p1',
              'c2_1', 'c2_2','p2',
              'c3_1', 'c3_2', 'c3_3', 'p3',
              'c4_1', 'c4_2', 'c4_3', 'p4',
              'c5_1', 'c5_2', 'c5_3', 'p5',
'fc6-conv', 'fc7-conv',]

#受容野の計算を行う関数
def in_from_out(layernum=9,net=convnet):
    if layernum>len(net):
        layernum = len(net)

    outsize = 1
    for layer in reversed(range(layernum)):
        ksize,stride,pad = net[layer]
        #ネットワーク内の出力サイズ(outsize*outsize)
        outsize = ((outsize-1)* stride) + ksize
    #入力層まで遡って計算した受容野
    rf_size = outsize
    return rf_size

#入力に対するoutputサイズとストライドサイズの累積値計算
def out_from_in(isz,layernum = 9, net= convnet):
        if layernum > len(net) :
            layernum=len(net)
        totstride = 1
        insize = isz
        for layer in range(layernum):
            fsize, stride ,pad = net[layer]
            outsize = (insize - fsize + 2*pad) /stride + 1
            insize = outsize
            totstride = totstride * stride
        return outsize, totstride

if __name__  == '__main__':
    imsize = 512
    print ("layer output sizes given image = %dx%d" %(imsize,imsize))
    for i in range (len(convnet)) :
        #層の出力サイズとストライドの累積値計算
        p = out_from_in(imsize,i+1)
        #層の出力時の受容野の計算
        rf = in_from_out(i+1)
        print("layer Name = %s ,Output size = %d, Stride = %d, RF size = %d"%(layer_name[i],p[0],p[1],rf))
