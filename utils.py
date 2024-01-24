import solc_select_api
from typing import Optional

import logging
import sys
import re

lg = logging.getLogger('utils')
lg.setLevel(logging.INFO)
lg.addHandler( logging.StreamHandler(sys.stdout) )


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
      lg.info(f'Version {version} found in line: {l}')
      return version
  
  lg.info(f'{path}: No version pragma found')

def set_appropriate_solc_version(path: str) -> None:
    # set solc version
    version = parse_version(path)
    if version is None:
      solc_select_api.use_latest()
    else:
      solc_select_api.use_version(version)