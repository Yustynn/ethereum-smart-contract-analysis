# note: GitHub rate limit using authenticated API is 5k per hour.

from github import Github, Auth
from dotenv import load_dotenv
from typing import Dict, TypeAlias
import os
import json
from tqdm import tqdm
import logging

RESULTS_FOLDER = './results'
load_dotenv('../../.env')

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('github_repos')

Languages: TypeAlias = Dict[str, int]

def solidity_fraction(languages: Languages) -> float:
    assert 'Solidity' in languages, f"Solidity not in {languages}"

    return languages['Solidity'] / sum(languages.values())

g = Github(auth=Auth.Token(os.environ['GITHUB_TOKEN']))
org_name = 'crypto-org-chain'

results = []
lg.info(f'[{org_name}] Retrieving repos')
repos = list(g.get_user(org_name).get_repos())

pbar = tqdm(repos)
for repo in pbar:
    pbar.set_description(f'[{org_name}/{repo.name}] Found {len(results)} solidity repos')
    languages = repo.get_languages()
    if 'Solidity' in languages:
        results.append({
            'name': repo.name,
            'url': repo.clone_url,
            'solidity_fraction': solidity_fraction(languages),
            'languages': languages,
        })

with open(os.path.join(RESULTS_FOLDER, f'{org_name}.json'), 'w') as f:
    json.dump({'org_name': org_name, 'results': results}, f)

g.close()