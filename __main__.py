import logging
import pandas as pd
from dataclasses import dataclass
from config import DATASET_CSV_OUTPUT_PATH, DATASET_DILL_OUTPUT_PATH, project_configs
from typing import Dict, List, Union

import dill

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
  failures: Dict[str, str]
  
  def to_record(self) -> Dict[str, Union[float, int, str]]:
    assert self.cc.num_functions == self.metadata.num_functions, "Metadata and CC show different num functions"

    return {
      'project_name': self.project_name,
      'num_files': self.metadata.num_files,
      'num_contracts': self.metadata.num_contracts,
      'num_libraries': self.metadata.num_libraries,
      'num_interfaces': self.metadata.num_interfaces,
      'num_functions': self.metadata.num_functions,
      'num_failures': len(self.failures),

      'cc_total': self.cc.total,
      'cc_mean': self.cc.mean,
      'cc_median': self.cc.median,

      'loc_total': self.metadata.loc_total,
      'loc_mean_file': self.metadata.loc_mean_file,
      'loc_median_file': self.metadata.loc_median_file,
    }

results: List[Result] = []

for cfg in project_configs:
  p = Project(cfg)
  cc = CyclomaticComplexityResult.neutral()
  md = MetadataResult.neutral()

  for path in p:
    cc += CyclomaticComplexityProcessor.run(path)
    md += MetadataProcessor.run(path)

  results.append(Result(
    project_name=p.name,
    cc=cc,
    metadata=md,
    failures=p.slither_failures
  ))

df = pd.DataFrame.from_records(r.to_record() for r in results)
df.to_csv(DATASET_CSV_OUTPUT_PATH, index=False)
with open(DATASET_DILL_OUTPUT_PATH, 'wb') as f:
  dill.dump(results, f)