from typing import List
from Processor import Processor

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


class LOCProcessor(Processor):
    @staticmethod
    def run(path: str) -> int:
        """Count lines for a single path"""

        with open(path) as f:
            lines = f.readlines()
        return len(remove_comments(lines))

