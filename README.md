为解决上万维大矩阵相乘问题，而编写的python代码。

适用范围：

- 内存较少（比如4G内存）
- 磁盘空间较大
- 磁盘闲时占用率较小
- 磁盘读写速率较快

原理：

- 矩阵乘法可分块进行
- 用磁盘空间换内存空间
- 基于numpy实现

弊端：

- 计算较慢，有大量的磁盘读写操作
- 每个对象需设置不同的名字

优点：

- 占用内存大大减少
- 通过相关函数的合理使用可减少磁盘读写次数


导入模块和类
```
from BlockMatrix import BlockMatrix
```

初始化（1）：未存在相关文件
```python
bm = BlockMatrix("1",0,200,200)
```
第一个参数为名称，不同对象名称不能重复，第二个为是否已存在（相关文件），第三个为行数，第四个为列数
，行数与列数必须为偶数。数据类型为float16，开始各位置元素初始化为1

初始化（2）：已存在
```python
bm = BlockMatrix("1",1,200,200)
```

赋值与取值

```python
bm.setValues([60,0],[60,0],[1,5])
bm.getValues([60],[60])
```

```python
setValues([],[],[])
```

第一个参数是要赋值位置的行数列表，第二个为列数列表，第三个为值列表。这三个列表
中元素一一对应。

```python
bm.getValues([],[])
```
第一个参数是要取值位置的行数列表，第二个为列数列表。得到的为值列表。同样，也是一一对应。

Tips：由于大量的磁盘IO操作费时，建议不要一个一个元素单独赋值，而是先保存，到一定数据量
时使用列表赋值。从而减少IO时间。

矩阵的加法

```python
bm1 = BlockMatrix("1",0,200,200)
bm1.setValues([60,0],[60,0],[1,5])
bm2 = BlockMatrix("2",0,200,200)
bm = bm1 + bm2
```

矩阵的减法

```python
bm1 = BlockMatrix("1",0,200,200)
bm1.setValues([60,0],[60,0],[1,5])
bm2 = BlockMatrix("2",0,200,200)
bm = bm2 - bm1
```

Tips：加法和减法的两个矩阵维度不一样都会产生错误

矩阵的数乘

```python
bm = BlockMatrix("1",0,200,200)
bm.setValues([60],[60],[1])
bm1 = 0.25 * bm
```
Tips：注意只能在左侧乘

对矩阵每列求和

```python
bm1 = BlockMatrix("1",0,10,10)
bm1.colSum()
```

返回为列表，从0到n-1依次是0列到n-1列的求和

对矩阵每一列乘以不同的数

```python
bm = BlockMatrix("1",0,4,4)
bm.setValues([0,0],[0,1],[2,4])
bm.colMul([0.5,0.5,1,1])
```

传入参数为每一列要乘的数，结果直接赋值给自身

矩阵与向量的乘法

```python
bm = BlockMatrix("1",0,2,2)
n = np.zeros((2,1))
r = bm.mulVector(n)
```
Tips：矩阵列数与向量行数相同

从文件中读入矩阵

```python
bm = BlockMatrix("1",0,4,4)
bm.loadFromFile(["a.txt","b.txt"])
```

参数可以时文件列表，函数会从左到右构建矩阵

性能分析：

若原矩阵占用为A（A足够大其他非矩阵占用内存可忽略）


| 函数         | 占用内存最大值    |  
| --------    | -----: | 
| Init(0)        | 0.25A      |
| Init(1)        | 0      |
| getValues()        | 0.25A      | 
| setValues()        | 0.25A      | 
| +        | 0.5A      |
| -        | 0.5A      |
| 常数乘        | 0.25A      |
| colSum()        | 0.5A      |
| colMul()        | 0.25A      |
| mulVector        | 0.5A      |      

Tips：不用临时变量（直接使用或用旧变量）可减少内存
