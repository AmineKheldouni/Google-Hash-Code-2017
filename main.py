#!/usr/bin/python
#encoding: utf8

"""
author : Mohammed Amine KHELDOUNI
#################### Hash Code Tranning ####################
"""

import numpy as np

import cvxpy as cvx


def show_matrix(M):
    mat = ""
    for i in range(len(M)):
        mat += '|'
        for j in range(len(M[0])):
            mat += str(M[i][j])
        mat += '|\n'
    return mat

def generatePizza(filename):
    file_object = open(filename, 'r')
    nb_rows = int(file_object.readline(1))
    nb_cols = int(file_object.readline(2))
    l = int(file_object.readline(3))
    h = int(file_object.readline(4))

    pizza1 = file_object.readlines()
    pizza = np.array([['T']*nb_cols]*nb_rows)
    for i in range(nb_rows):
        for j in range(nb_cols):
            pizza[i,j] = pizza1[i][j]

    print("rows : ", nb_rows)
    print("cols : ", nb_cols)
    print("min comp. : ", l)
    print("max comp. : ", h)
    print("pizza :\n")
    print(show_matrix(pizza))
    return nb_rows, nb_cols, l, h, pizza

def matrixTM(p):
    T = []
    M = []

    for i in range(len(p)):
        for j in range(len(p[0])):
            if j==0:
                if p[i][j] == 'T':
                    T.append([1])
                    M.append([0])
                else :
                    T.append([0])
                    M.append([1])
            else:
                if p[i][j] == 'T':
                    T[i].append(1)
                    M[i].append(0)
                else :
                    T[i].append(0)
                    M[i].append(1)
    return T, M

def slices(p, low, high):
    list_slices = []
    for i in range(len(p)):
        for j in range(len(p[0])):
            for k in range(i+1,len(p)+1):
                for l in range(j+1, len(p[0])+1):
                    Tmatrix, Mmatrix = matrixTM(p[j:l,i:k])
                    total_T = sum_elt(Tmatrix)
                    total_M = sum_elt(Mmatrix)
                    if total_T>=low and total_T<=high and total_M>=low and \
                    total_M<=high:
                        list_slices.append((i, j, k, l))
    return list_slices

def value_objects(o):
    L = []
    for x in o:
        print(x)
        L.append((x[3]-x[1])*(x[2]-x[0]))
    return L

def sum_elt(M):
    S = 0
    for line in M:
        S += sum(line)
    return S

def nb_slices_takingPart(list_obj):
    N = 0
    for x in list_obj:
        a, b, c, d = x

def in_object(ctp, k, o):
    global nb_cols
    W = 0
    j = ctp%nb_cols
    i = (ctp-j)//nb_cols
    a, b, c, d = o[k]
    if i>=b and i<=d and j>=a and j<=c:
        W = 1
    return W

nb_rows, nb_cols, l, h, pizza = generatePizza("example.in")

score = cvx.Variable()

objects = slices(pizza, l, h)

for i in range(len(objects)):
    a,b,c,d = objects[i]
    print(show_matrix(pizza[b:d, a:c]))
    print("Tomates :", sum_elt(matrixTM(pizza[b:d, a:c])[0]))
    print("Champis :", sum_elt(matrixTM(pizza[b:d, a:c])[1]))

objects_val = value_objects(objects)
print(objects)
print("objet valeur : ",objects_val)
pizza_covered = cvx.Variable(nb_rows*nb_cols, len(objects))
pizza_covered_x = cvx.Variable(nb_rows*nb_cols)
pizza_covered_y = cvx.Variable(len(objects))

objective = cvx.Maximize(score)
constrains = [  score == pizza_covered_y.T * objects_val,
                pizza_covered == np.array([[in_object(c, k, objects) for k in range(len(objects))] for c in range(nb_rows*nb_cols)]),
                pizza_covered_x == sum(pizza_covered),
                pizza_covered_y == sum(pizza_covered.T),
                pizza_covered >= 0,
                pizza_covered <= 1,
                pizza_covered_y >= 0,
                pizza_covered_x >= 0
                ]

prob = cvx.Problem(objective, constrains)

print("Solution : ", prob.solve())
nb_slices = 0
vect = pizza_covered_y.T
