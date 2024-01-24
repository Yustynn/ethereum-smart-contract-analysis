from glob import glob
import os
import logging

from CyclomaticComplexityProcessor import CyclomaticComplexityProcessor
from LOCProcessor import LOCProcessor

logging.basicConfig(level=logging.INFO)
# lg = logging.getLogger('Main')

ROOT_DIR = 'projects'

config = {
    '0x': {
        'dir': './0x/protocol/contracts',
    },
    'aave': {
        'dir': './aave-v3-core/contracts',
    },
    'compound': {
        'dir': 'compound/compound-protocol/contracts',
    },
    'dai': {
        'dir': './dai/by-module',
    },
    'synthetix': {
        'dir': './synthetix/synthetix/contracts',
        'exclude_paths': [
            './legacy',
            './test-helpers',
        ]
    },
    'uniswap': {
        'dir': 'uniswap/v3-core/contracts',
        'exclude_paths': ['./test'],
    },
}

name = 'aave'
cfg = config[name]

# for name, cfg in config.items():
for name, cfg in [[name, cfg]]:
    print(name)

    folder = os.path.join(ROOT_DIR, cfg['dir'])
    EXCLUDE_PATHS = cfg['exclude_paths'] if 'exclude_paths' in cfg else []

    paths = glob(os.path.join(folder, '*.sol')) + glob(os.path.join(folder, '**/*.sol'), recursive=True)
    paths = [
        p for p in paths
        if not any(p.startswith(os.path.join(folder, ep)) for ep in EXCLUDE_PATHS) # illegal path
        and not p.endswith('.t.sol') # exclude tests
    ]
    print(f'{len(paths)} solidity files.')

    for path in paths:
      print(f'---Processing {path}')
      loc = LOCProcessor.run(path)
      cc = CyclomaticComplexityProcessor.run(path)
      print(f'{loc} lines of non-comment code.')
      print(f'cc: {cc}')
      print()

    

