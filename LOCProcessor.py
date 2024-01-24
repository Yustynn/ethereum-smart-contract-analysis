from typing import List
from Processor import Processor
from dataclasses import dataclass

import statistics


@dataclass
class LOCResult:
    total: int
    mean_file: float
    median_file: float
    raw_by_file: List[int]

    @staticmethod
    def from_raw_by_file(raw_by_file: List[int]) -> 'LOCResult':
        return LOCResult(
            total=sum(raw_by_file),
            mean_file=statistics.mean(raw_by_file),
            median_file=statistics.median(raw_by_file),
            raw_by_file=raw_by_file,
        )
    
    def __add__(self, other) -> 'LOCResult':
        return self.__class__.from_raw_by_file(self.raw_by_file + other.raw_by_file)


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

def count_lines(path) -> int:
    with open(path) as f:
        lines = f.readlines()
    return len(remove_comments(lines))



class LOCProcessor(Processor):
    @staticmethod
    def run(path: str) -> LOCResult:
        """Count noncomment lines for a directory"""

        return LOCResult.from_raw_by_file([count_lines(path)])

