from PIL import Image
import numpy as np
from random import random
import time
import json

def tp(val:int)->float:
    return ((2*val)/255)-1

def tp1(val:float)->int:
    return round((255*(val+1))/2)

def create_data(matrix, n, m):
    array = []
    blocks_in_line = 256 // m
    for i in range(256 // n):
        for y in range(n):
            line = []
            for j in range(256 // m):
                for x in range(m):
                    pixel = []
                    for color in range(3):
                        pixel.append(tp1(matrix[i * blocks_in_line + j][(y * m * 3) + (x * 3) + color]))
                    line.append(tuple(pixel))
            array+=line
    return array

def mt(mat):
    res = []
    for col in range(len(mat[0])):
        column = []
        for row in range(len(mat)):
            column.append(mat[row][col])
        res.append(column)
    return res

def multiplication (mat1,mat2):
    res = []
    for res_row in range(len(mat1)):
        mat3 = []
        for res_col in range(len(mat2[0])):
            sum = 0
            for k in range(len(mat2)):
                sum += mat1[res_row][k] * mat2[k][res_col]
            mat3.append(sum)
        res.append(mat3)
    return res

def split(n,m):
    X_0 = []
    for y in range(0, 256, n):
        for x in range(0, 256, m):
            arr = []
            for i in range(y, y + n):
                for j in range(x, x + m):
                    arr.append(tp(pixels[j, i][0]))
                    arr.append(tp(pixels[j, i][1]))
                    arr.append(tp(pixels[j, i][2]))
            X_0.append(arr)
    return X_0

def getmMtrixWeight(n,m,p):
    W_1 = []  # Матрица вессов первого слоя
    for i in range(3 * m * n):
        arr = []
        for j in range(p):
            arr.append(random() * 2 - 1)
        W_1.append(arr)
    return W_1

def multnm(alpha,mat1):
    res = []
    mt3 = []
    for res_row in  range(len(mat1)):
        for res_col in range(len(mat1[0])):
            umn = 0
            umn = mat1[res_row][res_col] * alpha
            mt3.append(umn)
        res.append(mt3)
        mt3 = []
    return res

def difference(mt1,mt2):
    res = []
    dif=0
    mt3 =[]
    for res_row in range(len(mt1)):
        for res_col in range(len(mt1[0])):
            dif = mt1[res_row][res_col] - mt2[res_row][res_col]
            mt3.append(dif)
            dif =0
        res.append(mt3)
        mt3 =[]
    return res


def alpha(mat):
    res = sum(np.matmul(element, element) for element in mat)
    return 1/res



image1 = Image.open("coin.jpg")
pixels = image1.load()
x,y = image1.size



while True:
    print("Выберите режип:")
    print("1.режип обучения")
    print("2.режип использования")
    reg = int(input())
    if reg == 1 or reg == 2:
        break
if reg == 1:
    print("Ведите ширину и высоту")
    print("Ширина:")
    m = int(input())
    with open("m.txt", "w") as wm:
        json.dump(m, wm)
    print("Высота:")
    n = int(input())
    with open("n.txt", "w") as wn:
        json.dump(n, wn)
    X_0 = split(n, m)
    print("Введите число нейронов 2 слоя")
    p = int(input())
    with open("p.txt", "w") as wp:
        json.dump(p, wp)
    W_1 = getmMtrixWeight(n,m,p)
    print(W_1[0])
    W_2 = mt(W_1)
    X = []
    Y = []
    print("Максимальная допустимая ошибка:")
    e = int(input())
    while(True):
        start_time = time.time()
        E=0
        for x_i in X_0:
            x_i = [x_i]
            y_i = np.matmul(x_i,W_1)
            Y.append(y_i[0])
            x_i1 = np.matmul(y_i,W_2)
            X.append(x_i1[0])
            delta_x = difference(x_i1,x_i)
            W_1 = difference(W_1, multnm(alpha(x_i),np.matmul(np.matmul(np.transpose(x_i),delta_x),np.transpose(W_2))))
            W_2 = difference(W_2, multnm(alpha(y_i),np.matmul(np.transpose(y_i),delta_x)))
            E_q = 0
            for i in range(3*m*n):
                E_q += delta_x[0][i] * delta_x[0][i]
            E+=E_q
        print(E)
        print("time elapsed: {:.2f}s".format(time.time() - start_time))
        if E<e:
            with open('Weight1.txt','w') as wr1:
               json.dump(W_1,wr1)
            with open('Weight2.txt','w') as wr2:
               json.dump(W_2,wr2)
            break
else:
    with open('m.txt', 'r') as rdm:
        m = json.load(rdm)
    with open('n.txt', 'r') as rdn:
        n = json.load(rdn)
    X_0 = split(n, m)
    with open('p.txt', 'r') as rdp:
        p = json.load(rdp)
    X = []
    Y = []
    start_time = time.time()
    with open('Weight1.txt', 'r') as rd1:
        W_1 = json.load(rd1)
    with open('Weight2.txt', 'r') as rd2:
        W_2 = json.load(rd2)
    for x_i in X_0:
        x_i = [x_i]
        y_i = np.matmul(x_i, W_1)
        Y.append(y_i[0])
        x_i1 = np.matmul(y_i, W_2)
        X.append(x_i1[0])
        print("time elapsed: {:.2f}s".format(time.time() - start_time))

image2 = Image.new("RGB",(256,256))
image2.putdata(create_data(X,n,m))
image2.save("new_coin2.jpg")


