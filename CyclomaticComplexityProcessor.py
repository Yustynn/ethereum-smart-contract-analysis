from slither import Slither
from slither.utils.code_complexity import compute_cyclomatic_complexity
from Processor import Processor

from dataclasses import dataclass
from statistics import mean, median

@dataclass
class CyclomaticComplexityResult:
  total: int
  mean: float
  median: float
  num_functions: int

class CyclomaticComplexityProcessor(Processor):
  @staticmethod
  def run(path: str) -> CyclomaticComplexityResult:
    """Given code path, return cyclomatic complexity statistics."""

    functions = []
    for c in Slither(path).contracts:
      functions += c.functions

    ccs = [compute_cyclomatic_complexity(f) for f in functions]

    return CyclomaticComplexityResult(
      total = sum(ccs) + len(ccs),
      mean = mean(ccs),
      median = median(ccs),
      num_functions = len(ccs),
    )
    