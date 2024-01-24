import logging
from dataclasses import dataclass
from config import project_configs
from typing import List

from Project import Project
from processors.CyclomaticComplexityProcessor import CyclomaticComplexityProcessor, CyclomaticComplexityResult
from processors.MetadataProcessor import MetadataProcessor, MetadataResult

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('Main')

@dataclass
class Result:
   project_name: str
   cc: CyclomaticComplexityResult
   metadata: MetadataResult


results: List[Result] = []


p = Project(project_configs[0])
cc = CyclomaticComplexityResult.neutral()
md = MetadataResult.neutral()
for path in p:
   cc += CyclomaticComplexityProcessor.run(path)
   md += MetadataProcessor.run(path)

result = Result(
   project_name=p.name,
   cc=cc,
   metadata=md
)

print(result)
print('\n\n\n')
print(p.slither_failures)