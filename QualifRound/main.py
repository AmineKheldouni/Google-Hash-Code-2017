#!/usr/bin/python
#encoding: utf8

"""
#################### Hash Code Tranning ####################
"""

import numpy as np
import pickle
import os
import sys
import cvxpy as cvx
import math as m

def show_matrix(M):
    mat = ""
    for i in range(len(M)):
        mat += '|'
        for j in range(len(M[0])):
            mat += str(M[i][j])
        mat += '|\n'
    return mat

def read_file(file_path, file_name):
  fp = open(os.path.join(file_path, file_name) ,'r')
  fp_line = fp.read().split('\n')
  V, E, R, C, X = [int(i) for i in fp_line[0].split(' ')]
  video_sizes = [int(i) for i in fp_line[1].split(' ')]
  print("V : ", V)
  print("E : ", E)
  print("R : ", R)
  print("C : ", C)
  print("X : ", X)
  print("Size of Videos : ", video_sizes)
  endpointLatency = []
  endpointConnection = np.zeros((E, C))
  idLine = 2

  for i in range(E):
    for j in range(C):
      endpointConnection[i, j] = m.inf

  for i in range(E):
    idLine += 1
    endpointLatency[i] = fp_line[idLine]
    for j in range(fp_line[idLine][1]):
      idLine = idLine + 1
      endpointConnection[i,fp_line[idLine][0]] = fp_line[idLine][1]
  print("Connection EndPoint-Cache : ",endpointConnection)
  print("Connexion EndPoint to Latency : ", endpointLatency)
  return (V, E, R, C, X, endpointLatency, endpointConnection)

def write_file(l, weight):
    nbSlices = len(l)
    f = open('output_'+weight+'.out', 'w')
    f.write(str(nbSlices) + '\n')
    for slc in l:
        f.write(str(int(slc[0]))+' '+str(int(slc[1]))+' '+str(int(slc[2]))+' '+str(int(slc[3]))+'\n')
    f.close()


read_file("./", "me_at_the_zoo.in")
