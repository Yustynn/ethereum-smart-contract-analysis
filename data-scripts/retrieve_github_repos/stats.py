# Quick count on the number of repo results

import os
import json
import sys

RESULTS_DIR = './results'


results = []
for fname in os.listdir(RESULTS_DIR):
  if not fname.endswith('.json'):
    continue
  try:
    with open(os.path.join(RESULTS_DIR, fname)) as f:
      data = json.load(f)

    results += data['results']

  except Exception as e:
    print(f"ERROR - Failure on {fname}")
    print(e)

    sys.exit()

print(f"{len(results)} repos")