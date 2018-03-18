# -*- coding :utf-8 -*-
#フォードファルカーソン法
import numpy as np
import queue

class Graph():

    def __init__(self,node_num):
        self.node_num = node_num
        self.capacity = np.zeros((node_num,node_num))#容量
        self.flow = np.zeros((node_num,node_num))#フロー
        self.previous = np.zeros((node_num))#経路の前情報
        self.visit = np.zeros((node_num))#途中で訪問した節点
        #訪問状態は、0:クリア 1:キューにある 2:訪問済み
        
    def add_way(self,a,b,w):
        self.capacity[a][b] = w
        self.capacity[b][a] = -w

        
#経路があるか探索する
def search(graph,source,sink):
 
    graph.visit = np.zeros((graph.node_num))#訪問記録の初期化
    Q = queue.Queue() #queueの初期化
    Q.put(source)

    graph.previous[source] = -1
    graph.visit[source] = 1

    while not Q.empty():
        u = Q.get()
        graph.visit[u] = 2#訪問済み状態にする

        #まだ流量を増やす余地があれば、その経路をpreviousに記載する
        for v in range(graph.node_num):
            if(graph.visit[v] ==0 and graph.capacity[u][v] > graph.flow[u][v]):
                Q.put(v)
                graph.visit[v] = 1
                graph.previous[v] = u
                
    return graph.visit[sink] != 0
    
    
#経路の操作をする    
def compute(graph,source,sink):
    maxFlow = 0 
    while search(graph,source,sink):
        maxFlow += processPath(graph,source,sink)
        
    return maxFlow    


#経路を探して増やす
def processPath(graph,source,sink):
    v = sink#ゴールのノード
    delta = 10000

    #増やせる最小の流量を探す
    while graph.previous[v] != -1: #ソースノードにたどり着くまで
        unit = graph.capacity[int(graph.previous[v])][v] - graph.flow[int(graph.previous[v])][v]
        if unit < delta:#もし流量を増やせるなら、unitを記録しておく
            delta = unit
        v = int(graph.previous[v])
        
    #増やせる分だけ、実際に増やす
    v = sink

    while (graph.previous[v] != -1):
        graph.flow[int(graph.previous[v])][v] += delta
        graph.flow[v][int(graph.previous[v])] -= delta
        v = int(graph.previous[v])
        
    return delta

        

if __name__=='__main__':

    node_num = 6
    graph = Graph(node_num)
    graph.add_way(0,1,3)
    graph.add_way(0,2,2)
    graph.add_way(1,3,2)
    graph.add_way(1,4,2)
    graph.add_way(2,3,2)
    graph.add_way(2,4,3)
    graph.add_way(3,5,3)
    graph.add_way(4,5,2)

    source = 0
    sink   = 5
    
    maxFlow = compute(graph,source,sink)
    print(graph.flow)
