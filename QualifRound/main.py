#!/usr/bin/python
#encoding: utf8

"""
#################### Hash Code QualifRound ####################
"""

"""
timeSaved = cvx.Variable(R)
videoInCache = cvx.Variable(C, V)

objective = cvx.Maximize(1000. * sum(timeSaved) / sum([request[j][2] for j in range(R)]))

constrains = [ videoInCache >= 0, videoInCache <= 1]
for c in range(C):
  constrains.append(sum([videoInCache[c, v] * video_sizes[v] for v in range(V)]) <= X)

for r in range(R):
  constrains.append(timeSaved[r] >= 0)
  tmp_request = [int(request[r][i]) for i in range(3)]
  for c in range(C):
    constrains.append(timeSaved[r]  >= (endpointLatency[tmp_request[1]] - endpointConnection[tmp_request[1], c]) * videoInCache[c, tmp_request[0]])





prob = cvx.Problem(objective, constrains)
prob.solve()
print("Solution :", objective.value)
"""

import numpy as np
import pickle
import os
import sys
import cvxpy as cvx
import math as m
from utils import *


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
  #print("Size of Videos : ", video_sizes)
  endpointLatency = np.zeros(E)
  endpointConnection = np.zeros((E, C))
  idLine = 1

  for i in range(E):
    for j in range(C):
      endpointConnection[i, j] = m.inf
  for i in range(E):
    idLine += 1
    a,b = [int(k) for k in fp_line[idLine].split(' ')]
    endpointLatency[i] = a
    for j in range(b):
        idLine = idLine + 1
        a, b = [int(k) for k in fp_line[idLine].split(' ')]
        endpointConnection[i, a] = b
  #print("Connection EndPoint-Cache : ",endpointConnection)
  #print("Connexion EndPoint to Latency : ", endpointLatency)
  request = np.zeros((R,3))
  for j in range(len(request)):
      idLine +=1
      a,b,c = [int(i) for i in fp_line[idLine].split(' ')]
      request[j][0] =  a
      request[j][1] =  b
      request[j][2] =  c
  #print(request)
  return (V, E, R, C, X, video_sizes, endpointLatency, endpointConnection, request)

def write_file(videoCache):
    C = len(videoCache)
    V = len(videoCache[0])
    nb_cache = 0
    for i in range(C):
      if videoCache[i] != [0]*V:
        nb_cache += 1
    f = open('output.out', 'w')
    f.write(str(nb_cache) + '\n')
    for i in range(C):
      f.write(str(i)+' ')
      for j in range(V):
        if int(videoCache[i, j]) == 1:
          f.write(str(j)+' ')
      f.write('\n')
    f.close()

V, E, R, C, X, video_sizes, endpointLatency, endpointConnection, request = read_file("./", "me_at_the_zoo.in")

videoValue = cost_request(request,video_sizes, endpointLatency, endpointConnection)
show_matrix(videoValue)
weight = X
videoTaken = cvx.Bool(V)
print("video_size ", video_sizes)
print("X : ", X)
objective = cvx.Maximize(sum([videoValue[i][0]*videoTaken[i] for i in range(V)]))

constrains = [ ]

constrains.append(sum([video_sizes[i]*videoTaken[i] for i in range(V)]) <= weight)

prob = cvx.Problem(objective, constrains)
prob.solve()
print("Solution :", objective.value)

videoTakenFinally = videoTaken.value
for i in range(len(videoTakenFinally)):
  if videoTakenFinally[i] > 0:
    videoTakenFinally[i] = 1
  else :
    videoTakenFinally[i] = 0

videoTakenFinally = videoTakenFinally.T
print(videoTakenFinally)
