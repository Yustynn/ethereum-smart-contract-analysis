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
    name='Chainlink',
    repo_urls=['https://github.com/smartcontractkit/chainlink']
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

  ProjectConfig(
    name='The Graph',
    repo_urls=['https://github.com/graphprotocol/contracts']
  ),

  ProjectConfig(
    name='Render',
    repo_urls=['https://github.com/rndr-network/Token-Audit']
  ),

  ProjectConfig(
    name='Synthetix',
    repo_urls=['https://github.com/Synthetixio/synthetix']
  ),

  ProjectConfig(
    name='Fantom',
    repo_urls=[
      # In general, seem to be lots of redundant/abandoned stuff
      'https://github.com/Fantom-foundation/Artion-Contracts',
      'https://github.com/Fantom-foundation/opera-sfc',
      # 'https://github.com/Fantom-foundation/qewa', # unclear what this is, excluding.
      'https://github.com/Fantom-foundation/FtmStableCoin',
      'https://github.com/Fantom-foundation/FNS-SCs', # i don't think this is used. it's an ENS clone.
      'https://github.com/Fantom-foundation/fns-contracts/tree/master', # unclear about whether this is used. I suspect no, in favor of other repos.
      'https://github.com/Fantom-foundation/Fantom-CrossChain-Bridge',
      'https://github.com/Fantom-foundation/Fantom-wFTM',
      'https://github.com/Fantom-foundation/Fantom-Contract-Validation',
      'https://github.com/Fantom-foundation/Fantom-Uniswap', # seems deployed, acc to README
      'https://github.com/Fantom-foundation/keep3r.network', # idk what this is, seems abandoned
      'https://github.com/Fantom-foundation/Fantom-Oracle-Pricefeed',
      'https://github.com/Fantom-foundation/Fantom-FLend',
      'https://github.com/Fantom-foundation/data-hashing-authentication',
      'https://github.com/Fantom-foundation/Fantom-DeFi', # possibly not used
      'https://github.com/Fantom-foundation/Fantom-Fusd'
    ]
  ),

  ProjectConfig(
    name='The Sandbox',
    repo_urls=['https://github.com/thesandboxgame/sandbox-smart-contracts']
  ),

  ProjectConfig(
    name='Axie Infinity',
    repo_urls=[
      'https://github.com/axieinfinity/public-smart-contracts',
      # here's ronin stuff. Not 100% on including it
      'https://github.com/axieinfinity/ronin-bridge-contracts',
      'https://github.com/axieinfinity/rns-contracts',
      'https://github.com/axieinfinity/ronin-dpos-contracts',
]),
]