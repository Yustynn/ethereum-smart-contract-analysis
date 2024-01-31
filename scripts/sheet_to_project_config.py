# hacky, but works fine.
import pandas as pd

SHEET_PATH = '../input/project-to-github.csv'
INDENT = '  '

parts = []
df = pd.read_csv(SHEET_PATH)
for r in df[df.gh_link.notnull()].itertuples():
  part = f'\n{INDENT}ProjectConfig('

  name = r.name
  repo_urls = r.gh_link.split(', ')

  part += f'\n{2*INDENT}name="{name}",'
  part += f'\n{2*INDENT}repo_urls=['

  for url in repo_urls:
    part += f'\n{3*INDENT}"{url}",'
  part += f'\n{2*INDENT}],'
  part += f'\n{INDENT}),'

  parts.append(part)


output = 'PROJECT_CONFIGS = ['
output += '\n'.join(parts)
output += '\n]'

print(output)