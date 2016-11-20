# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:44:42 2016

@author: Albert
"""

from BlockMatrix import BlockMatrix
import numpy as np



def TestInit0():
    bm = BlockMatrix("1",0,200,200)
    assert bm.shape == (200,200)
    assert bm.name == "1"
    assert bm.A_name == "1A.npy"
    assert bm.B_name == "1B.npy"
    assert bm.C_name == "1C.npy"
    assert bm.D_name == "1D.npy"
    
  
def TestInit1():
    bm = BlockMatrix("1",0,200,200)
    bm.setValues([0],[0],[100])
    bm1 = BlockMatrix("1",1,200,200)
    assert bm1.getValues([0],[0])[0] == 100
    assert bm.shape == (200,200)
    assert bm.name == "1"
    assert bm.A_name == "1A.npy"
    assert bm.B_name == "1B.npy"
    assert bm.C_name == "1C.npy"
    assert bm.D_name == "1D.npy"
    
   
def TestSetGet():
    bm = BlockMatrix("1",0,200,200)
    bm.setValues([60,0],[60,0],[1,5])
    assert bm.getValues([60],[60])[0] == 1
    assert bm.getValues([0],[0])[0] == 5
    
   
def TestAdd():
    bm1 = BlockMatrix("1",0,200,200)
    bm1.setValues([60,0],[60,0],[1,5])
    bm2 = BlockMatrix("2",0,200,200)
    bm = bm1 + bm2
    assert bm.name == "1a2"
    assert bm.shape == (200,200)
    assert bm.getValues([60],[60])[0] == 2
    assert bm.getValues([0],[0])[0] == 6
    
  
def TestSub():
    bm1 = BlockMatrix("1",0,200,200)
    bm1.setValues([60,0],[60,0],[1,5])
    bm2 = BlockMatrix("2",0,200,200)
    bm = bm2 - bm1
    assert bm.name == "2s1"
    assert bm.shape == (200,200)
    assert bm.getValues([60],[60])[0] == 0
    assert bm.getValues([0],[0])[0] == -4
    
    
def TestNumMul():
    bm = BlockMatrix("1",0,200,200)
    bm.setValues([60],[60],[1])
    bm1 = 0.25 * bm
    assert bm1.getValues([60],[60])[0] == 0.25
    assert bm1.name == "0.25nm1"
    
   
def TestColSum():
    bm1 = BlockMatrix("1",0,10,10)
    bm1.setValues([0,0,1],[0,2,2],[1.0,2,3])
    assert bm1.colSum()[0] == 1+9 
    assert bm1.colSum()[2] == 5+8 
    
  
def TestMulVector():
    bm = BlockMatrix("1",0,2,2)
    n = np.zeros((2,1))
    n[0,0] = 2
    n[1,0] = 2
    r = bm.mulVector(n)
    assert r[0,0] == 4
    assert r[1,0] == 4
    
   
def TestLoad():
    bm = BlockMatrix("1",0,4,4)
    bm.loadFromFile(["a.txt","b.txt"])
    assert bm.getValues([0],[0])[0] == 0.25
    

def TestColMul():
    bm = BlockMatrix("1",0,4,4)
    bm.setValues([0,0],[0,1],[2,4])
    bm.colMul([0.5,0.5,1,1])
    assert bm.getValues([0],[0])[0] == 1
    assert bm.getValues([0],[1])[0] == 2
         
if __name__ == "__main__":
    TestInit0()
    TestInit1()
    TestSetGet()
    TestAdd()
    TestSub()
    TestNumMul()
    TestColSum()
    TestMulVector()
    TestLoad()
    TestColMul()
