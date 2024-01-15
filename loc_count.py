from glob import glob
from typing import List
import os

config = {
    '0x': {
        'root_dir': './0x/protocol/contracts',
    },
    'aave': {
        'root_dir': './aave-v3-core/contracts',
    },
    'compound': {
        'root_dir': 'compound/compound-protocol/contracts',
    },
    'dai': {
        'root_dir': './dai/by-module',
    },
    'synthetix': {
        'root_dir': './synthetix/synthetix/contracts',
        'exclude_paths': [
            './legacy',
            './test-helpers',
        ]
    },
    'uniswap': {
        'root_dir': 'uniswap/v3-core/contracts',
        'exclude_paths': ['./test'],
    },
}


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

def count_lines(path: str) -> int:
    """Count lines for a single path"""

    with open(path) as f:
        lines = f.readlines()
    return len(remove_comments(lines))

for name, cfg in config.items():
    print(name)

    ROOT_DIR = cfg['root_dir']
    EXCLUDE_PATHS = cfg['exclude_paths'] if 'exclude_paths' in cfg else []

    paths = glob(os.path.join(ROOT_DIR, '*.sol')) + glob(os.path.join(ROOT_DIR, '**/*.sol'), recursive=True)
    paths = [
        p for p in paths
        if not any(p.startswith(os.path.join(ROOT_DIR, ep)) for ep in EXCLUDE_PATHS) # illegal path
        and not p.endswith('.t.sol') # exclude tests
    ]
    print(f'{len(paths)} solidity files.')

    loc = sum(count_lines(path) for path in paths)
    print(f'{loc} lines of non-comment code.')
    print()
