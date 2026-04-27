#!/usr/bin/env python3

from lc304 import NumMatrix
from fenwick_tree import FenwickTree

# https://leetcode.com/problems/range-sum-query-2d-mutable/description/
#
# 308. Range Sum Query 2D - Mutable
#
# Given a 2D matrix matrix, handle multiple queries of the following types:
# 1) Update the value of a cell in matrix.
# 2) Calculate the sum of the elements of matrix inside the rectangle defined
#    by its upper left corner (row1, col1) and lower right corner (row2, col2).
#
# Implement the NumMatrix class:
# - NumMatrix(int[][] matrix)
#     Initializes the object with the integer matrix matrix.
# - void update(int row, int col, int val)
#     Updates the value of matrix[row][col] to be val.
# - int sumRegion(int row1, int col1, int row2, int col2)
#     Returns the sum of the elements of matrix inside the rectangle defined by
#     its upper left corner (row1, col1) and lower right corner (row2, col2).
#
# Example 1:
#
# Input
# ["NumMatrix", "sumRegion", "update", "sumRegion"]
# [[[[3, 0, 1, 4, 2],
#    [5, 6, 3, 2, 1],
#    [1, 2, 0, 1, 5],
#    [4, 1, 0, 1, 7],
#    [1, 0, 3, 0, 5]]],
#  [2, 1, 4, 3], [3, 2, 2], [2, 1, 4, 3]]
#
# Output
# [null, 8, null, 10]
#
# Explanation
# NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
# numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e. sum of the left red rectangle)
# numMatrix.update(3, 2, 2);       // matrix changes from left image to right image
# numMatrix.sumRegion(2, 1, 4, 3); // return 10 (i.e. sum of the right red rectangle)
#
# Constraints:
#     m == matrix.length
#     n == matrix[i].length
#     1 <= m, n <= 200
#     -1000 <= matrix[i][j] <= 1000
#     0 <= row < m
#     0 <= col < n
#     -1000 <= val <= 1000
#     0 <= row1 <= row2 < m
#     0 <= col1 <= col2 < n
#     At most 5000 calls will be made to sumRegion and update.


def test1():
   matrix = [
      [3, 0, 1, 4, 2],
      [5, 6, 3, 2, 1],
      [1, 2, 0, 1, 5],
      [4, 1, 0, 1, 7],
      [1, 0, 3, 0, 5],
   ]

   fenwickTree = NumMatrix(matrix)
   assert fenwickTree.sumRegion(2, 1, 4, 3) == 8
   fenwickTree.update(3, 2, 2)
   assert fenwickTree.sumRegion(2, 1, 4, 3) == 10


def test2():
   matrix = [[1]]
   fenwickTree = NumMatrix(matrix)
   assert fenwickTree.sumRegion(0, 0, 0, 0) == 1
   fenwickTree.update(0, 0, -1)
   assert fenwickTree.sumRegion(0, 0, 0, 0) == -1


def test3():
   matrix = [[0, -5, 9, 1, -8, 5, 8, 1, 1, 5]]
   fenwickTree = NumMatrix(matrix)
   assert fenwickTree.sumRegion(0, 5, 0, 9) == 20
   fenwickTree.update(0, 3, -1)
   fenwickTree.sumRegion(0, 3, 0, 6) == 4
   fenwickTree.update(0, 1, 6)
   fenwickTree.update(0, 9, 3)
   fenwickTree.update(0, 7, 2)
   assert fenwickTree.sumRegion(0, 4, 0, 7) == 7
   fenwickTree.update(0, 4, -5)
   assert fenwickTree.sumRegion(0, 8, 0, 9) == 4
   fenwickTree.update(0, 7, 8)


def main():
   test1()
   test2()
   test3()


if __name__ == "__main__":
   main()
