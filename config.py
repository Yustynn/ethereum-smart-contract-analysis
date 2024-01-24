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
