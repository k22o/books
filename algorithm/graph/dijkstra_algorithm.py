#-*- coding :utf-8 -*-
#ダイクストラ法

import numpy as np
import queue
import heapq

#グラフを作成および探索するためのクラス
class Graph:
    '''
    node_num ...ノード数
    node_matrix ...有効・無向グラフを記した表
    color ...探索の様子を示す
    　　　　　白…未訪問　灰色…訪問済み・未訪問隣接点あり　黒...完全終了
    pred ...1つ前の隣接点のストック
    '''
    
    def __init__(self,node_num):
        self.node_num = node_num
        self.node_matrix = np.zeros((node_num,node_num))
        self.color = np.ones((node_num))
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
        

def singleSourceShortest(graph,start):
    
    #priority queueの設定
    graph.dist[start] = 0
    pq = []
    heapq.heappush(pq,(graph.dist[start],start))

    #各ノードと初期距離をpqにいれる
    for i in range(graph.node_num):
        heapq.heappush(pq,(graph.dist[i],i))

    while len(pq) != 0  :#queueが空になるまで
        u  = heapq.heappop(pq)#最小を取り出す
        u = u[1]
        for v in range (graph.node_num):
            if graph.node_matrix[u][v] != 0:
                weight = graph.node_matrix[u][v]
                newlen = graph.dist[u] + weight
                if newlen < graph.dist[v]:
                    for j in range(len(pq)):
                        if pq[j][1] == v:
                            pq[j] = (newlen,v)
                            pq.sort()
                    #heapq.heappush(pq,(newlen,v))
                    graph.dist[v] = newlen
                    graph.pred[v] = u
    print(graph.dist)
    print(graph.pred)
        
if __name__ == "__main__":

    node_num = 6
    graph = Graph(node_num)
    
    graph.add_node(0,1,1,6)
    graph.add_node(0,2,1,8)
    graph.add_node(0,3,1,18)
    graph.add_node(1,4,1,11)
    graph.add_node(2,3,1,9)
    graph.add_node(4,5,1,3)
    graph.add_node(5,3,1,4)
    graph.add_node(5,2,1,7)
        
    singleSourceShortest(graph,0)#start地点(0)から探索開始
