
""" Hash Code - Practice Round
### Hash Winners Team ###"""
# Author : Mohammed Amine KHELDOUNI
# Kind regards to TuningMaster team which helped us for modeling the problem.

import numpy as np

def show_matrix(M):
    mat = ""
    for i in range(len(M)):
        mat += '|'
        for j in range(len(M[0])):
            mat += str(M[i][j])
        mat += '|\n'
    print(mat)

def generatePizza(filename):
    file_object = open(filename, 'r')
    line = file_object.read().split('\n')
    nb_rows, nb_cols, l, h = [int(i) for i in line[0].split(' ')]
    pizza = np.zeros((nb_rows, nb_cols), dtype = np.int)
    for i in range(nb_rows):
        for j in range(nb_cols):
            pizza[i][j] = 1 if line[i+1][j] == 'T' else 0

    print("rows : ", nb_rows)
    print("cols : ", nb_cols)
    print("min comp. : ", l)
    print("max comp. : ", h)
    return nb_rows, nb_cols, l, h, pizza

def valid_slices(l, h):
    list_valid_slices = []
    for i in range(1, h+1):
        for j in range(i, h+1):
            if 2*l <= i*j and i*j <= h:
                list_valid_slices.append((i, j))
                if i != j:
                    list_valid_slices.append((j ,i))
    return sorted(list_valid_slices, key=lambda x : x[0]*x[1], reverse = True)

def point_slice(a, b, c, d, n, m, l, p):
    if a + c > n or b + d > m:
        return False
    subpizza = p[c:c+a, d:d+b]
    Ttot = np.sum(subpizza)
    Mtot = subpizza.size - Ttot
    if Ttot >= l and Mtot >= l:
        return True
    else:
        return False

def valid_map(n, m, l, h, p):
    list_valid_map = []
    validSlices = valid_slices(l, h)
    for slc in validSlices:
        list_valid_map.append(np.zeros(p.shape, dtype=np.int))
        p_map = list_valid_map[-1]
        for i in range(n):
            for j in range(m):
                if point_slice(slc[0], slc[1], i, j, n, m, l, p):
                    p_map[i, j] = 1
    return list_valid_map

def get_slices(n, m, l, h, i, j, p):
    slices = []
    validSlices = valid_slices(l, h)
    for k in range(len(validSlices)):
        a, b = validSlices[k]
        pizza_covered = np.zeros(p.shape, dtype=np.int)
        S = np.sum(pizza_covered[i:i+a, j:j+b])
        if S>0:
            continue
        valid_pizzamap = valid_map(n, m, l, h, p)[k]
        if valid_pizzamap[i, j] == 1:
            slices.append(validSlices[k])
    return slices

def next_slice(n, m, i, j):
    if not (i>=0 and i < n): raise RuntimeError
    if not (j>=0 and j < m): raise RuntimeError
    if j < m - 1:
        j += 1
    else:
        j = 0
        i += 1
    if i>= n or j>= m:
        return (-1, -1)
    return (i, j)

def find_slices(n, m, l, h, p):
    listOfSlices = []
    coord_i = 0
    coord_j = 0
    idx = 1
    pizza_covered = np.zeros(p.shape, dtype=np.int)
    while (True):
        if pizza_covered[coord_i, coord_j] == 0:
            possible_cuts = get_slices(n, m, l, h, coord_i, coord_j, p)
            if (len(possible_cuts) != 0):
                slice_i, slice_j = possible_cuts[0]
                pizza_covered[coord_i:coord_i + slice_i, coord_j:coord_j + slice_j] = np.ones((slice_i, slice_j)) * idx
                idx += 1
                listOfSlices.append((coord_i, coord_j, coord_i+slice_i-1, coord_j+slice_j-1))
                coord_j += slice_j - 1

        coord_i, coord_j = next_slice(n, m, coord_i, coord_j)
        if coord_i == -1 and coord_j == -1:
            return listOfSlices, pizza_covered

def write_file(l, weight):
    nbSlices = len(l)
    f = open('output_'+weight+'.out', 'w')
    f.write(str(nbSlices) + '\n')
    for slc in l:
        f.write(str(int(slc[0]))+' '+str(int(slc[1]))+' '+str(int(slc[2]))+' '+str(int(slc[3]))+'\n')
    f.close()

def show_pizzaMap(n, l):
    cover_file = open('pizza_map.txt', 'w')
    for i in range(n):
        cover_file.write(''.join(map(str, list(l[i]))))
        cover_file.write('\n')
    cover_file.close()

def cuttingTheBigPizza(n, m, p, r):
    listMiniPizza = []
    nb_rows = n
    nb_cols = m
    nr = n%r
    mr = m%r
    for i in range(0, n, r):
        for j in range(0, m, r):
            listMiniPizza.append(p[i:i+r, j:j+r])
    return listMiniPizza


weight = "small"
r = 10
n, m, l, h, pizza_map = generatePizza(weight+".in")
#show_matrix(pizza_map)

#Cutting the problem into subproblems with lower dimension
if weight == "medium" or weight == "big":
    listOfPizza = cuttingTheBigPizza(n, m, pizza_map, r)
    print(len(listOfPizza))
    listOfSol = []
    listOfMaps = []
    for k in range(len(listOfPizza)):
        n_tmp, m_tmp = listOfPizza[k].shape
        print("Rate to end : ", str(round(100.*float(k/len(listOfPizza)), 1)))
        tmp1, tmp2 = find_slices(n_tmp, m_tmp, l, h, listOfPizza[k])
        listOfSol += tmp1
        listOfMaps += [tmp2]
    S = 0
    for k in range(len(listOfMaps)):
        S += np.sum(listOfMaps[k]>0)
    print(S)
    write_file(listOfSol, weight)
    #show_pizzaMap(n, mapOfPizza)

# Best maximum parts of the pizza covered :
if weight == "example" or weight == "small":
    solution, mapOfPizza = find_slices(n, m, l, h, pizza_map)
    print(np.sum(mapOfPizza > 0))
    # Writting the list of slices found :
    write_file(solution, weight)
    show_pizzaMap(n, mapOfPizza)
