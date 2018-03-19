#-*- coding: utf-8 -*-

class Item:
    #コンストラクタ
    def __init__(self,value,weight):
        self.value = value
        self.weight = weight

class ApproximateItem(Item):
    def __init__(self,item,idx):
        Item.__init__(self,item.value,item.weight)
        self.normalizedValue = item.value/item.weight
        self.index = idx
        

#動的計画法による
def knapsack_01(items,W):
    n = len(items)
    m = [None] *(n+1)
    for i in range(n+1):
        m[i] = [0] *(W+1)
    for i in range(1,n+1):
        for j in range(W+1):
            if items[i-1].weight <= j:
                m[i][j] = max(m[i-1][j],m[i-1][j-items[i-1].weight]+items[i-1].value)
            else:
                m[i][j] = m[i-1][j]
    selections = [0] * n
    i = n
    w = W
    while i>0 and w>=0:
        if m[i][w] != m[i-1][w]:
            selections[i-1] = 1
            w -= items[i-1].weight
        i -=1
    return (m[n][W],selections)

#無制限ナップサック問題
def knapsack_unbounded(items,W):
    
    n = len(items)
    progress = [0] *(W+1)
    progress[0] = -1
    m = [0] *(W+1)
    for j in range(1,W+1):
        progress[j] = progress[j-1]
        best = m[j-1]
        for i in range(n):
            remaining = j -items[i].weight
            if remaining >=0 and m[remaining] + items[i].value > best:
                best = m[remaining] + items[i].value
                progress[j] = i
            m[j] = best
    selections = [0] * n
    i=n
    w=W
    while w>=0:
        choice = progress[w]
        if choice == -1:
            break
        selections[choice] +=1
        w -= items[progress[w]].weight
    return (m[W],selections)

#無制限ナップサック近似
def knapsack_approximate(items,W):
    approxItems = []
    n = len(items)
    for idx in range(n):
        approxItems.append(ApproximateItem(items[idx],idx))
    approxItems.sort(key= lambda x:x.normalizedValue, reverse=True)

    selections = [0] * n
    w = W
    total = 0
    for idx in range(n):
        item = approxItems[idx]
        if w == 0:
            break
        numAdd = w // item.weight
        if numAdd>0:
            selections[item.index] += numAdd
            w -= numAdd * item.weight
            total += numAdd *item.value
    return (total,selections)



if __name__ == '__main__':

    items = [None] * 4
    items[0] = Item(4,3)
    items[1] = Item(2,1)
    items[2] = Item(4,2)
    items[3] = Item(5,3)
    
    print("動的計画法によるナップサック問題...各商品は1回のみ使用可")
    ans,selections = knapsack_01(items,4)
    print("ans:{} selections:{}".format(ans,selections))

    print("無制限ナップサック問題...同一商品の複数選択可能")
    ans,selections = knapsack_unbounded(items,4)
    print("ans:{} selections:{}".format(ans,selections))

    print("無制限ナップサック近似")
    ans,selections = knapsack_approximate(items,4)
    print("ans:{} selections:{}".format(ans,selections))


    
    
