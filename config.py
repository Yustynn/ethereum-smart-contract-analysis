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
    name='DAI',
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
    name='AAVE',
    repo_urls=['https://github.com/aave/aave-v3-core']
  ),

  ProjectConfig(
    name='USD Tether',
    repo_urls=['https://github.com/tethercoin/USDT']
  ),

  ProjectConfig(
    name='Polygon',
    repo_urls=['https://github.com/maticnetwork/contracts']
  ),

  ProjectConfig(
    name='USDC',
    repo_urls=['https://github.com/circlefin/stablecoin-evm']
  ),

  ProjectConfig(
    name='Shiba Inu',
    repo_urls=['https://github.com/shibaswaparmy/contracts']
  ),

  ProjectConfig(
    name='Toncoin',
    repo_urls=['https://github.com/ton-blockchain/bridge-solidity']
  ),

  ProjectConfig(
    name='Uniswap',
    repo_urls=['https://github.com/Uniswap/v3-core']
  ),

  ProjectConfig(
    name='Lido DAO',
    repo_urls=['https://github.com/lidofinance/lido-dao']
  ),

  ProjectConfig(
    name='Immutable',
    repo_urls=['https://github.com/immutable/contracts']
  ),

  ProjectConfig(
    name='Mantle',
    repo_urls=['https://github.com/mantlenetworkio/mantle']
  ),

  ProjectConfig(
    name='Cronos',
    repo_urls=['https://github.com/crypto-org-chain/cronos']
  ),
]