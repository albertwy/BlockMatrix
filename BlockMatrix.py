# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 23:49:11 2016

@author: Albert
"""

import numpy as np
import gc


class BlockMatrix():
    
    def __init__(self, name, exist = 0, rows = 0, cols = 0):
        assert rows % 2 == 0
        assert cols % 2 == 0
        
        self.rows = rows
        self.cols = cols
        self.name = name
        self.shape = (self.rows,self.cols)
        self.A_name = name + "A" + ".npy"
        self.B_name = name + "B" + ".npy"
        self.C_name = name + "C" + ".npy"
        self.D_name = name + "D" + ".npy"
        self.dic = {True:{},False:{}}
        self.dic[True][True] = self.B_name
        self.dic[True][False] = self.D_name
        self.dic[False][True] = self.A_name
        self.dic[False][False] = self.C_name
        
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        
        if exist == 0:
            block = np.ones((self.rows/2,self.cols/2), dtype = "float16")
            np.save(self.A_name, block)
            np.save(self.B_name, block)
            np.save(self.C_name, block)
            np.save(self.D_name, block)
            del block
            gc.collect()
            
        
       
     
    def setValues(self, row_lis, col_lis, value_lis):
        assert len(row_lis) == len(col_lis) == len(value_lis)
        length = len(row_lis)
        block_dic = {self.A_name:[],self.B_name:[],
                     self.C_name:[],self.D_name:[]                     
                     }
        
        for i in xrange(length):
            block_dic[self.dic[row_lis[i]>=self.rows/2][col_lis[i]>=self.cols/2]].append(i)
        for i in block_dic.keys():
            block = np.load(i)
            for j in block_dic[i]:
                block[row_lis[j] % (self.rows/2),col_lis[j] % (self.cols/2)] = value_lis[j]
            np.save(i, block)
            del block
            gc.collect()
        
    
    
    def getValues(self, row_lis, col_lis):
        assert len(row_lis) == len(col_lis)
     
        length = len(row_lis)
        values = [0 for i in xrange(length)]
        block_dic = {self.A_name:[],self.B_name:[],
                     self.C_name:[],self.D_name:[]                     
                     }
        
        for i in xrange(length):
            block_dic[self.dic[row_lis[i]>=self.rows/2][col_lis[i]>=self.cols/2]].append(i)
            
        for i in block_dic.keys():
            block = np.load(i)
            for j in block_dic[i]:
                values[j] = block[row_lis[j] % (self.rows/2),col_lis[j] % (self.cols/2)] 
            del block
            gc.collect()
        return values
       
    def __add__(self, otherMatrix):
        assert self.rows == otherMatrix.rows
        assert self.cols == otherMatrix.cols
        assert self.name != otherMatrix.name
        name = self.name + "a" + otherMatrix.name
        
        A1 = np.load(self.A_name)
        A2 = np.load(otherMatrix.A_name)
        np.save(name+"A.npy",A1 + A2)
        del A1
        del A2
        gc.collect()
        
        B1 = np.load(self.B_name)
        B2 = np.load(otherMatrix.B_name)
        np.save(name+"B.npy",B1 + B2)
        del B1
        del B2
        gc.collect()
        
        C1 = np.load(self.C_name)
        C2 = np.load(otherMatrix.C_name)
        np.save(name+"C.npy",C1 + C2)
        del C1
        del C2
        gc.collect()
        
        D1 = np.load(self.D_name)
        D2 = np.load(otherMatrix.D_name)
        np.save(name+"D.npy",D1 + D2)
        del D1
        del D2
        gc.collect()
        
        return BlockMatrix(name, 1, self.rows, self.cols)
      
    def __sub__(self, otherMatrix):
        assert self.rows == otherMatrix.rows
        assert self.cols == otherMatrix.cols
        assert self.name != otherMatrix.name
        name = self.name + "s" +otherMatrix.name
        
        A1 = np.load(self.A_name)
        A2 = np.load(otherMatrix.A_name)
        np.save(name+"A.npy",A1 - A2)
        del A1
        del A2
        gc.collect()
        
        B1 = np.load(self.B_name)
        B2 = np.load(otherMatrix.B_name)
        np.save(name+"B.npy",B1 - B2)
        del B1
        del B2
        gc.collect()
        
        C1 = np.load(self.C_name)
        C2 = np.load(otherMatrix.C_name)
        np.save(name+"C.npy",C1 - C2)
        del C1
        del C2
        gc.collect()
        
        D1 = np.load(self.D_name)
        D2 = np.load(otherMatrix.D_name)
        np.save(name+"D.npy",D1 - D2)
        del D1
        del D2
        gc.collect()
        
        return BlockMatrix(name, 1, self.rows, self.cols)
        
    
    def __rmul__(self, number): 
        name = str(number) + "nm" +self.name 
        
        A = np.load(self.A_name)
        A = A * number
        np.save(name+"A.npy",A)
        del A
        gc.collect()
        
        B = np.load(self.B_name)
        B = B * number
        np.save(name+"B.npy",B)
        del B
        gc.collect()
        
        C = np.load(self.C_name)
        C = C * number
        np.save(name+"C.npy",C)
        del C
        gc.collect()
        
        D = np.load(self.D_name)
        D = D * number
        np.save(name+"D.npy",D)
        del D
        gc.collect()
        
        return BlockMatrix(name, 1, self.rows, self.cols)
       
    def colSum(self):
        lis = []
        
        A = np.load(self.A_name)
        C = np.load(self.C_name)
        for i in xrange(self.cols/2):
            lis.append(A[:,i].sum() + C[:,i].sum())
        del A
        del C
        gc.collect()
        
        B = np.load(self.B_name)
        D = np.load(self.D_name)
        for i in xrange(self.cols/2):
            lis.append(B[:,i].sum() + D[:,i].sum())
        del B
        del D
        gc.collect()
        
        return lis
    
       
    def colMul(self, numbers):
        assert self.cols == len(numbers)
        A = np.load(self.A_name)
        for i in xrange(self.cols/2):
            A[:,i] *= numbers[i]
        np.save(self.A_name, A)
        del A 
        gc.collect()
        
        C = np.load(self.C_name)
        for i in xrange(self.cols/2):
            C[:,i] *= numbers[i]
        np.save(self.C_name, C)
        del C 
        gc.collect()

        B = np.load(self.B_name)
        for i in xrange(self.cols/2):
            B[:,i] *= numbers[i + self.cols/2]
        np.save(self.B_name, B)
        del B
        gc.collect()

        D = np.load(self.D_name)
        for i in xrange(self.cols/2):
            D[:,i] *= numbers[i + self.cols/2]
        np.save(self.D_name, D)
        del D 
        gc.collect()        
        
        
        
        
    
    def mulVector(self,vector):
        assert vector.shape[0] % 2 == 0
        assert vector.shape[0] == self.cols
        length = vector.shape[0] 
        v1 = vector[0:length/2]
        v2 = vector[length/2:]
        A = np.load(self.A_name)
        B = np.load(self.B_name)
        block1 = np.dot(A,v1) + np.dot(B,v2)
        del A
        del B
        gc.collect()
        
        C = np.load(self.C_name)
        D = np.load(self.D_name)
        block2 = np.dot(C,v1) + np.dot(D,v2)
        del C
        del D
        gc.collect()
        
        return np.concatenate((block1,block2))
       
    def loadFromFile(self, files):
        row = 0
        for af in files:
            for line in open(af,"r"):
                lis = line.split(" ")
                assert len(lis) == self.cols
                self.setValues([row for i in xrange(self.cols)], [i for i in xrange(self.cols)], [float(i) for i in lis])
                row = row + 1   
