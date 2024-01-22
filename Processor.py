from abc import abstractstaticmethod
from typing import Any

class Processor:
  @abstractstaticmethod
  def run(path: str) -> Any:
    pass

