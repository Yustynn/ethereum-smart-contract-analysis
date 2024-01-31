import logging
import pandas as pd
from dataclasses import dataclass
from config import DATASET_CSV_OUTPUT_PATH, DATASET_DILL_OUTPUT_PATH, PROJECT_CONFIGS
from typing import Dict, List, Union
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import dill

from Project import Project
from processors.CyclomaticComplexityProcessor import CyclomaticComplexityProcessor, CyclomaticComplexityResult
from processors.MetadataProcessor import MetadataProcessor, MetadataResult

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('Main')

@dataclass
class Result:
  project_name: str
  cyclomatic_complexity: CyclomaticComplexityResult
  metadata: MetadataResult
  failures: Dict[str, str]
  
  def to_record(self) -> Dict[str, Union[float, int, str]]:
    assert self.cyclomatic_complexity.num_functions == self.metadata.num_functions, "Metadata and CC show different num functions"

    return {
      'project_name': self.project_name,
      'num_files': self.metadata.num_files,
      'num_contracts': self.metadata.num_contracts,
      'num_libraries': self.metadata.num_libraries,
      'num_interfaces': self.metadata.num_interfaces,
      'num_functions': self.metadata.num_functions,
      'num_failures': len(self.failures),

      'cc_total': self.cyclomatic_complexity.total,
      'cc_mean': self.cyclomatic_complexity.mean,
      'cc_median': self.cyclomatic_complexity.median,
      'cc_max': self.cyclomatic_complexity.max,

      'loc_total': self.metadata.loc_total,
      'loc_mean_file': self.metadata.loc_mean_file,
      'loc_median_file': self.metadata.loc_median_file,
    }

results: List[Result] = []

with logging_redirect_tqdm():
  progress_bar = tqdm(PROJECT_CONFIGS)
  for cfg in progress_bar:
    progress_bar.set_description(f'Project: {cfg.name}')
    project = Project(cfg)
    cyclomatic_complexity = CyclomaticComplexityResult.neutral()
    metadata = MetadataResult.neutral()

    for slither in project:
      cyclomatic_complexity += CyclomaticComplexityProcessor.run(slither)
      metadata += MetadataProcessor.run(slither)

    results.append(Result(
      project_name=project.name,
      cyclomatic_complexity=cyclomatic_complexity,
      metadata=metadata,
      failures=project.slither_failures
    ))

df = pd.DataFrame.from_records(r.to_record() for r in results)
df.to_csv(DATASET_CSV_OUTPUT_PATH, index=False)
with open(DATASET_DILL_OUTPUT_PATH, 'wb') as f:
  dill.dump(results, f)