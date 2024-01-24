import logging
from dataclasses import dataclass
from config import project_configs
from typing import List

from Project import Project
from processors.CyclomaticComplexityProcessor import CyclomaticComplexityProcessor, CyclomaticComplexityResult
from processors.MetadataProcessor import MetadataProcessor, MetadataResults

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('Main')

@dataclass
class Result:
   project_name: str
   cc: CyclomaticComplexityResult
   metadata: MetadataResults


results: List[Result] = []

# for name, cfg in config.items():
# for cfg in project_configs:
#     cc = CyclomaticComplexityProcessor.run_config(cfg)
#     metadata = MetadataProcessor.run_config(cfg)
#     print(metadata)

#     results.append(Result(
#       project_name = cfg.name,
#       cc = cc,
#       metadata = metadata
#     ))

# print(results[0])


p = Project(project_configs[0]).get_path_candidates()