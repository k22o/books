#-*- coding :utf-8 -*-
#幅優先探索

import numpy as np
import queue

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
        

def bfs_init(node_num):

    node_matrix = np.zeros((node_num,node_num))
    color = np.ones((node_num))
    pred  = np.ones((node_num))*(-1)
    dist = np.ones((node_num))*1000
    graph = Graph(node_num,node_matrix,color,pred,dist)
    
    return graph


def bfs(graph,start):

    #startの初期設定
    graph.change_color(start,"GRAY")
    graph.dist[start] = 0

    #queueの設定
    Q = queue.Queue()#queueの初期化
    Q.put(start)#startをqueueに入れる(enqueue)
    
    while not Q.empty():#queueが空になるまで

        u = Q.get()#queueの先頭(First In)を取得(dequeue)
        
        for i in range(graph.node_num):
            #道があって未訪問だったら
            if graph.node_matrix[u][i] != 0 and graph.color[i] == 1:
                graph.dist[i] = graph.dist[u] + graph.node_matrix[u][i]
                graph.pred[i] = u
                graph.change_color(i,"GRAY")
                Q.put(i)
        graph.change_color(u,"BLACK")
        print(graph.color)

        
if __name__ == "__main__":

    node_num = 9
    graph = bfs_init(node_num)
    
    graph.add_node(0,1,2)
    graph.add_node(0,4,2)
    graph.add_node(1,2,2)
    graph.add_node(2,6,2)
    graph.add_node(2,3,2)
    graph.add_node(3,4,2)
    graph.add_node(4,5,2)
    graph.add_node(7,8,2)
    
    print (graph.color)
    
    bfs(graph,0)#start地点(0)から探索開始
