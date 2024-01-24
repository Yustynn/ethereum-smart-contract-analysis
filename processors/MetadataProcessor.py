# loc excludes comments

import statistics

from dataclasses import dataclass
from slither import Slither
from typing import List

from utils import set_appropriate_solc_version
from .Processor import Processor
@dataclass
class MetadataResult:
  num_files: int
  num_contracts: int
  num_functions: int
  loc_total: int
  loc_mean_file: float
  loc_median_file: float
  loc_raw_by_file: List[int]


  def __add__(self, other):
    loc_raw_by_file = self.loc_raw_by_file + other.loc_raw_by_file

    return self.__class__(
      num_files=self.num_files + other.num_files,
      num_contracts=self.num_contracts + other.num_contracts,
      num_functions=self.num_functions + other.num_functions,
      loc_total=self.loc_total + other.loc_total,
      loc_mean_file=statistics.mean(loc_raw_by_file),
      loc_median_file=statistics.median(loc_raw_by_file),
      loc_raw_by_file=loc_raw_by_file,
    )

  @classmethod
  def neutral(cls):
    return cls(
      num_files=0,
      num_contracts=0,
      num_functions=0,
      loc_total=0,
      loc_mean_file=0,
      loc_median_file=0,
      loc_raw_by_file=[],
    )


def remove_comments(lines: List[str]) -> List[str]:
    """Remove single and multi-line comments

    Note: Doesn't handle case where multiline is embedded in multiline. Unlikely to occur.
    
    """

    result: List[str] = []

    is_multiline = False
    for line in lines:
        line = line.strip()

        # handle single line
        if line.startswith('//'):
            continue
        # handle multiline
        elif is_multiline:
            if line.startswith('*/'):
                is_multiline = False
            continue
        # handle multiline start
        elif line.startswith('/*'):
            is_multiline = True
            continue

        result.append(line)

    return result

def count_lines(s: Slither) -> int:
  src = list(s.source_code.values())[0]
  lines = src.split('\n')
  return len(remove_comments(lines))

class MetadataProcessor(Processor):
  @staticmethod
  def run(s: Slither) -> MetadataResult:
    loc = count_lines(s)

    return MetadataResult(
      num_files=1,
      num_contracts=len(s.contracts),
      num_functions=sum( len(c.functions) for c in s.contracts ),
      loc_total = loc,
      loc_mean_file = loc,
      loc_median_file = loc,
      loc_raw_by_file = [loc],
    )