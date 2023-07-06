import os
import sys
import ast
import requests
import pprint
import json
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join

def get_latest_df(filetype="scraped_dataset"):
    data_path = "/Users/dayoorigunwa/code_base/music_mapping/data/"
    allfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    files = [filename for filename in allfiles if filetype in filename]
    files.sort()
    df = pd.read_csv(data_path + files[-1])
    return df
    