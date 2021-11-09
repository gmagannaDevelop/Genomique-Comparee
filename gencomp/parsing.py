"""
placeholder
wait for real docstring
"""

import copy
from pathlib import Path
from typing import Union, List

import toml
import pandas as pd
from tidycsv import TidyCSV as Tidy
from gencomp.utils import ObjDict as odict

__GENCOMP_DIR__ = Path(__file__).parent.absolute()
__ASSETS_DIR__ = __GENCOMP_DIR__.joinpath("_assets")
__CONFIG_FILE__ = __ASSETS_DIR__.joinpath("config.toml")

with open(__CONFIG_FILE__, "r", encoding="utf-8") as f:
    _config = toml.load(f, _dict=odict)
    config = copy.deepcopy(_config)


def parse_strains_from_filename(
    file_name: Union[str, Path], extension: str = ".bl", split_on: str = "-vs-"
) -> List[str]:
    """Return a list containing the two compared strains from a filename"""
    if isinstance(file_name, Path):
        file_name = file_name.name
    elif not isinstance(file_name, str):
        raise TypeError(f"Expected `pathlib.Path` or `str` but got {type(file_name)}")
    return file_name.rstrip(extension).split(split_on)


def parse_blast_to_dataframe(file: Union[str, Path]):
    """ """
    with Tidy(file, separator="\t") as f:
        x = pd.read_csv(f, sep="\t", header=None, names=_config.parsing.columns)
    return x
