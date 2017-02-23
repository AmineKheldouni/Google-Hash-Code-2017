#!/usr/bin/python
#encoding: utf8

"""
author : Mohammed Amine KHELDOUNI
#################### Hash Code Tranning ####################
"""

import numpy as np
import pickle
import os
import sys
import cvxpy as cvx


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
  row_num, col_num, min_item, max_total = [int(i) for i in fp_line[0].split(' ')]
  pizza_map = np.zeros((row_num, col_num), dtype = np.int)
  for i in range(row_num):
    for j in range(col_num):
      pizza_map[i][j] = 1 if fp_line[i+1][j] == 'T' else 0
  return (row_num, col_num, min_item, max_total, pizza_map)

def write_file(l, weight):
    nbSlices = len(l)
    f = open('output_'+weight+'.out', 'w')
    f.write(str(nbSlices) + '\n')
    for slc in l:
        f.write(str(int(slc[0]))+' '+str(int(slc[1]))+' '+str(int(slc[2]))+' '+str(int(slc[3]))+'\n')
    f.close()
