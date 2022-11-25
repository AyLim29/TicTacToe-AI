import string

X = 1
O = -1
DRAW = 0
NO_WIN = 2

# HORIZONTAL = [[(i, j) for j in range(3)] for i in range(3)]
# VERTICAL = [[(j, i) for j in range(3)] for i in range(3)]
# DIAGONAL = [[(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]]

# 0 -> 8
HORIZONTAL = [[j + i for i in range(0,3)] for j in range(0,7,3)]
VERTICAL = [[j + i for i in range(0,7,3)] for j in range(0,3)]
DIAGONAL = [[0, 4, 8], [2, 4, 6]]

#  0   1   2
#  3   4   5
#  6   7   8