#!/usr/bin/env python3

"""
This module implements three data structures that all solve the same problem:
given an array of integers, efficiently answer range-sum queries (sum of
elements between two indices) and support point updates (set an element to a
new value).

The three implementations make different time/space tradeoffs:

  Array          — the simplest approach: store the raw values. Updates are O(1)
                   but queries scan the whole interval in O(n).

  PrefixSumArray — precompute cumulative sums so queries become O(1), but every
                   update must shift all prefix sums to the right of the changed
                   element, costing O(n).

  FenwickTree    — a Binary Indexed Tree that achieves O(log n) for both update
                   and query by storing partial sums in a cleverly structured
                   array, using the lowest set bit of each index to determine
                   which range each cell covers.

Complexity comparison:
                 build       update    range_query
Array            O(1)        O(1)      O(n)
PrefixSumArray   O(n)        O(n)      O(1)
FenwickTree      O(n log n)  O(log n)  O(log n)

All implementations use 0-based indexing in their public API.
"""

from abc import ABC, abstractmethod


class RangeQueryBase(ABC):
   """Abstract base for point-update, range-sum data structures."""

   @abstractmethod
   def update(self, index: int, value: int) -> None:
      """Set the element at index to value."""
      pass

   @abstractmethod
   def range_query(self, left: int, right: int) -> int:
      """Return the sum of elements in the closed interval [left, right]."""
      pass


class Array(RangeQueryBase):
   """Baseline implementation backed by a plain list.

   update: O(1) — direct index assignment.
   range_query: O(n) — linear scan over the interval.
   """

   def __init__(self, array: list[int]) -> None:
      self.array = array[:]  # copy so the caller's list is not mutated
      self.size = len(self.array)

   def range_query(self, left: int, right: int) -> int:
      if (left > right) or (left < 0 or right >= self.size):
         raise RuntimeError(
            f"Invalid index size: {self.size}, left: {left}, right: {right}"
         )
      # Python slice is [left, right+1) so right is included.
      return sum(self.array[left : right + 1])

   def update(self, index: int, value: int) -> None:
      if not (0 <= index < self.size):
         raise RuntimeError(f"Invalid index size: {self.size}, index: {index}")
      self.array[index] = value


class PrefixSumArray(RangeQueryBase):
   """Range-sum via a stored prefix-sum array.

   self.array[i] holds the sum of the original elements at indices 0..i.
   For example, given [3, 1, 4, 1] the stored array is [3, 4, 8, 9].

   update: O(n) — every prefix sum from index onward must be shifted.
   range_query: O(1) — single subtraction of two stored prefix sums.
   """

   def __init__(self, array: list[int]) -> None:
      self.size = len(array)
      self.array = [0] * self.size

      # Build prefix sums: self.array[i] = array[0] + ... + array[i].
      total = 0
      for index, value in enumerate(array):
         total += value
         self.array[index] = total

   def range_query(self, left: int, right: int) -> int:
      if (left > right) or (left < 0 or right >= self.size):
         raise RuntimeError(
            f"Invalid index size: {self.size}, left: {left}, right: {right}"
         )
      # sum[left..right] = prefix[right] - prefix[left-1].
      # When left == 0 there is no prefix[left-1], so subtract 0 instead.
      return self.array[right] - (self.array[left - 1] if left > 0 else 0)

   def update(self, index: int, value: int) -> None:
      # Compute the change between the new value and the current value at index.
      # range_query(index, index) recovers the original value in O(1).
      diff = value - self.range_query(index, index)

      # Every stored prefix sum at index or beyond includes the changed element,
      # so each must be shifted by diff.
      for i in range(index, len(self.array)):
         self.array[i] += diff


