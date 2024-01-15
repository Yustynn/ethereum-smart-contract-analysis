from dataclasses import dataclass
from abc import ABC, abstractmethod
import csv
from typing import Any, List, Tuple
import logging

logging.basicConfig(level=logging.DEBUG)

STAR = '*'
INDENT = '   '

@dataclass
class Role:
  name: str
  description: str


@dataclass
class Entry:
  name: str
  description: str
  category: str
  roles: List[Role]
  primary_blockchain: str


class Extractor(ABC):
  start_format: str

  def __init__(self):
    self.logger = logging.getLogger(type(self).__name__)

  @abstractmethod
  def _extract(self, lines: List[str]) -> Tuple[Any, List[str]]:
    pass

  def extract(self, lines: List[str]) -> Tuple[Any, List[str]]:
    self.logger.debug(f'Running with {len(lines)} remaining.')

    # remove blank lines
    while lines[0].strip() == '':
      lines = lines[1:]

    # validate
    line = lines[0].strip()
    assert line.startswith(self.start_format), f'[{type(self).__name__}] Line should start with ({self.start_format}). Line: ({line})'

    return self._extract(lines)

class NameExtractor(Extractor):
  start_format = f'{STAR} '

  def _extract(self, lines: List[str]) -> Tuple[Any, List[str]]:
    name = lines[0].strip().replace(self.start_format, '')

    return name, lines[1:]
    

class DescriptionExtractor(Extractor):
  start_format = f'{STAR} Brief Description: '

  def _extract(self, lines: List[str]) -> Tuple[Any, List[str]]:
    description = lines[0].strip().replace(self.start_format, '')

    return description, lines[1:]
    

class CategoryExtractor(Extractor):
  start_format = f'{STAR} Classification: '

  def _extract(self, lines: List[str]) -> Tuple[Any, List[str]]:
    category = lines[0].strip().replace(self.start_format, '')

    return category, lines[1:]


class PrimaryBlockchainExtractor(Extractor):
  start_format = f'{STAR} Primary Blockchain: '

  def _extract(self, lines: List[str]) -> Tuple[Any, List[str]]:
    primary_blockchain = lines[0].strip().replace(self.start_format, '')

    return primary_blockchain, lines[1:]
    

class RolesExtractor(Extractor):
  start_format = f'{STAR} User Roles:'

  def _extract(self, lines: List[str]) -> Tuple[Any, List[str]]:
    lines = lines[1:]
    roles: List[Role] = []

    while not lines[0].strip().startswith(PrimaryBlockchainExtractor.start_format):
      line = lines[0]
      lines = lines[1:]

      name, description = [s.strip() for s in line.replace(STAR,'').split(':', 1)]

      roles.append(Role(name, description))

    return roles, lines


EXTRACTOR_ORDERING = [
  NameExtractor,
  DescriptionExtractor,
  CategoryExtractor,
  RolesExtractor,
  PrimaryBlockchainExtractor
]

# load data
DATA_PATH = '../data/chatgpt_20240115.txt'
with open(DATA_PATH) as f:
  lines = f.readlines()

# preprocess
lines = lines[1:]
lines[0] = lines[0].replace(f'{STAR} ', '', 1)

entries: List[Entry] = []
while lines:
  infos = []
  for extractor in EXTRACTOR_ORDERING:
    info, lines = extractor().extract(lines)
    infos.append(info)

  entries.append(Entry(*infos))

# to csv
OUTPUT_PATH = '../data/project-qual-info.csv'
HEADERS = [
  'Name',
  'Category',
  'Num Roles',
  'Primary Blockchain',
  'Roles',
  'Description',
]

with open(OUTPUT_PATH, 'w') as f:
  writer = csv.writer(f)
  writer.writerow(HEADERS)
  for entry in entries:
    writer.writerow([
      entry.name,
      entry.category,
      len(entry.roles),
      entry.primary_blockchain,
      ', '.join([r.name for r in entry.roles]),
      entry.description
    ])