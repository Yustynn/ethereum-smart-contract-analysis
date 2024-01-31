"""Uses /data-scripts/retrieve_github_repos/results"""

import json
import os
import pandas as pd

DATA_DIR = '../../data-scripts/retrieve_github_repos/results'
OUTPUT_PATH = 'all-repos.csv'

records: list[dict] = []
for fname in os.listdir(DATA_DIR):
  if not fname.endswith('.json'):
    continue
  path = os.path.join(DATA_DIR, fname)
  with open(path) as f:
    data = json.load(f)

  for result in data['results']:
    records.append({
      'name': data['name'],
      'solidity_fraction': result['solidity_fraction'],
      'repo_name': result['name'],
      'url': result['url']
    })

pd.DataFrame.from_records(records).to_csv(OUTPUT_PATH, index=False)