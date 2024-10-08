

# This file was *autogenerated* from the file ntt_4_step.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_12 = Integer(12); _sage_const_6 = Integer(6); _sage_const_576460752303415297 = Integer(576460752303415297); _sage_const_288482366111684746 = Integer(288482366111684746)#计算a*b mod Zq/x^n+1
def polymul(a, b, n, q):
    assert(len(a) == len(b) == n)
    Zq = GF(q)
    c = [Zq(_sage_const_0 )] * n
    for i in range(n):
        for j in range(n):
            if i+j > n-_sage_const_1 :
                c[i+j-n] += -a[i] * b[j] 
            else:
                c[i+j] += a[i] * b[j]
    return c


def find_prime(n1, n2, bit_len):
    n = n1 * n2
    largest_value = _sage_const_2  ** bit_len
    value = previous_prime(largest_value)
    while True:
        if value % (_sage_const_2 *n) == _sage_const_1  and value % (_sage_const_2 *n1) == _sage_const_1  and value % (_sage_const_2 *n2) == _sage_const_1 :
            return value
        value = previous_prime(value)


def znorder(a, q):
    mul = _sage_const_1 
    if xgcd(a, q)[_sage_const_0 ] == _sage_const_1 :
        for i in range(_sage_const_1 , q):
            mul = (mul * a) % q
            if mul % q == _sage_const_1 :
                return i


def get_root_of_unity(n, q):
    for i in range(_sage_const_2 , q):
        if znorder(i, q) == n:
            return i


def bit_reverse(index, bit_len):
    return int('{:0{width}b}'.format(index, width=bit_len)[::-_sage_const_1 ], _sage_const_2 )


#####################################基础蝴蝶操作#####################################
#is_4step=0时，得到负折叠卷积的结果,整体过程符合FFT-trick,左边的子树分解为减,为比特翻转结果
#is_4step=1时，计算的结果为循环卷积,整体过程为经典迭代形式,顺序为比特翻转结果
def forward_ntt(src, n, q, root, is_4step=False):
    a = src[:]
    length = _sage_const_1 
    while(length < n):
        #print("length=",length)
        for tid in range(n >> _sage_const_1 ): #只关注上半部分
            step = int(n / length / _sage_const_2 ) #代表的是步长 每一个组的半长
            psi_step = int(tid / step) #代表的是位于当前层的第几组中
            tar_idx = psi_step * step * _sage_const_2  + (tid % step) #tar_idx代表的是第tid个蝴蝶操作开始的位置
            step_group = length + psi_step
            #print(step_group, bit_reverse(step_group, log(n, 2)))
            psi = root ** bit_reverse(step_group, log(n, _sage_const_2 ))
            if is_4step:
                step_group = psi_step
                psi = root ** bit_reverse(step_group, log(n, _sage_const_2 ) - _sage_const_1 ) #旋转因子
            U, V = Zq(a[tar_idx]), Zq(a[tar_idx + step])
            a[tar_idx], a[tar_idx + step] = U + V*psi, U - V*psi
        length <<= _sage_const_1 
    return a

#同forward_ntt
def inverse_ntt(src, n, q, inv_root, is_4step=False):
    a = src[:]
    step = _sage_const_1 
    while(step < n):
        for tid in range(n >> _sage_const_1 ):
            len = int(n / step / _sage_const_2 )
            psi_step = int(tid / step)
            tar_idx = psi_step * step * _sage_const_2  + (tid % step)
            step_group = len + psi_step
            psi = inv_root ** bit_reverse(step_group, log(n, _sage_const_2 ))
            if is_4step:
                step_group = psi_step
                psi = inv_root ** bit_reverse(step_group, log(n, _sage_const_2 ) - _sage_const_1 )
            U, V = Zq(a[tar_idx]), Zq(a[tar_idx + step])
            a[tar_idx], a[tar_idx + step] = (U + V) / _sage_const_2 , (U - V) * psi / _sage_const_2 
        step <<= _sage_const_1 
    return a
###########################################################################




##########################循环卷积NTT########################
#循环卷积NTT
def postive_NTT(src,n,q,root_n): 
    a = forward_ntt(src, n, q, root_n, is_4step=True)
    return a

#逆循环卷积NTT
def postive_NTT_inv(src,n,q,root_n):
    inv_root = _sage_const_1  / root_n
    a = inverse_ntt(src, n, q, inv_root, is_4step=True)
    return a

#####################################################




#####school book计算在Zq[x] / x^n + 1上的NTT#######
def schoolbook(a, b, n, n1, n2, q):
    c = polymul(a, b, n ,q)
    return c
##################################################




