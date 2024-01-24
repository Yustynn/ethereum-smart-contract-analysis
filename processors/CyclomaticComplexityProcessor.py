from slither import Slither
from slither.utils.code_complexity import compute_cyclomatic_complexity
from .Processor import Processor

from dataclasses import dataclass
from statistics import mean, median
from typing import List, Optional

@dataclass
class CyclomaticComplexityResult:
  total: int
  mean: float
  median: float
  num_functions: int
  raw: List[int]

  @staticmethod
  def from_ccs(ccs: List[int]) -> 'CyclomaticComplexityResult':
      return CyclomaticComplexityResult(
        total = sum(ccs),
        mean = mean(ccs),
        median = median(ccs),
        num_functions = len(ccs),
        raw = ccs,
      )

  def __add__(self, other):
    return self.__class__.from_ccs(self.raw + other.raw)

  @classmethod
  def neutral(cls):
    return cls(
      total = 0,
      mean = float('-inf'),
      median = float('-inf'),
      num_functions = 0,
      raw = [],
    )


class CyclomaticComplexityProcessor(Processor):
  @staticmethod
  def run(s: Slither) -> Optional[CyclomaticComplexityResult]:
    """Given code path, return cyclomatic complexity statistics."""

    # gather all functions
    functions = []
    for c in s.contracts:
      functions += c.functions

    if len(functions) == 0:
      return
    # retrieve cc for each function
    ccs = [compute_cyclomatic_complexity(f) for f in functions]

    # return statistics
    return CyclomaticComplexityResult(
      total = sum(ccs),
      mean = mean(ccs),
      median = median(ccs),
      num_functions = len(ccs),
      raw = ccs
    )