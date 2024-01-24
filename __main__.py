import logging
from dataclasses import dataclass
from config import config
from typing import List

from CyclomaticComplexityProcessor import CyclomaticComplexityProcessor, CyclomaticComplexityResult
from MetadataProcessor import MetadataProcessor, MetadataResults

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('Main')

@dataclass
class Result:
   project_name: str
   cc: CyclomaticComplexityResult
   metadata: MetadataResults


name = 'aave'
cfg = config[name]

results: List[Result] = []

# for name, cfg in config.items():
for name, cfg in [[name, cfg]]:
    cc = CyclomaticComplexityProcessor.run_config(cfg)
    metadata = MetadataProcessor.run_config(cfg)
    print(metadata)

    results.append(Result(
      project_name = name,
      cc = cc,
      metadata = metadata
    ))

print(results[0])

