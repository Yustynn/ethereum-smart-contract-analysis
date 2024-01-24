import logging
from dataclasses import dataclass
from config import config
from typing import List

from CyclomaticComplexityProcessor import CyclomaticComplexityProcessor, CyclomaticComplexityResult
from LOCProcessor import LOCProcessor, LOCResult

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('Main')

@dataclass
class Result:
   project_name: str
   loc: LOCResult
  #  cc: CyclomaticComplexityResult


name = 'aave'
cfg = config[name]

results: List[Result] = []

# for name, cfg in config.items():
for name, cfg in [[name, cfg]]:
    loc = LOCProcessor.run_config(cfg)
    # cc = CyclomaticComplexityProcessor.run_config(cfg)

    results.append(Result(
      project_name = name,
      loc = loc,
      # cc = cc,
    ))

print(results)    

