from glob import glob
from slither import Slither
from typing import List
import logging
import os
import sys
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

sys.path.append('..')

from git import Repo
from config import ProjectConfig, EXCLUDE_PATHS_PATH, REPO_DIR
from utils import set_appropriate_solc_version


lg = logging.getLogger('Project')
lg.setLevel(logging.DEBUG)

exclude_paths = open(EXCLUDE_PATHS_PATH).read().split('\n')


class Project:
  def __init__(self, config: ProjectConfig):
    self.name = config.name
    self.repo_urls = [
      # ensure repo doesn't end with '/' as it breaks path
      # processing.
      u[:-1] if u.endswith('/') else u
      for u in config.repo_urls
    ]
    self.exclude_dirs = config.exclude_dirs
    self.base_dir = os.path.join(REPO_DIR, self.name)

    self.slither_failures = []

    os.makedirs(self.base_dir, exist_ok=True)
    self.ensure_repos_exist()

  def ensure_repos_exist(self):
    with logging_redirect_tqdm():
      pbar = tqdm(self.repo_urls)
      for repo_url in pbar:
        pbar.set_description(f"[{self.name}] {os.path.basename(repo_url)}")
        self.ensure_repo_exists(repo_url)
  
  def ensure_repo_exists(self, repo_url):
    name = os.path.basename(repo_url)
    path = os.path.join(self.base_dir, name)

    # clone repo if it doesn't exist
    if not os.path.exists(path):
      with logging_redirect_tqdm():
        lg.info(f"Cloning repo {repo_url}, with submodules")
        Repo.clone_from(repo_url, path, multi_options=["--recurse-submodules"])
        # lg.info(f"{name} cloned with submodules.")


  def get_path_candidates(self) -> List[str]:
    global exclude_paths

    overall_candidates = []
    for repo_url in self.repo_urls:
      name = os.path.basename(repo_url)
      path = os.path.join(self.base_dir, name)

      repo = Repo(path)
      submodule_paths = {os.path.join(path, s.path) for s in repo.submodules}

      candidates = glob(os.path.join(path, '*.sol'))
      candidates += glob(os.path.join(path, '**/*.sol'), recursive=True)
      candidates = {
        c for c in candidates
        if
          # exclude submodules
          not any(c.startswith(ip) for ip in submodule_paths)
          # exclude exclude_dirs
          and not any(c.startswith(ip) for ip in exclude_paths)
          # exclude tests
          and not c.endswith('.t.sol')
          # only include files
          and os.path.isfile(c)
      }

      overall_candidates += list(candidates)

    return overall_candidates

  def __iter__(self) -> Slither:
    self.slither_failures = []
    with logging_redirect_tqdm():
      progress_bar = tqdm(self.get_path_candidates(), desc=self.name)
      for path in progress_bar:
        progress_bar.set_description(f'Path: {path}')
        try:
          set_appropriate_solc_version(path)
          yield Slither(path)
        except Exception as e:
          lg.info(f'[FAIL] {path}')
          self.slither_failures.append((path, e))

    

    