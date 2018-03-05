#-*- coding: utf-8 -*-
import numpy as np
#本来ループの計算にnumpyは向かない
#python のコンテナ型を使えばもっと容易になる？？


#文字列の場合の計算
def hashcode(word):
    length = len(word)
    h = 0
    for i in range(length):
        h = 31 * h + ord(word[i]);
    return h

#ハッシュの計算方法
def hash_calc(value,key):
    return value % key

    

#ハッシュテーブルを作成
#key...割り算の値
#size...ハッシュテーブルのサイズ
def hash_store(arrayD,key,size):
    arrayH = np.zeros((2,size))
    array = [0 for i in range(len(arrayD))]

    for x in range(len(arrayD)):

        #文字列のとき
        array[x] =  hashcode(arrayD[x])
        #数字のとき
        #array = arrayD

        k = hash_calc(array[x], key)
        while(arrayH[0,k] != 0):
            k = hash_calc(k+1,key)
        arrayH[0,k] = array[x]
        arrayH[1,k] = x
        
    return (arrayH)


#探索する
def hash_search(array,target,key):
    k = target % key
    while(array[0,k] != 0):
        if(array[0,k] == target):
            return (array[1,k])
        else:
            k = (k+1) % key
    return (None)
        

if __name__ == '__main__':

    target = hashcode("apple")
    key = 11
    size = 15
    #arrayD = np.array([12,25,36,20,30,8,42])
    arrayD = ["apple","banana","peach","melon","strawberry"]
    
    hash_array = hash_store(arrayD,key,size)
    print (hash_array)
    ans = hash_search(hash_array, target, key)
    
    print ("元のリストの {} 番目に存在する".format(ans+1))
