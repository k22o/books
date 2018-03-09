#-*- coding :utf-8 -*-
#深さ優先探索

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
    
    def __init__(self,node_num,node_matrix,color,pred):
        self.node_num = node_num
        self.node_matrix = node_matrix
        self.color = color
        self.pred = pred
        
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
            self.color[node] = 1
        elif state == "GRAY":
            self.color[node] = 2
        else:
            self.color[node] = 3
        

def dfs_init(node_num):

    node_matrix = np.zeros((node_num,node_num))
    color = np.ones((node_num))
    pred  = np.ones((node_num))*(-1)
    graph = Graph(node_num,node_matrix,color,pred)
 
    return graph


def dfsVisit(graph,node):
    graph.change_color(node,"GRAY")#nodeの色をGRAYに
    for i in range (graph.node_num):
        if graph.node_matrix[node][i] !=0:#隣接nodeに対して
            if graph.color[i] == 1:#未探索であれば
                graph.pred[i] = node
                print (graph.color)
                dfsVisit(graph,i)
                print (graph.color)
    
    graph.change_color(node,"BLACK")
    

if __name__ == "__main__":

    node_num = 9
    graph = dfs_init(node_num)
    
    graph.add_node(0,1,2)
    graph.add_node(0,4,2)
    graph.add_node(1,2,2)
    graph.add_node(2,6,2)
    graph.add_node(2,3,2)
    graph.add_node(3,4,2)
    graph.add_node(4,5,2)
    graph.add_node(7,8,2)

    dfsVisit(graph,0)#start地点から探索開始
