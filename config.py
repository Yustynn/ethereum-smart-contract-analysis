from dataclasses import dataclass, field
from typing import List

ROOT_DIR = 'projects'
REPO_DIR = 'project-repos'
DATASET_CSV_OUTPUT_PATH = './output/results.csv'

@dataclass
class ProjectConfig:
  name: str
  repo_urls: List[str]
  exclude_dirs: List[str] = field(default_factory=list)

project_configs = [
  ProjectConfig(
    name='dai',
    repo_urls=[
      'https://github.com/makerdao/dss-cdp-manager/',
      'https://github.com/makerdao/dss-flash/',
      'https://github.com/dapphub/ds-pause',
      'https://github.com/makerdao/osm.git',
      'https://github.com/makerdao/esm/',
      'https://github.com/makerdao/median',
      'https://github.com/dapphub/ds-chief/',
      'https://github.com/dapphub/ds-spell/',
      'https://github.com/makerdao/dss.git',
      'https://github.com/makerdao/dss-proxy-actions',
      'https://github.com/makerdao/dsr-manager/',
      'https://github.com/dapphub/ds-token',
      'https://github.com/makerdao/vote-proxy/',
    ]
  ),
]

# config = {
#     '0x': {
#         'dir': './0x/protocol/contracts',
#     },
#     'aave': {
#         'dir': './aave-v3-core/contracts',
#     },
#     'compound': {
#         'dir': 'compound/compound-protocol/contracts',
#     },
#     'dai': {
#         'dir': './dai/by-module',
#     },
#     'synthetix': {
#         'dir': './synthetix/synthetix/contracts',
#         'exclude_paths': [
#             './legacy',
#             './test-helpers',
#         ]
#     },
#     'uniswap': {
#         'dir': 'uniswap/v3-core/contracts',
#         'exclude_paths': ['./test'],
#     },
# }
