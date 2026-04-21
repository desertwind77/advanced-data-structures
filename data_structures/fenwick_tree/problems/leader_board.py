#!/usr/bin/env python3
# 2574. Design a Contest Leaderboard
#
# Design a leaderboard for an online coding contest with up to 1000
# participants. Each participant is identified by a unique name. Scores are
# non-negative integers bounded by MAX_SCORE.
#
# Implement the ContestLeaderboard class:
#
#   ContestLeaderboard(max_score)
#     Initializes the leaderboard. All participants start with no score.
#
#   update_score(participant, new_score) -> None
#     Sets participant's score to new_score. If the participant already has a
#     score, the old score is replaced.
#
#   count_at_most(score) -> int
#     Returns the number of participants whose score is less than or equal to
#     score.
#
#   count_score_range(low, high) -> int
#     Returns the number of participants whose score is in the closed interval
#     [low, high].
#
#   percentile(participant) -> float
#     Returns the percentage of participants who have a strictly lower score
#     than participant, rounded to one decimal place.
#
# Constraints:
#   - 1 <= max_score <= 10^5
#   - 0 <= new_score <= max_score
#   - At most 10^4 calls will be made to each method.
#
# Follow-up: Could you achieve O(log MAX_SCORE) per call for all operations?

from data_structures.fenwick_tree import FenwickTree


class ContestLeaderboard:
   def __init__(self, max_score: int = 100) -> None:
      # Key insight: instead of a tree over participant values, build a tree
      # over a frequency array indexed by score. freq[s] = number of
      # participants currently holding score s. This turns range-count queries
      # ("how many scores ≤ X?") into prefix-sum queries — exactly what a
      # Fenwick tree does in O(log MAX_SCORE).
      array: list[int] = [0] * max_score
      self.max_score = max_score
      self.ft = FenwickTree(array)
      # Tracks each participant's current score so we can find their old bucket
      # on an update without scanning the whole tree.
      self.scores = {}

   def update_score(self, participant: str, new_score: int) -> None:
      if new_score > self.max_score:
         raise RuntimeError(
            f"Invalid score: {new_score}, max score allowed: {self.max_score}"
         )
      # Remove from the old bucket only if the participant was already tracked.
      # Defaulting to 0 for unknown participants would corrupt the score-0
      # bucket if anyone legitimately holds that score.
      if participant in self.scores:
         old_score = self.scores.get(participant)
         old_score_count = self.ft.range_query(old_score, old_score)
         if old_score_count > 0:
            # FenwickTree.update sets (not adds), so pass the new frequency.
            self.ft.update(old_score, old_score_count - 1)

      self.scores[participant] = new_score
      new_score_count = self.ft.range_query(new_score, new_score)
      self.ft.update(new_score, new_score_count + 1)

   def count_at_most(self, score: int) -> int:
      # Prefix sum over freq[0..score] = number of participants with score ≤ X.
      return self.ft.query(score)

   def count_score_range(self, low: int, high: int) -> int:
      # prefix[high] - prefix[low-1] = sum of freq[low..high].
      return self.ft.range_query(low, high)

   def percentile(self, participant: str) -> float:
      score = self.scores[participant]
      # Count participants strictly below this score; score 0 has nobody below.
      below = self.ft.query(score - 1) if score > 0 else 0
      return round(below / len(self.scores) * 100, 1)


def main() -> None:
   lb = ContestLeaderboard(max_score=100)

   # --- initial registrations ---
   lb.update_score("alice", 85)
   lb.update_score("bob", 90)
   lb.update_score("carol", 75)
   lb.update_score("dave", 90)
   lb.update_score("eve", 85)
   # freq: {75:1, 85:2, 90:2}

   assert lb.count_at_most(74) == 0
   assert lb.count_at_most(75) == 1,  "only carol"
   assert lb.count_at_most(85) == 3,  "carol + alice + eve"
   assert lb.count_at_most(90) == 5,  "all five"

   assert lb.count_score_range(85, 90) == 4, "alice, bob, dave, eve"
   assert lb.count_score_range(75, 75) == 1, "carol only"
   assert lb.count_score_range(80, 84) == 0, "nobody in this band"

   assert lb.percentile("carol") == 0.0,  "nobody below 75"
   assert lb.percentile("alice") == 20.0, "1 of 5 below 85"
   assert lb.percentile("bob")   == 60.0, "3 of 5 below 90"
   assert lb.percentile("dave")  == 60.0, "same score as bob"

   # --- update carol 75 → 92 ---
   lb.update_score("carol", 92)
   # freq: {75:0, 85:2, 90:2, 92:1}

   assert lb.count_at_most(75) == 0, "carol left score-75 bucket"
   assert lb.count_at_most(85) == 2, "alice + eve"
   assert lb.count_at_most(90) == 4, "alice, eve, bob, dave"
   assert lb.count_at_most(92) == 5, "all five again"

   assert lb.count_score_range(75, 75) == 0
   assert lb.count_score_range(85, 92) == 5, "alice, eve, bob, dave, carol"

   assert lb.percentile("alice") == 0.0,  "nobody below 85 anymore"
   assert lb.percentile("bob")   == 40.0, "2 of 5 below 90 (alice, eve)"
   assert lb.percentile("carol") == 80.0, "4 of 5 below 92"

   # --- edge case: score at index 0 ---
   lb2 = ContestLeaderboard(max_score=10)
   lb2.update_score("zero", 0)
   lb2.update_score("one", 1)

   assert lb2.count_at_most(0) == 1
   assert lb2.count_score_range(0, 1) == 2
   assert lb2.percentile("zero") == 0.0,  "nobody below 0"
   assert lb2.percentile("one")  == 50.0, "1 of 2 below score 1"

   print("All assertions passed.")


if __name__ == "__main__":
   main()
