import sys
import os
import logging
import glob

sys.path.append('..')

from git import Repo

from config import ProjectConfig, REPO_DIR


lg = logging.getLogger('Project')
lg.setLevel(logging.DEBUG)
lg.addHandler( logging.StreamHandler() )

class Project:
  def __init__(self, config: ProjectConfig):
    self.name = config.name
    self.repo_urls = [
      # ensure repo doesn't end with '/' as it breaks path processing
      u[:-1] if u.endswith('/') else u
      for u in config.repo_urls
    ]
    self.exclude_dirs = config.exclude_dirs
    self.base_dir = os.path.join(REPO_DIR, self.name)

    os.makedirs(self.base_dir, exist_ok=True)
    self.ensure_repos_exist()

  def ensure_repos_exist(self):
    for repo_url in self.repo_urls:
      self.ensure_repo_exists(repo_url)
  
  def ensure_repo_exists(self, repo_url):
    name = os.path.basename(repo_url)
    path = os.path.join(self.base_dir, name)
    if not os.path.exists(path):
      lg.info(f"Cloning repo {repo_url}")
      Repo.clone_from(repo_url, path, multi_options=["--recurse-submodules"])
      lg.info(f"{name} cloned with submodules.")