###########负循环卷积NTT的计算####################
def negative_MUL(a, b, n, n1, n2, q ,root_n):
    inv_root_n = _sage_const_1  / root_n
    #print("root_n",root_n)
    #print("inv_root_n",inv_root_n)
    a_hat = forward_ntt(a, n, q, root_n)
    # print(a_hat)
    b_hat = forward_ntt(b, n, q, root_n)
    c_hat = [a_hat[i] * b_hat[i] for i in range(n)]
    c_prime = inverse_ntt(c_hat, n, q, inv_root_n)
    return c_prime,a_hat
    # print(c_prime)
    #print("negative",c_prime == c)
    #a_prime = inverse_ntt(a_hat, n, q, inv_root_n)
    #print("negative",a_prime == a)
###############################################





###########4-step的循环卷积NTT###########################################

#循环卷积NTT,输出比特翻转顺序
def forward_ntt_4step(src, n1, n2, q, root_n):
    n = n1 * n2    
    root_n1 = root_n ** n2
    root_n2 = root_n ** n1

    M12 = MatrixSpace(Zq, n1, n2) #MatrixSpace 是用于定义矩阵空间的一个类

    # step 1
    a = M12(src)
    for j in range(a.ncols()):
        a[:,j] = column_matrix(forward_ntt(a[:,j].list(), n1, q, root_n1, is_4step=True))

    for i in range(n1):
        for j in range(n2):
            print(a[i][j],",",end="")
    print("\n")
    # step 2
    W_n = M12()
    for i in range(W_n.nrows()):
        for j in range(W_n.ncols()):
            br_i = bit_reverse(i, log(n1, _sage_const_2 ))
            W_n[i, j] = root_n ** (br_i * j)
    a = a.elementwise_product(W_n)


    # step 3
    a = a.transpose()

    # step 4
    for j in range(a.ncols()):
        a[:,j] = column_matrix(forward_ntt(a[:,j].list(), n2, q, root_n2, is_4step=True))

    a = a.transpose()

    return a.list()

#逆循环卷积NTT,输出正常顺序
def inverse_ntt_4step(src, n1, n2, q ,root_n):
    n = n1 * n2
    
    root_n1 = root_n ** n2
    root_n2 = root_n ** n1
    inv_root_n = _sage_const_1  / root_n
    inv_root_n1 = _sage_const_1  / root_n1
    inv_root_n2 = _sage_const_1  / root_n2

    M12 = MatrixSpace(Zq, n1, n2)

    a = M12(src)

    a = a.transpose()
    for j in range(a.ncols()):
        a[:,j] = column_matrix(inverse_ntt(a[:,j].list(), n2, q, inv_root_n2, is_4step=True))

    a = a.transpose()

    W_n = M12()
    for i in range(W_n.nrows()):
        for j in range(W_n.ncols()):
            br_i = bit_reverse(i, log(n1, _sage_const_2 ))
            W_n[i, j] = (inv_root_n ** (br_i * j))
            #W_n[i, j] = 1 / tmp
    a = a.elementwise_product(W_n)


    for j in range(a.ncols()):
        a[:,j] = column_matrix(inverse_ntt(a[:,j].list(), n1, q, inv_root_n1, is_4step=True))

    return a.list()

def ntt4step(a, b, n, n1, n2, q,root_n):

    a_hat_prime = forward_ntt_4step(a, n1, n2, q,root_n)
    # print(a_hat_prime)
    b_hat_prime = forward_ntt_4step(b, n1, n2, q,root_n)
    c_hat_prime = [a_hat_prime[i] * b_hat_prime[i] for i in range(n)]
    c_prime = inverse_ntt_4step(c_hat_prime, n1, n2, q,root_n)
    
    a_hat_prime_2 = inverse_ntt_4step(a_hat_prime, n1, n2, q,root_n)
    # print(c_prime)
    #print("a == a_hat_prime_2",a == a_hat_prime_2)
    return c_prime,a_hat_prime
    #return [],a_hat_prime
    
    #print('c_prime == c', c_prime == c)
    #a_prime = inverse_ntt_4step(a_hat_prime, n1, n2, q)
    #print('a_prime == a', a_prime == a)
###############################################################################





