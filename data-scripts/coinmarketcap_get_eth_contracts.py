from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import json

from time import sleep

import coloredlogs
import logging

from typing import Dict, Optional

URLS = [
  'https://coinmarketcap.com/currencies/bitcoin/',
  'https://coinmarketcap.com/currencies/ethereum/',
  'https://coinmarketcap.com/currencies/tether/',
  'https://coinmarketcap.com/currencies/bnb/',
  'https://coinmarketcap.com/currencies/solana/',
  'https://coinmarketcap.com/currencies/xrp/',
  'https://coinmarketcap.com/currencies/usd-coin/',
  'https://coinmarketcap.com/currencies/cardano/',
  'https://coinmarketcap.com/currencies/avalanche/',
  'https://coinmarketcap.com/currencies/dogecoin/',
  'https://coinmarketcap.com/currencies/polkadot-new/',
  'https://coinmarketcap.com/currencies/tron/',
  'https://coinmarketcap.com/currencies/polygon/',
  'https://coinmarketcap.com/currencies/chainlink/',
  'https://coinmarketcap.com/currencies/toncoin/',
  'https://coinmarketcap.com/currencies/internet-computer/',
  'https://coinmarketcap.com/currencies/shiba-inu/',
  'https://coinmarketcap.com/currencies/multi-collateral-dai/',
  'https://coinmarketcap.com/currencies/litecoin/',
  'https://coinmarketcap.com/currencies/bitcoin-cash/',
  'https://coinmarketcap.com/currencies/ethereum-classic/',
  'https://coinmarketcap.com/currencies/uniswap/',
  'https://coinmarketcap.com/currencies/cosmos/',
  'https://coinmarketcap.com/currencies/unus-sed-leo/',
  'https://coinmarketcap.com/currencies/optimism-ethereum/',
  'https://coinmarketcap.com/currencies/near-protocol/',
  'https://coinmarketcap.com/currencies/stellar/',
  'https://coinmarketcap.com/currencies/okb/',
  'https://coinmarketcap.com/currencies/lido-dao/',
  'https://coinmarketcap.com/currencies/injective/',
  'https://coinmarketcap.com/currencies/aptos/',
  'https://coinmarketcap.com/currencies/filecoin/',
  'https://coinmarketcap.com/currencies/immutable-x/',
  'https://coinmarketcap.com/currencies/monero/',
  'https://coinmarketcap.com/currencies/arbitrum/',
  'https://coinmarketcap.com/currencies/hedera/',
  'https://coinmarketcap.com/currencies/kaspa/',
  'https://coinmarketcap.com/currencies/celestia/',
  'https://coinmarketcap.com/currencies/stacks/',
  'https://coinmarketcap.com/currencies/mantle/',
  'https://coinmarketcap.com/currencies/vechain/',
  'https://coinmarketcap.com/currencies/cronos/',
  'https://coinmarketcap.com/currencies/trueusd/',
  'https://coinmarketcap.com/currencies/first-digital-usd/',
  'https://coinmarketcap.com/currencies/maker/',
  'https://coinmarketcap.com/currencies/bitcoin-sv/',
  'https://coinmarketcap.com/currencies/the-graph/',
  'https://coinmarketcap.com/currencies/sei/',
  'https://coinmarketcap.com/currencies/thorchain/',
  'https://coinmarketcap.com/currencies/aave/',
  'https://coinmarketcap.com/currencies/algorand/',
  'https://coinmarketcap.com/currencies/ordi/',
  'https://coinmarketcap.com/currencies/render/',
  'https://coinmarketcap.com/currencies/multiversx-egld/',
  'https://coinmarketcap.com/currencies/quant/',
  'https://coinmarketcap.com/currencies/sui/',
  'https://coinmarketcap.com/currencies/sats/',
  'https://coinmarketcap.com/currencies/mina/',
  'https://coinmarketcap.com/currencies/flow/',
  'https://coinmarketcap.com/currencies/helium/',
  'https://coinmarketcap.com/currencies/synthetix/',
  'https://coinmarketcap.com/currencies/fantom/',
  'https://coinmarketcap.com/currencies/the-sandbox/',
  'https://coinmarketcap.com/currencies/axie-infinity/',
  'https://coinmarketcap.com/currencies/theta-network/',
  'https://coinmarketcap.com/currencies/bittorrent-new/',
  'https://coinmarketcap.com/currencies/ftx-token/',
  'https://coinmarketcap.com/currencies/tezos/',
  'https://coinmarketcap.com/currencies/kucoin-token/',
  'https://coinmarketcap.com/currencies/wemix/',
  'https://coinmarketcap.com/currencies/onbeam/',
  'https://coinmarketcap.com/currencies/decentraland/',
  'https://coinmarketcap.com/currencies/neo/',
  'https://coinmarketcap.com/currencies/osmosis/',
  'https://coinmarketcap.com/currencies/eos/',
  'https://coinmarketcap.com/currencies/bonk1/',
  'https://coinmarketcap.com/currencies/bitget-token-new/',
  'https://coinmarketcap.com/currencies/kava/',
  'https://coinmarketcap.com/currencies/astar/',
  'https://coinmarketcap.com/currencies/oasis-network/',
  'https://coinmarketcap.com/currencies/iota/',
  'https://coinmarketcap.com/currencies/ethereum-name-service/',
  'https://coinmarketcap.com/currencies/wootrade/',
  'https://coinmarketcap.com/currencies/usdd/',
  'https://coinmarketcap.com/currencies/gala/',
  'https://coinmarketcap.com/currencies/pancakeswap/',
  'https://coinmarketcap.com/currencies/chiliz/',
  'https://coinmarketcap.com/currencies/blur-token/',
  'https://coinmarketcap.com/currencies/terra-luna/',
  'https://coinmarketcap.com/currencies/xdc-network/',
  'https://coinmarketcap.com/currencies/rocket-pool/',
  'https://coinmarketcap.com/currencies/ecash/',
  'https://coinmarketcap.com/currencies/frax-share/',
  'https://coinmarketcap.com/currencies/conflux-network/',
  'https://coinmarketcap.com/currencies/klaytn/',
  'https://coinmarketcap.com/currencies/akash-network/',
  'https://coinmarketcap.com/currencies/arweave/',
  'https://coinmarketcap.com/currencies/curve-dao-token/',
  'https://coinmarketcap.com/currencies/fetch/',
  'https://coinmarketcap.com/currencies/flare/'
]