class FenwickTree(RangeQueryBase):
   """Binary Indexed Tree (Fenwick Tree) for efficient point updates and prefix sums.

   Core idea: self.tree[i] does not store a single element — it stores the sum
   of a block of consecutive elements. The block length is exactly the value of
   the lowest set bit of i (written i & -i, or _lowbit(i)).

   Examples with an 8-element array (1-indexed):
     i=1 (001): covers 1 element  → tree[1] = a[1]
     i=2 (010): covers 2 elements → tree[2] = a[1]+a[2]
     i=4 (100): covers 4 elements → tree[4] = a[1]+a[2]+a[3]+a[4]
     i=6 (110): covers 2 elements → tree[6] = a[5]+a[6]

   Prefix query (sum of a[1..i]):
     Start at i, add tree[i], then move to i - lowbit(i) and repeat until 0.
     Each step strips the lowest set bit, visiting O(log n) nodes.

   Point update (add delta to a[i]):
     Start at i, add delta to tree[i], then move to i + lowbit(i) and repeat
     until past the end. Each step sets the next lowest bit, visiting O(log n)
     nodes that cover a[i] in their range.

   update: O(log n).
   range_query: O(log n) — two prefix queries.
   """

   def __init__(self, array: list[int]) -> None:
      self.size = len(array)
      # 1-indexed: index 0 is unused, so allocate size + 1 slots.
      self.tree = [0] * (self.size + 1)
      self.build(array)

   def _lowbit(self, num: int) -> int:
      """Return the value of the lowest set bit of num (num & -num).

      In two's complement, -num flips all bits then adds 1, so the result
      isolates exactly the rightmost 1-bit. E.g. _lowbit(6) = _lowbit(110₂) = 2.
      """
      return num & (-num)

   def update(self, index: int, value: int) -> None:
      """Set element at 0-based index to value and propagate the delta up the tree."""
      if not (0 <= index < self.size):
         raise RuntimeError(f"Invalid index size: {self.size}, index: {index}")

      # Convert to 1-based index used internally.
      tree_index = index + 1

      # Compute how much the element actually changed so we apply an additive
      # delta rather than overwriting tree cells (which store partial sums).
      delta = value - self.range_query(index, index)

      # Walk up: each ancestor whose range covers this position is found by
      # adding the lowest set bit. Stop when we exceed the array bounds.
      while tree_index <= self.size:
         self.tree[tree_index] += delta
         tree_index += self._lowbit(tree_index)

   def build(self, array: list[int]) -> None:
      """Populate the tree from a plain array in O(n log n)."""
      for index, value in enumerate(array):
         self.update(index, value)

   def query(self, index: int) -> int:
      """Return the prefix sum of elements at 0-based indices 0..index."""
      # Convert to 1-based index used internally.
      tree_index = index + 1
      total = 0

      # Walk down: strip the lowest set bit each step to visit only the nodes
      # whose ranges tile the prefix [1..tree_index] without overlap.
      while tree_index > 0:
         total += self.tree[tree_index]
         tree_index -= self._lowbit(tree_index)
      return total

   def range_query(self, left: int, right: int) -> int:
      """Return the sum of elements in the closed interval [left, right]."""
      if (left > right) or (left < 0 or right >= self.size):
         raise RuntimeError(
            f"Invalid index size: {self.size}, left: {left}, right: {right}"
         )
      # sum[left..right] = prefix[right] - prefix[left-1].
      # When left == 0 there is no prefix[left-1], so subtract 0 instead.
      return self.query(right) - (self.query(left - 1) if left > 0 else 0)


def main():
   data = [3, 1, 4, 1, 5, 9, 2, 6]
   impls: list[RangeQueryBase] = [Array(data), PrefixSumArray(data), FenwickTree(data)]

   print("Range queries on", data)
   for left, right in [(0, 0), (0, 3), (2, 5), (0, 7)]:
      results = [impl.range_query(left, right) for impl in impls]
      assert len(set(results)) == 1, f"Mismatch [{left},{right}]: {results}"
      print(f"  [{left},{right}] = {results[0]}")

   # Update index 3 to value 10, re-check
   for impl in impls:
      impl.update(3, 10)
   print("After update(3, 10):")
   for left, right in [(0, 3), (3, 3), (2, 5)]:
      results = [impl.range_query(left, right) for impl in impls]
      assert len(set(results)) == 1, f"Mismatch [{left},{right}]: {results}"
      print(f"  [{left},{right}] = {results[0]}")


if __name__ == "__main__":
   main()
