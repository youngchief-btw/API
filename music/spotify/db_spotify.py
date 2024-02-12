import os, sys, inspect

# Add parent directory to import search path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
sys.path.append(parent_dir)
from utils.db import get as db_get
from utils.db import set as db_set

def set(key, value):
    print(f'(spotify) db/set [{key}]: {value}')
    return db_set('spotify', key, value)

def get(key):
    value = db_get('spotify', key)
    print(f'(spotify) db/get [{key}]: {value}')
    return value