XPATH_CONTRACTS = "//span[@data-role='title' and text()='Contracts']"


# # setup logging
# # for viz on my terminal theme
# coloredlogs.DEFAULT_FIELD_STYLES = { 'levelname': {'color': 'white'} } 
# # logging.basicConfig(level=logging.INFO)
# l = logging.getLogger('Yus')
# coloredlogs.install(level='DEBUG')
# l.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setFormatter( logging.Formatter('%(levelname)s:%(asctime)s:%(message)s') )
# l.addHandler(l)


# setup driver and wait
options = Options()
options.page_load_strategy = 'none'
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 3)
driver.implicitly_wait(5) # seconds
 
results: Dict[str, bool] = {}

XPATH_MORE = ".//div[@data-role='body']"
# check each url

def retrieve_url(url, results):
  try:
    driver.get(url)
    print(f'In {url}')
    try:
      wait.until( EC.presence_of_element_located((By.XPATH, XPATH_CONTRACTS)) )
      print(f'Contract(s) found!')

    # no contracts found
    except TimeoutException:
      # l.info(f"SKIP - no 'Contracts' section found for {url}")
      print('No contracts found')
      results[url] = False
      return

    el_more_contracts = driver.find_element(By.XPATH, XPATH_CONTRACTS)
    el_container = el_more_contracts.find_element(By.XPATH, '../..')
    el_first_contract = el_container.find_element(By.CSS_SELECTOR, '[data-role="body"] > div > div')

    if 'Ethereum' in el_first_contract.text:
      results[url] = True
      print('Match!')
      return


    try:
      # renew
      el_more_contracts = driver.find_element(By.XPATH, XPATH_CONTRACTS) 
      el_container = el_more_contracts.find_element(By.XPATH, '../..')
      el_more = el_container.find_element(By.CSS_SELECTOR, '[data-role="body"] > div > div:nth-child(2)')

      print(el_first_contract.text)
      ActionChains(driver).move_to_element(el_more).perform()
      sleep(2)
      el_more_contracts = driver.find_element(By.CSS_SELECTOR, '.tippy-content')
      print(el_more_contracts.text)
      if 'Ethereum' in el_more_contracts.text:
        results[url] = True
        print('Match!')


    except NoSuchElementException:
      print('no find')
      results[url] = False
      return
  except StaleElementReferenceException:
    print("STALE, trying again...")
    retrieve_url(url, results)

for url in URLS:
  retrieve_url(url, results)
print(results)
with open('results.json', 'w') as f:
  json.dump(results, f)