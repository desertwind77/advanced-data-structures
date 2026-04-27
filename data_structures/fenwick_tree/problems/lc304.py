#!/usr/bin/env python3
# https://leetcode.com/problems/range-sum-query-2d-immutable/description/
#
# 304. Range Sum Query 2D - Immutable
# Given a 2D matrix matrix, handle multiple queries of the following type:
#
# Calculate the sum of the elements of matrix inside the rectangle defined by
# its upper left corner (row1, col1) and lower right corner (row2, col2).
#
# Implement the NumMatrix class:
#
# NumMatrix(int[][] matrix) :
#     Initializes the object with the integer matrix matrix.
#
# int sumRegion(int row1, int col1, int row2, int col2)
#     Returns the sum of the elements of matrix inside the rectangle defined by
#     its upper left corner (row1, col1) and lower right corner (row2, col2).
#
# You must design an algorithm where sumRegion works on O(1) time complexity.
#
# Input
# ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
# [[[[3, 0, 1, 4, 2],
#    [5, 6, 3, 2, 1],
#    [1, 2, 0, 1, 5],
#    [4, 1, 0, 1, 7],
#    [1, 0, 3, 0, 5]]],
#  [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
#
# Output
# [null, 8, 11, 12]
#
# Explanation
# NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
# numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e sum of the red rectangle)
# numMatrix.sumRegion(1, 1, 2, 2); // return 11 (i.e sum of the green rectangle)
# numMatrix.sumRegion(1, 2, 2, 4); // return 12 (i.e sum of the blue rectangle)


class NumMatrix:
   def __init__(self, matrix: list[list[int]]) -> None:
      if not matrix:
         return

      rows, cols = len(matrix), len(matrix[0])
      self.rows, self.cols = rows + 1, cols + 1
      self.tree = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

      for r in range(rows):
         for c in range(cols):
            self.update(r + 1, c + 1, matrix[r][c])

   def _low_bit(self, num: int) -> int:
      return num & (-num)

   def update(self, row: int, col: int, value: int) -> None:
      while col < self.cols:
         cur_row = row
         while cur_row < self.rows:
            self.tree[cur_row][col] += value
            cur_row += self._low_bit(cur_row)
         col += self._low_bit(col)

   def print(self):
      for r in range(self.rows):
         for c in range(self.cols):
            print(f"{self.tree[r][c]:3}", end="")
         print()

   def query(self, row: int, col: int) -> int:
      # Change from 0-based index to 1-based index
      row, col = row + 1, col + 1

      total = 0
      while row > 0 or col > 0:
         next_col = col - self._low_bit(col)
         next_row = row - self._low_bit(row)
         total += (
            self.tree[row][col] + self.tree[next_row][col] + self.tree[row][next_col]
         )
         row, col = next_row, next_col
      return total

   def sumRegion(self, x0: int, y0: int, x1: int, y1: int) -> int:
      if x0 > x1 or y0 > y1:
         raise ValueError(f"Invalid region ({x0}, {y0}) and ({x1}, {y1})")
      area1 = self.query(x1, y1)
      area2 = self.query(x0 - 1, y1)
      area3 = self.query(x1, y0 - 1)
      area4 = self.query(x0 - 1, y0 - 1)
      return area1 - area2 - area3 + area4


def main():
   matrix = [
      [3, 0, 1, 4, 2],
      [5, 6, 3, 2, 1],
      [1, 2, 0, 1, 5],
      [4, 1, 0, 1, 7],
      [1, 0, 3, 0, 5],
   ]
   tree = NumMatrix(matrix)
   assert tree.sumRegion(2, 1, 4, 3) == 8
   assert tree.sumRegion(1, 1, 2, 2) == 11
   assert tree.sumRegion(1, 2, 2, 4) == 12


if __name__ == "__main__":
   main()
