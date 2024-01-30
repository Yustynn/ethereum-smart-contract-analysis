# hacky, but works fine.

import os
import json
import sys

RESULTS_DIR = './results'

parts = []

INDENT = '  '

for fname in os.listdir(RESULTS_DIR):
  part = f'\n{INDENT}ProjectConfig('

  if not fname.endswith('.json'):
    continue
  try:
    with open(os.path.join(RESULTS_DIR, fname)) as f:
      data = json.load(f)
      name = data["name"]
      repo_urls = [r['url'] for r in data['results']]

      part += f'\n{2*INDENT}name="{name}",'
      part += f'\n{2*INDENT}repo_urls=['

      for url in repo_urls:
        part += f'\n{3*INDENT}"{url}",'
      part += f'\n{2*INDENT}],'
    part += f'\n{INDENT}),'

    parts.append(part)


  except Exception as e:
    print(f"ERROR - Failure on {fname}")
    print(e)

    sys.exit()

output = 'project_configs = ['
output += '\n'.join(parts)
output += '\n]'

print(output)