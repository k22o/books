#-*- coding :utf-8 -*-
#ダイクストラ法

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
    def __init__(self,node_num,node_matrix,color,pred,dist):
        self.node_num = node_num
        self.node_matrix = node_matrix
        self.color = color
        self.pred = pred
        self.dist = dist
        
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
        

def sss_init(node_num):

    node_matrix = np.zeros((node_num,node_num))
    color = np.ones((node_num))
    pred  = np.ones((node_num))*(-1)
    dist = np.ones((node_num))*1000
    graph = Graph(node_num,node_matrix,color,pred,dist)
    
    return graph


def singleSourceShortest(graph,start):

    graph.dist[start] = 0
    for k in range(graph.node_num):
        for i in range(graph.node_num):
            for j in range(graph.node_num): 
                if graph.node_matrix[i][j] != 0:
                    newlen = graph.dist[i] + graph.node_matrix[i][j]
                    if newlen < graph.dist[j] and k== graph.node_num-1:
                        graph.dist[j] = newlen
                        graph.pred[j] = i
                        print("{} {}".format(graph.dist[j],graph.dist[j]))
                        
        
if __name__ == "__main__":

    node_num = 6
    graph = sss_init(node_num)
    
    graph.add_node(0,1,1,6)
    graph.add_node(0,2,1,8)
    graph.add_node(0,3,1,18)
    graph.add_node(1,4,1,11)
    graph.add_node(2,3,1,9)
    graph.add_node(4,5,1,3)
    graph.add_node(5,3,1,4)
    graph.add_node(5,2,1,7)
       
    singleSourceShortest(graph,0)#start地点(0)から探索開始
