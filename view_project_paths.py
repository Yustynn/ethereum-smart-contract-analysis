import logging
import os
from config import PROJECT_CONFIGS
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

OUTPUT_PATH = 'output/paths.txt'
from Project import Project

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('view_project_files')


paths = []
with logging_redirect_tqdm():
  progress_bar = tqdm(PROJECT_CONFIGS)
  for cfg in progress_bar:
    progress_bar.set_description(f'Project: {cfg.name}')
    project = Project(cfg)
    paths += list({os.path.dirname(p) for p in project.get_path_candidates()})

with open(OUTPUT_PATH, 'w') as f:
  f.write('\n'.join(sorted(paths)))
print(f'{len(paths)} saved to {OUTPUT_PATH}')