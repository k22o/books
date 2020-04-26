# -*- coding:utf-8 -*-

from sklearn import decomposition
from matplotlib import pyplot as plt
from fdl_examples.datatools import input_data


mnist = input_data.read_data_sets("data/", one_hot=False)
#PCAの設定
pca = decomposition.PCA(n_components=2)
#PCAを実行して主成分などを計算
pca.fit(mnist.train.images)
#PCAの結果を利用して、主成分にデータを投射する
pca_codes = pca.transform(mnist.test.images)
#投射したものをもとに戻す
pca_recon = pca.inverse_transform(pca_codes[:1])
plt.imshow(pca_recon[0].reshape((28,28)), cmap=plt.cm.gray)
plt.show()