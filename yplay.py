import pickle
from config import DATASET_PICKLE_OUTPUT_PATH

with open(DATASET_PICKLE_OUTPUT_PATH, 'rb') as f:
  results = pickle.load(f)

print(results)