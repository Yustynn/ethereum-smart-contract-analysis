import logging
from dataclasses import dataclass
from config import config
from typing import List

from CyclomaticComplexityProcessor import CyclomaticComplexityProcessor, CyclomaticComplexityResult
from LOCProcessor import LOCProcessor, LOCResult
from MetadataProcessor import MetadataProcessor, MetadataResults

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('Main')

@dataclass
class Result:
   project_name: str
   loc: LOCResult
   cc: CyclomaticComplexityResult
   metadata: MetadataResults


name = 'aave'
cfg = config[name]

results: List[Result] = []

# for name, cfg in config.items():
for name, cfg in [[name, cfg]]:
    loc = LOCProcessor.run_config(cfg)
    cc = CyclomaticComplexityProcessor.run_config(cfg)
    metadata = MetadataProcessor.run_config(cfg)

    results.append(Result(
      project_name = name,
      loc = loc,
      cc = cc,
      metadata = metadata
    ))

print(results[0])

