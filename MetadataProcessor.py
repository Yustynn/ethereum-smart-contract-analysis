from slither import Slither
from Processor import Processor

from dataclasses import dataclass
from utils import set_solc_version

@dataclass
class MetadataResults:
  num_files: int
  num_contracts: int
  num_functions: int
  num_modifiers: int

  def __add__(self, other):
    return self.__class__(
      num_files=self.num_files + other.num_files,
      num_contracts=self.num_contracts + other.num_contracts,
      num_functions=self.num_functions + other.num_functions,
      num_modifiers=self.num_functions + other.num_functions,
    )

class MetadataProcessor(Processor):
  @staticmethod
  def run(path: str) -> MetadataResults:
    set_solc_version(path)
    s = Slither(path)

    num_functions = 0
    num_modifiers = 0
    for c in s.contracts:
      num_functions += len(c.functions)
      num_modifiers += len(c.modifiers)

    return MetadataResults(
      num_files=1,
      num_contracts=len(s.contracts),
      num_functions=num_functions,
      num_modifiers=num_modifiers
    )

      
     
