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
    file_name: Union[str, Path],
    extension: str = _config.parsing.file.extension,
    split_on: str = _config.parsing.file.strain_sep,
) -> List[str]:
    """Return a list containing the two compared strains from a filename"""
    if isinstance(file_name, Path):
        file_name = file_name.name
    elif not isinstance(file_name, str):
        raise TypeError(f"Expected `pathlib.Path` or `str` but got {type(file_name)}")
    return file_name.rstrip(extension).split(split_on)


def parse_blast_to_dataframe(file: Union[str, Path]):
    """ """
    with Tidy(file, separator=_config.parsing.separator) as g:
        x = pd.read_csv(
            g, sep=_config.parsing.separator, header=None, names=_config.parsing.columns
        )
    return x


def parse_blast_to_dict(file: Union[str, Path]):
    """ """
    data = dict()
    names = _config.parsing.criteria.names
    is_int = _config.parsing.criteria.is_int
    with Tidy(file, separator=_config.parsing.separator) as g:
        for line in g.readlines():
            query, target, *criteria = line.strip().split(_config.parsing.separator)

            if query not in data.keys():
                data.update({query: dict()})

            name_value_type = zip(names, criteria, is_int)
            data[query][target] = {
                name: int(value) if _type else float(value)
                for name, value, _type in name_value_type
            }

    return data
