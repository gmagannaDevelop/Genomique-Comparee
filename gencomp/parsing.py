"""
placeholder
wait for real docstring
"""

import copy
from pathlib import Path
from typing import Union, List, Dict, Optional

import toml
import numpy as np
import pandas as pd
from tidycsv import TidyCSV as Tidy
from gencomp.utils import ObjDict as odict

__GENCOMP_DIR__ = Path(__file__).parent.absolute()
__ASSETS_DIR__ = __GENCOMP_DIR__.joinpath("_assets")
__CONFIG_FILE__ = __ASSETS_DIR__.joinpath("config.toml")
__THRESHOLDS_FILE__ = __ASSETS_DIR__.joinpath("thresholds.csv")

with open(__CONFIG_FILE__, "r", encoding="utf-8") as f:
    _config = toml.load(f, _dict=odict)
    config = copy.deepcopy(_config)

with open(__THRESHOLDS_FILE__, "r", encoding="utf-8") as f:
    _thresholds_df = pd.read_csv(f, index_col=0)
    _thresholds = _thresholds_df.loc[
        "threshold",
    ].to_dict()


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


def parse_blast_to_dataframe(file: Union[str, Path]) -> pd.DataFrame:
    """ """
    with Tidy(file, separator=_config.parsing.separator) as g:
        x = pd.read_csv(
            g, sep=_config.parsing.separator, header=None, names=_config.parsing.columns
        )
    return x


def parse_blast_to_dict(
    file: Union[str, Path],
    thresholds: Dict[str, Union[int, float]] = _thresholds,
    n_pass: Optional[int] = None,
):
    """ """
    data = dict()
    names = _config.parsing.criteria.names
    is_int = _config.parsing.criteria.is_int

    n_pass = n_pass or len(thresholds)
    if n_pass > len(thresholds):
        raise ValueError(
            "\n".join(
                [
                    "n_pass should be equal or lesser than the number of thresholds.",
                    f"n_pass = {n_pass}",
                    f"len(thresholds) = {len(thresholds)}",
                ]
            )
        )

    with Tidy(file, separator=_config.parsing.separator) as g:
        try:
            for line in g.readlines():
                query, target, *criteria = line.strip().split(_config.parsing.separator)

                if query not in data.keys():
                    data.update({query: dict()})

                name_value_type = zip(names, criteria, is_int)
                _entry = {
                    name: int(value) if _type else float(value)
                    for name, value, _type in name_value_type
                }
                criteria = compute_selection_criteria(_entry)
                _passed = sum(
                    1 for i in thresholds.keys() if criteria[i] > thresholds[i]
                )
                if _passed >= n_pass:
                    data[query][target] = _entry
        except KeyError:
            raise KeyError(
                "\n".join(
                    [
                        "`thresholds` contains keys absent in entry file",
                        f"{criteria.keys()}",
                        f"{thresholds.keys()}",
                    ]
                )
            ) from None

    return data


def compute_selection_criteria(
    blast: Dict[str, Union[int, float]]
) -> Dict[str, Union[int, float]]:
    """Calculate a series of parameters used to
    discriminate which entries should be kept to
    search for a core genome from a series of
    blast files (*.bl)"""

    criteria = dict()
    criteria["coverage"] = (blast["s. end"] - blast["s. start"]) / blast[
        "subject length"
    ]
    criteria["log_bit_score"] = np.log(blast["bit score"] + 1)
    criteria["% identity"] = blast["% identity"]
    return criteria


# def check_entry_meets_criteria(
#    entry: Dict[str, Union[int, float]],
# ):
#    """According to the discussion we had in class"""
#    coverage = entry["s. start"] - entry["s. end"] / entry["subject length"]
#    return None
