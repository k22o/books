#-*- coding: utf-8 -*-

class BinaryNode:
    def __init__(self,value=None):
        #二分節点をつくる
        self.value = value
        self.left = None
        self.right = None
        self.height = 0

    def computeHeight(self):
        #BSTの節点の高さを子から計算
        height = -1
        if self.left:
            height = max(height,self.left.height)
        if self.right:
            height = max(height,self.right.height)
        self.height = height + 1

    def heightDifference(self):
        #BSTの左右の高低差を計算する
        leftTarget = 0
        rightTarget = 0
        if self.left:
            leftTarget = 1 + self.left.height
        if self.right:
            rightTarget = 1 + self.right.heigt
        return leftTarget - rightTarget
        
    def add(self,val):
        #新しい数をBSTに追加
        newRoot = self
        if val <= self.value:
            self.left = self.addToSubTree(self.left,val)
            if self.heightDifference() == 2:
                if val <= self.left.value:
                    newRoot = self.rotateRight()
                else:
                    newRoot = self.rotateRight()
        else :
              self.right = self.addToSubTree(self.right,val)
              if self.heightDifference() == -2:
                if val > self.right.value:
                    newRoot = self.rotateleft()
                else:
                    newRoot = self.rotateLeft()

        newRoot.computeHeight()
        return newRoot

    def addToSubTree(self,parent,val):
        #親の部分木にvalを追加し、回転の際には根を返す
        if parent is None :
            return BinaryNode(val)

        parent = parent.add(val)
        return parent
                
    def rotateRight(self):
        newRoot = self.left
        grandson = newRoot.right
        self.left = grandson
        newRoot.right = self

        self.computeHeight()
        return newRoot

    def rotateRightLeft(self):
        child = self.right
        newRoot = child.left
        grand1 = newRoot.left
        grand2 = newRoot.right
        child.left = grand2
        self.right = grand1

        newRoot.left = self
        newRoot.right = child

        child.computeHeight()
        self.computeHeight()
        return newRoot
        
    def rotateleft(self):
        newRoot = self.right
        grandson = newRoot.left
        self.right = grandson
        newRoot.left = self

        self.computeHeight()
        return newRoot

    def rotateLeftRight(self):
        child = self.left
        newRoot = child.right
        grand1 = newRoot.right
        grand2 = newRoot.left
        child.right = grand2
        self.left = grand1

        newRoot.right = self
        newRoot.left = child

        child.computeHeight()
        self.computeHeight()
        return newRoot

    def removeFromParent(self,parent,val):
        if parent:
            return parent.remove(val)
        return None

    def remove(self,val):
        newRoot = self
        if val == self:
            if self.left is None:
                return self.right
            
            child = self.left
            while child.right:
                child = child.right

            childkey = child.value
            self.left = self.removeFromParent(self.left,childkey)
            self.value = childkey

            if self.heightDiffenrence() == -2:
                if self.right.heightDifference <= 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()

        elif val < self.value:
            self.left = self.removeFromParent(self.left,val)
            if self.heightDiffenrence() == -2:
                if self.right.heightDifference <= 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()

        else:
            self.right = self.removeFromParent(self.right,val)
            if self.heightDiffenrence() == 2:
                if self.left.heightDifference >= 0:
                    newRoot = self.rotateRight()
                else:
                    newRoot = self.rotateLeftRight()

    def inorder(self):
        if self.left:
            for n in self.left.inorder():
                yield n

        yield self.value

        if self.right:
            for n in self.right.inorder():
                yield n
                    
class BinaryTree:
    def __init__(self):
        #からのBSTをつくる
        self.root = None

    def __iter__(self):
        #木の要素を間順走査
        if self.root:
            return self.root.inorder()
        
    def add (self,value):
        if self.root is None:
            self.root = BinaryNode(value)
        else :
            self.root.add(value)

    def __contain__(self,target):
        node = self.root
        while node:
            if target < node.value:
                node = node.left
            elif target > node.value:
                node = node.right
            else:
                return True
        return False



    
if __name__ == "__main__":
        
    bt = BinaryTree()
    for i in range(10,0,-1):
        print(i)
        bt.add(i)
    for v in bt:
        print (v)
    
