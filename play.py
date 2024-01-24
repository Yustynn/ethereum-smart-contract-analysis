import pickle
from config import DATASET_DILL_OUTPUT_PATH

with open(DATASET_DILL_OUTPUT_PATH, 'rb') as f:
  results = pickle.load(f)

print(results)