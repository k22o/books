# CONTENTS

- convnet_mnist:基本的なCNN
- convet_cifar_bn:バッチ正規化を利用した分類
- cifar10_input:cifar10からランダムに24*24を取り出す

# REFERENCE
## 中間層の可視化
CNNの中間層がどうなっているかを表示するには、t-SNE(t-Distributed Stochastic Neighbor Rmbedding)というアルゴリズムを用いることで、二次元画像に変換することができる。<br>
Maaten, Laurens van der, and Geofferey Hinton "Visualizing Data using t-SNE",<br> 
Journal of Machine Learning Resarch (2008)

## ニューラルスタイル
受け取った写真を絵画風に変換する。
Gatys, A.Leon et al. "A Neural Algorithm of Artistic Style"<br>
arXiv Preprint arXiv (2015)

## 画像の前処理
- tf.image.per_image_standarization(iamge):正規化
- tf.image.random_flip_up_down(iamge,seed=None)

など