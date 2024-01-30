# note: GitHub rate limit using authenticated API is 5k per hour.

from gidgethub.aiohttp import GitHubAPI
from dotenv import load_dotenv
from typing import Dict, Optional, TypeAlias
import os
import json
import aiohttp
from tqdm import tqdm
import logging
import asyncio

RESULTS_FOLDER = './results'
load_dotenv('../../.env')

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('github_repos')

Languages: TypeAlias = Dict[str, int]

def solidity_fraction(languages: Languages) -> float:
    assert 'Solidity' in languages, f"Solidity not in {languages}"

    return languages['Solidity'] / sum(languages.values())

org_name = 'crypto-org-chain'

async def process_repo(gh: GitHubAPI, org_name: str, repo: dict) -> Optional[dict]:
    languages = await gh.getitem(f'/repos/{org_name}/{repo["name"]}/languages')
    if 'Solidity' in languages:
        return {
            'name': repo['name'],
            'url': repo['clone_url'],
            'solidity_fraction': solidity_fraction(languages),
            'languages': languages,
        }

ORG_NAMES = [
    'decentraland',
]

async def main():
    pbar = tqdm(ORG_NAMES)
    for org_name in ORG_NAMES:
        pbar.set_description(org_name)
        results_path = os.path.join(RESULTS_FOLDER, f'{org_name}.json')
        if os.path.exists(results_path):
            lg.info(f'[{org_name}] Skipping - results already exist.')
            continue

        async with aiohttp.ClientSession() as session:
            gh = GitHubAPI(session, 'web3-investigation', oauth_token=os.environ['GITHUB_TOKEN'])

            lg.info(f'[{org_name}] Retrieving repos')
            repos = []
            async for repo in gh.getiter(f'/orgs/{org_name}/repos?per_page=100'):
                repos.append(repo)
            print(len(repos))

            with open('tmp.json', 'w') as f:
                json.dump(repos, f)

            tasks = [process_repo(gh, org_name, repo) for repo in repos]
            results = await asyncio.gather(*tasks)
            results = [r for r in results if r is not None]

        with open(results_path, 'w') as f:
            json.dump({ 'org_name': org_name, 'results': results}, f)
        lg.info(f'{len(results)} results found. Written to {results_path}')


# Run the main function
asyncio.run(main())