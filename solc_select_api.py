import re
from typing import List

import subprocess
import logging
import sys

lg = logging.getLogger('solc_select_api')
lg.setLevel(logging.INFO)


PATTERN_VERSION = r"\d+\.\d+\.\d+"

def sh(cmd: str) -> str:
  return subprocess.run(
    cmd,
    shell=True,
    text=True,
    capture_output=True
  ).stdout

def installed_versions() -> List[str]:
  raw = sh('solc-select versions')
  lines = raw.split('\n')

  versions = []
  for l in lines:
    matches = re.findall(PATTERN_VERSION, l)
    if len(matches) > 0:
      versions.append(matches[0])

  return versions

def current_version() -> str:
  raw = sh('solc-select versions')
  lines = raw.split('\n')

  for l in lines:
    if '(current' in l:
      return re.findall(PATTERN_VERSION, l)[0]

  raise Exception('No solc version currently set!')

def install_version(version: str) -> None:
  assert len(re.findall(PATTERN_VERSION, version)) == 1, f"Malformed version input: {version}"

  sh(f'solc-select install {version}')

def use_version(version: str) -> None:
  assert len(re.findall(PATTERN_VERSION, version)) == 1, f"Malformed version input: {version}"

  if not version in installed_versions():
    lg.info(f'v{version} not installed. Installing now...')
    install_version(version)

  if current_version() != version:
    sh(f'solc-select use {version}')
    lg.info(f'solc version set to {current_version()}')

def use_latest() -> None:
  if current_version != installed_versions()[0]:
    sh('solc-select use latest')
    lg.info(f'solc version set to {current_version()}')