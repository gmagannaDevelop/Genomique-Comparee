import toml
from tidycsv import TidyCSV as Tidy
import pandas as pd
from gencomp.utils import ObjDict as odict


with open("config.toml", "r") as f:
    config = toml.load(f, _dict=odict)


with Tidy(config.testing.example_file, separator="\t") as f:
    x = pd.read_csv(f, sep="\t", header=None, names=config.parsing.columns)


