import logging
import os
import re
import sys

from typing import List, Optional
from glob import glob

import solc_select_api
from config import ROOT_DIR

lg = logging.getLogger('utils')
lg.setLevel(logging.INFO)


def parse_version(path: str) -> Optional[str]:
  PATTERN_VERSION = r"\d+\.\d+\.\d+"

  with open(path) as f:
    lines = f.readlines()

  for l in lines:
    if not 'pragma' in l:
      continue
    matches = re.findall(PATTERN_VERSION, l)

    if len(matches) > 0:
      version = matches[0]
      lg.debug(f'Version {version} found in line: {l}')
      return version
  
  lg.info(f'{path}: No version pragma found')

def set_appropriate_solc_version(path: str) -> None:
    # set solc version
    version = parse_version(path)
    if version is None:
      solc_select_api.use_latest()
    else:
      solc_select_api.use_version(version)

def cfg_to_paths(cfg) -> List[str]:
    folder = os.path.join(ROOT_DIR, cfg['dir'])
    exclude_paths = cfg['exclude_paths'] if 'exclude_paths' in cfg else []

    paths = glob(os.path.join(folder, '*.sol')) + glob(os.path.join(folder, '**/*.sol'), recursive=True)
    paths = [
        p for p in paths
        if not any(p.startswith(os.path.join(folder, ep)) for ep in exclude_paths) # illegal path
        and not p.endswith('.t.sol') # exclude tests
    ]

    return paths
