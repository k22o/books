#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pandas as pd
import numpy as np
#os.systemなどの代わり
#https://docs.python.jp/3/library/subprocess.html
import subprocess
from skimage import graph, data, io, segmentation, color
from matplotlib import pyplot as plt


data_root_dir = './data'
label_table_name = 'label_color'
image_dir = 'CamSeq01'
image_dir_path = os.path.join(data_root_dir, image_dir)

#csvファイルの読み込み
label_table = pd.read_csv(os.path.join(data_root_dir, label_table_name))
cmd = 'ls {}|grep _L.png'.format(os.path.join(data_root_dir, image_dir))
'''
subprocess.Popen : 新しいプロセスで子のプログラムを実行する
args:実行すべきプログラムのパスまたは名前
shell:実行するプログラムでシェルを使うかどうか
stdout:標準出力
stderr:標準エラー出力
((.PIPEはそのようなものだと理解))

process.communicate()で、上記で指定した出力などを指定
'''
process = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
b_stdout_data, stderr_data = process.communicate()
stdout_data = b_stdout_data.decode('utf-8')


for image_file_name in stdout_data.rstrip().split('\n'):
    file_path = os.path.join(image_dir_path, image_file_name)
    print('processing {}'.format(file_path))
    img = io.imread(file_path)

    class_map = np.empty((img.shape[0], img.shape[1]), dtype='i')
    for i_row in range(len(label_table)):
        class_color = label_table.iloc[i_row]
        idx = np.where((img[:,:,0]==class_color[0])  # r
                        & (img[:,:,1]==class_color[1])  # g
                        & (img[:,:,2]==class_color[2]))  # b
        class_map[idx] = i_row
    label_file_name = os.path.join(image_dir_path,
                                    os.path.splitext(image_file_name)[0]+'.npz')
np.savez(label_file_name, data=class_map)
