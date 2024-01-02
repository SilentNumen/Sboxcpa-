# -*- coding: utf-8 -*-

import math

S_Box= [ [14, 4,  13, 1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
         [0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
	     [4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
	     [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]]

#补充plaintext取值列表（十进制），与仿真阶段取值一样
plaintext = [33,36,18,44,35,51,55,48,52,22,15,31,13,11,59,20,27,31,19,20]
#补充power_std列表，由仿真阶段得到的汉明重量向量
power_std1 = [2, 2, 1, 2, 2, 2, 3, 1, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 4, 3]


def to_bin(value, num):#十进制数据，二进制位宽
	bin_chars = ""
	temp = value
	for i in range(num):
		bin_char = bin(temp % 2)[-1]
		temp = temp // 2
		bin_chars = bin_char + bin_chars
	return bin_chars.upper()
    
    

def HWfun(num):#计算汉明重量
    # 统计输入num的汉明重量并返回
    hmweight = []
    for x in num:
        count = 0
        x = to_bin(x, 6)
        for y in x:
            if y == '1':
                count += 1
        hmweight.append(count)
    return hmweight


def Meanfun(n,num):
    total=0
    for i in range(0,n):
        total=total+num[i]
    return total/n

def sboxout(n,P,key):
    pxork=0
    cv=0#列
    rv=0#行
    bpxork=0
    sout=[]
    for i in range(0,n):
        pxork=P[i]^key
        bpxork=str(to_bin(pxork,8))[2:]
        cv=2*int(bpxork[0])+int(bpxork[5])
        rv=8*int(bpxork[1])+4*int(bpxork[2])+2*int(bpxork[3])+int(bpxork[4])
        sout.append(S_Box[cv][rv])
    return sout



def Corrfun(n,pstd,ptest):#计算相关系数
   #补充相关系数函数，返回两个向量的相关系数值
   xv = sum(pstd) / n  # pstd
   yv = sum(ptest) / n  # ptest

   fenzi = 0
   fenmux = 0
   fenmuy = 0
   for i in range(0, n):
       fenzi += (pstd[i] - xv) * (ptest[i] - yv)
       fenmux += math.pow((pstd[i] - xv), 2)
       fenmuy += math.pow((ptest[i] - yv), 2)
   coor = fenzi / (math.sqrt(fenmux) * math.sqrt(fenmuy))
   return coor


if __name__ == "__main__":
    #遍历所有可能密钥，计算每个猜测密钥对应的相关系数，求最大系数对应的猜测密钥
    testkey = 0
    maxcoor = 0
    for key in range(1, 64):
        sout = sboxout(20, plaintext, key)
        hw = HWfun(sout)
        coor = Corrfun(20, power_std1, ptest=hw)
        if coor > maxcoor:
            maxcoor = coor
            testkey = key
    print(testkey)




     
    
    
    






