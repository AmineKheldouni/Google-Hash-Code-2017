
import numpy as np
import pickle
import os
import sys
import cvxpy as cvx
import math as m
from utils import *


list_valeurs = cvx.Parameter(5)
list_valeurs.value = [1,2,3,4,5]
list_poids = cvx.Parameter(5)
list_poids.value = [5,4,8,2,1]
weight = cvx.Parameter(1, sign="Positive")
weight.value = 100
X = cvx.Bool(5)

objective = cvx.Maximize(cvx.sum_entries(X.T*list_valeurs))


constrains = [ ]

constrains.append(cvx.sum_entries(X.T*list_poids) <= weight)

prob = cvx.Problem(objective, constrains)
print("status: ", prob.status)
print("Solution : ", prob.value)
print(" X_i : ", X.value)
