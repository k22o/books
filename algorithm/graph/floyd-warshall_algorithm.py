#-*- coding :utf-8 -*-
#フロイド-ワーシャル法

import numpy as np

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
        self.pred  = np.ones((node_num,node_num))*(-1)
        self.dist = np.ones((node_num,node_num))*1000
        self.path_list = np.array([])

        
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
        

#実装
def allPairsShortestPath(graph):

    way = []
    
    for i in range(graph.node_num):
        graph.dist[i][i] = 0

    for i in range(graph.node_num):
        for j in range(graph.node_num):
            if graph.node_matrix[i][j] != 0:
                graph.dist[i][j] = graph.node_matrix[i][j]
                graph.pred[i][j] = i

    for k in range(graph.node_num):
        for i in range(graph.node_num):
            for j in range(graph.node_num):
                newlen = graph.dist[i][k] + graph.dist[k][j]
                if newlen < graph.dist[i][j]:
                    graph.dist[i][j] = newlen
                    graph.pred[i][j] = graph.pred[k][j]
                    print (graph.dist)
                    print (graph.pred)

                    
                    
if __name__ == "__main__":

    node_num = 5
    graph = Graph(node_num)
    
    graph.add_node(0,1,1,2)
    graph.add_node(1,2,1,3)
    graph.add_node(0,4,1,4)
    graph.add_node(2,4,1,1)
    graph.add_node(4,3,1,7)
    graph.add_node(2,3,1,5)
    graph.add_node(3,0,1,8)
    
    allPairsShortestPath(graph)
