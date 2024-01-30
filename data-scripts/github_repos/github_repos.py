# note: GitHub rate limit using authenticated API is 5k per hour.

import aiohttp
import asyncio
import json
import logging
import os
import pandas as pd

from dotenv import load_dotenv
from gidgethub.aiohttp import GitHubAPI
from statistics import mean, median
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from typing import Dict, Optional, TypeAlias

RESULTS_FOLDER = './results'
INFO_PATH = './info.csv'

load_dotenv('../../.env')

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('github_repos')

Languages: TypeAlias = Dict[str, int]

def solidity_fraction(languages: Languages) -> float:
    assert 'Solidity' in languages, f"Solidity not in {languages}"

    return languages['Solidity'] / sum(languages.values())

async def process_repo(gh: GitHubAPI, org_name: str, repo: dict) -> Optional[dict]:
    languages = await gh.getitem(f'/repos/{org_name}/{repo["name"]}/languages')
    if 'Solidity' in languages:
        return {
            'name': repo['name'],
            'url': repo['clone_url'],
            'solidity_fraction': solidity_fraction(languages),
            'languages': languages,
        }


async def main():
    df = pd.read_csv(INFO_PATH)
    df = df[df.gh_org_name.notnull()]

    with logging_redirect_tqdm():
        pbar = tqdm(list(df.itertuples()))
        for r in pbar:
            pbar.set_description(r.name)
            results_path = os.path.join(RESULTS_FOLDER, f'{r.name}.json')

            # skip if exists
            if os.path.exists(results_path):
                lg.info(f'[{r.gh_org_name}] Skipping - results already exist.')
                continue

            # retrieve data
            async with aiohttp.ClientSession() as session:
                gh = GitHubAPI(session, 'web3-investigation', oauth_token=os.environ['GITHUB_TOKEN'])

                lg.info(f'[{r.gh_org_name}] Retrieving repos')
                repos = []
                async for repo in gh.getiter(f'/orgs/{r.gh_org_name}/repos?per_page=100'):
                    repos.append(repo)

                with open('tmp.json', 'w') as f:
                    json.dump(repos, f)

                tasks = [process_repo(gh, r.gh_org_name, repo) for repo in repos]
                results = await asyncio.gather(*tasks)
                results = [r for r in results if r is not None]

            # write to json
            with open(results_path, 'w') as f:
                solidity_fractions = [r['solidity_fraction'] for r in results]
                json.dump({
                    'name': r.name,
                    'org_name': r.gh_org_name,
                    'results': results,
                    'num_results': len(results),
                    'solidity_fraction_min': min(solidity_fractions),
                    'solidity_fraction_max': max(solidity_fractions),
                    'solidity_fraction_median': median(solidity_fractions),
                    'solidity_fraction_mean': mean(solidity_fractions),
                }, f)
            lg.info(f'{len(results)} results found. Written to {results_path}')


# Run the main function
asyncio.run(main())