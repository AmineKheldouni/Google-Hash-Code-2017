# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pickle
import os
import sys



def read_file(file_path, file_name):

  fp = open(os.path.join(file_path, file_name) ,'r')
  fp_line = fp.read().split('\n')

  row_num, col_num, min_item, max_total = [int(i) for i in fp_line[0].split(' ')]

  pizza_map = np.zeros((row_num, col_num), dtype = np.int)

  for i in range(row_num):
    for j in range(col_num):
      pizza_map[i][j] = 1 if fp_line[i+1][j] == 'T' else 0

  return (row_num, col_num, min_item, max_total, pizza_map)

def get_valid_rect() :
  valid_rect = []
  for i in range(1, max_total+1) :
    for j in range(i, max_total+1) :
      if  min_item * 2 <= i * j and i * j <=  max_total :
        valid_rect.append((i,j))
        if i!=j :
        	valid_rect.append((j,i))
  return sorted(valid_rect, key=lambda x : x[0] * x[1], reverse = True)

def rect_is_valid_here(rect, i,j):
  cols = rect[1]
  rows = rect[0]
  if rows + i > row_num or cols + j > col_num: # rect is outside the pizza
    return False
  sub_pizza = pizza_map[i:i+rows,j:j+cols]
  area = sub_pizza.size
  Tsums = np.sum(sub_pizza)
  Msums = area - Tsums
  if Tsums >= min_item and Msums >= min_item:
    return True
  else:
    return False


def get_rect_validation_map():
  rects_validation_map=[]
  for rect in rects_candidates:
    rects_validation_map.append(np.zeros(pizza_map.shape, dtype=np.int))
    map = rects_validation_map[-1]
    for i in range(row_num):
      for j in range(col_num):
        if rect_is_valid_here(rect,i,j):
          map[i,j]=1
  return rects_validation_map

## return list of valid rects: [(h0,w0), (h1,w1), (h2,w2), ...]
def give_all_valid_rects_locally(i,j):
  valid_rects=[]
  for k in range(len(rects_candidates)):
    rows, cols = rects_candidates[k]
    sum = np.sum(cover_map[i:i+rows,j:j+cols]);
    if sum > 0: continue
    validation_map = rects_validation_map[k]
    if validation_map[i,j] == 1:
    	valid_rects.append(rects_candidates[k])
  return valid_rects

## [(i0,j0), (i1,j1), (i2,j2)...]
#def find_start_points() :
#  rows, cols = np.where(cover_map == 0)
#  all_points = [(i,j) for i,j in zip(rows, cols)]

#  return sorted(all_points , key=lambda x : x[0], reverse = False)

def next_pos(i,j):
  if not (i>=0 and i < row_num): raise RuntimeError
  if not ( j>=0 and j < col_num) : raise RuntimeError
  if j < col_num -1:
    j += 1
  else: # new line
    j = 0
    i += 1

  if i >= row_num or j >= col_num:
    return -1, -1

  return i,j

def search_in_pizza():

  point_i = 0
  point_j = 0
  index = 1

  while (True):
    if cover_map[point_i, point_j] == 0:

      #here, i,j is valid, covermap[i,j]==0
      possible_moves = give_all_valid_rects_locally(point_i, point_j)
      if len(possible_moves) != 0:
        move_i, move_j = possible_moves[0]
        cover_map[point_i: point_i + move_i, point_j: point_j + move_j] = np.ones((move_i, move_j)) * index
        index += 1
        action_list.append((point_i, point_j, point_i+move_i-1, point_j+move_j-1))
        point_j += move_j - 1

    point_i, point_j = next_pos(point_i, point_j)
    if point_i == -1 or point_j == -1:
        return

def cover_area():
  return np.sum(cover_map > 0)

def submission():
  nb_slices = len(action_list)
  f = open('output2.out', 'w')
  f.write(str(nb_slices) + '\n')
  for rect in action_list :
    f.write(str(int(rect[0])) + ' ' + str(int(rect[1])) + ' ' + str(int(rect[2])) + ' ' + str(int(rect[3])) + '\n')
  f.close()

def visualisation():
  fp = open('cover_map.txt', 'w')
  for i in range(row_num):
    fp.write(''.join(map(str, list(cover_map[i]))))
    fp.write('\n')

  fp.close()

row_num, col_num, min_item, max_total, pizza_map = read_file('./', 'big.in')
rects_candidates = get_valid_rect()
rects_validation_map = get_rect_validation_map()
cover_map = np.zeros(pizza_map.shape, dtype=np.int)
action_list = []
search_in_pizza()
print(cover_area())
submission()
visualisation()
