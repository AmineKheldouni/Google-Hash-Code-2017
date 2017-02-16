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


nb_rows, nb_cols, l, h, pizza = generatePizza("example.in")

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
    j = ctp%nb_cols
    i = (ctp-j)//nb_cols
    a, b, c, d = o[k]
    if i>=b and i<=d and j>=a and j<=c:
        return 1
    return 0

score = cvx.Variable()

objects = slices(pizza, l, h)
objects_val = value_objects(objects)

pizza_covered = cvx.Int(nb_rows*nb_cols, len(objects))

objective = cvx.Maximize(score)

constrains = [  score == sum(pizza_covered) * np.array(objects_val).T,
                pizza_covered == np.array([[round(in_object(c, k, objects)) for k in range(len(objects))] for c in range(nb_rows*nb_cols)]),
                sum(pizza_covered) == np.array(objects_val),
                np.sum(pizza_covered, axis=-1) <= 1,
                pizza_covered >= 0,
                pizza_covered <= 1
                ]

prob = cvx.Problem(objective, constrains)

print("Solution : ", round(prob.solve()))
nb_Slices = 0
vect_pizza = pizza_covered.value
print("Pizza_covered sum")
print(sum(vect_pizza))
print("Pizza_covered sum T")
print(sum(vect_pizza.T))
print("#############")

def objectKinSack(k,v):
    S = 0
    for i in range(nb_rows):
        for j in range(nb_cols):
            S += v[j+i*nb_cols, k]
    return S

for k in range(len(objects)):
    if objectKinSack(k,vect_pizza) >= 1:
        nb_Slices += 1
print("Number of Slices : ", nb_Slices)
