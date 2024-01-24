from dataclasses import dataclass, field
from typing import List

ROOT_DIR = 'projects'
REPO_DIR = 'project-repos'
DATASET_CSV_OUTPUT_PATH = './output/results.csv'
DATASET_DILL_OUTPUT_PATH = './output/results.dill' # better pickle

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

  ProjectConfig(
    name='aave',
    repo_urls=['https://github.com/aave/aave-v3-core']
  ),

  ProjectConfig(
    name='tether',
    repo_urls=['https://github.com/tethercoin/USDT']
  ),

  ProjectConfig(
    name='polygon',
    repo_urls=['https://github.com/maticnetwork/contracts']
  )
]