#-*- coding :utf-8 -*-
#プリム法

import numpy as np
import queue
import heapq

#グラフを作成および探索するためのクラス
class Graph:
    '''
    node_num ...ノード数
    node_matrix ...有効・無向グラフを記した表
    pred ...1つ前の隣接点のストック
    '''
    
    def __init__(self,node_num):
        self.node_num = node_num
        self.node_matrix = np.zeros((node_num,node_num))
        self.pred  = np.ones((node_num))*(-1)
        self.dist = np.ones((node_num))*1000
    
        
    def add_node(self,a,b,direction=1,w=1):
        '''
        a,b ... ノードaからノードbへのグラフ
        direction ... 有向グラフ(1)か無向グラフ(2)か
        w ... グラフの重み
        '''
        self.node_matrix[a][b] = w    
        if direction == 2:
            self.node_matrix[b][a] = w

    def change_color(self,node,state):
        if state == "WHITE" :
            self.color[int(node)] = 1
        elif state == "GRAY":
            self.color[int(node)] = 2
        else:
            self.color[int(node)] = 3
        

def prim(graph):
    
    #priority queueの設定
    graph.dist[0] = 0 
    pq = []

    #各ノードと初期距離をpqにいれる
    for i in range(graph.node_num):
        heapq.heappush(pq,(graph.dist[i],i))

    while len(pq) != 0  :#queueが空になるまで
        u  = heapq.heappop(pq)[1]#最小を取り出す(タプルの0番目をもとにソート)
        for v in range (graph.node_num):
            #もしuv間に道があって、まだvがキューの中にあったら
            if graph.node_matrix[u][v] != 0:
                for i in range(len(pq)):
                    if pq[i][1] == v:
                        weight = graph.node_matrix[u][v]
                        if weight < graph.dist[v] :
                            graph.dist[v] = weight
                            graph.pred[v] = u

                            #最短距離を更新する
                            for j in range(len(pq)):
                                if pq[j][1] == v:
                                    pq[j] = (weight,v)
                                    pq.sort()

    print("dist:{}".format(graph.dist))
    print("pred:{}".format(graph.pred))
        
if __name__ == "__main__":

    node_num = 5
    graph = Graph(node_num)
    
    graph.add_node(0,1,2,2)
    graph.add_node(1,2,2,3)
    graph.add_node(0,3,2,8)
    graph.add_node(0,4,2,4)
    graph.add_node(2,3,2,5)
    graph.add_node(3,4,2,7)
    graph.add_node(2,4,2,1)
    
    prim(graph)