###########4-step的负数循环卷积NTT################################################
def neg_forward_ntt_4step(src, n1, n2, q, root_2n):
    n = n1 * n2
    M12 = MatrixSpace(Zq, n1, n2) #MatrixSpace 是用于定义矩阵空间的一个类
    M21 = MatrixSpace(Zq, n2, n1)

    root_2n1 = root_2n ** n2

    a = M12(src)

    for j in range(a.ncols()):
        a[:,j] = column_matrix(forward_ntt(a[:,j].list(), n1, q, root_2n1, is_4step=False))

    W_n = M12()
    for i in range(W_n.nrows()):
        for j in range(W_n.ncols()):
            br_i = bit_reverse(i, log(n1, _sage_const_2 ))
            W_n[i, j] = root_2n ** ( (_sage_const_2  *br_i + _sage_const_1  )* j)
    a = a.elementwise_product(W_n)

    a = a.transpose()

    root_n2 = root_2n ** (_sage_const_2  * n1)
    for j in range(a.ncols()):
        a[:,j] = column_matrix(forward_ntt(a[:,j].list(), n2, q, root_n2, is_4step=True))

    a = a.transpose()
    return a.list()

def negative_inverse_ntt_4step(src, n1, n2, q ,root_2n):
    n = n1 * n2
    

    root_n2 = root_2n ** (_sage_const_2  * n1)
    inv_root_2n = _sage_const_1  / root_2n
    inv_root_n2 = _sage_const_1  / root_n2
    M12 = MatrixSpace(Zq, n1, n2)
    M21 = MatrixSpace(Zq, n2, n1)

    # step 1
    a = M12(src) #按行展开

    a = a.transpose()
    for j in range(a.ncols()):
        a[:,j] = column_matrix(inverse_ntt(a[:,j].list(), n2, q, inv_root_n2, is_4step=True))

    # step 2
    a = a.transpose()

    # step 3
    W_n = M12()
    for i in range(W_n.nrows()):
        for j in range(W_n.ncols()):
            br_i = bit_reverse(i, log(n1, _sage_const_2 ))
            W_n[i, j] = inv_root_2n ** ( (_sage_const_2  *br_i + _sage_const_1  )* j)
    a = a.elementwise_product(W_n)


    # step 4
    root_2n1 = root_2n ** n2
    inv_root_2n1 = _sage_const_1  / root_2n1
    for j in range(a.ncols()):
        a[:,j] = column_matrix(inverse_ntt(a[:,j].list(), n1, q, inv_root_2n1, is_4step=False))

    return a.list()

def negative_ntt4step(a, b, n, n1, n2, q ,root_2n):

    a_hat_prime = neg_forward_ntt_4step(a, n1, n2, q, root_2n)
    b_hat_prime = neg_forward_ntt_4step(b, n1, n2, q, root_2n)

    c_hat_prime = [a_hat_prime[i] * b_hat_prime[i] for i in range(n)]
    c_hat_prime_2 = negative_inverse_ntt_4step(c_hat_prime, n1, n2, q ,root_2n)

    
    
    a_hat_prime_2 = negative_inverse_ntt_4step(a_hat_prime, n1, n2, q ,root_2n)
    #print("a_hat_prime_2 == a" ,a_hat_prime_2 == a)
    return c_hat_prime_2,a_hat_prime
#######################################################################################





if __name__ == "__main__":
    n = _sage_const_2 **_sage_const_12 
    n1 = _sage_const_2 **_sage_const_6 
    n2 = _sage_const_2 **_sage_const_6 
    # q = find_prime(n1, n2, 15)
    q = _sage_const_576460752303415297 #12289
    """
    assert(q % (2*n) == 1)
    assert(q % (2*n1) == 1)
    assert(q % (2*n2) == 1)
    """
    
    Zq = GF(q)

    a = []
    for i in range(n):
        #a.append(Zq(i))
        a.append(Zq(i))
        #a.append( Zq.random_element())

    b = []
    for i in range(n):
        b.append(Zq(i))
        #b.append( Zq.random_element())

    #print(a)
    #print(b)
    root_n = Zq(_sage_const_288482366111684746 ) #Zq(get_root_of_unity(n, q))
    #root_2n = Zq(get_root_of_unity(2 * n, q))

    c3 ,a2 = ntt4step(a, b, n, n1, n2, q,root_n)
    a3 = postive_NTT(a,n,q,root_n)
    a4 = postive_NTT_inv(a3,n,q,root_n)
    print("positive NTT正确:",a4 == a)
    print("ntt4step的正向NTT满足比特翻转的顺序:",a3 == a2)
    
    """
    c1 = schoolbook(a, b, n, n1, n2, q)
    c2 ,a1 = negative_MUL(a, b, n, n1, n2, q,root_2n)
    print("negative_MUL正确",c1 == c2)
    c4,a5 = negative_ntt4step(a, b, n, n1, n2, q ,root_2n)
    print("negative_ntt4step正确",c4 == c1)
    print("negative_ntt4step的正向NTT满足比特翻转的顺序",a1 == a5)
    """


