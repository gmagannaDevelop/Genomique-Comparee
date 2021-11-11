"""
placeholder
wait for real docstring
"""

# TODO : discuss creating a BlastParser Class, in order
# to be able to specify criteria at instantiation time.

import copy
from pathlib import Path
from typing import Union, List, Dict, Optional, Any
from collections import namedtuple
import multiprocessing as mp

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

BlastFile = namedtuple("BlastFile", ["query", "target", "file"])


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


def parse_blast_file_to_dataframe(file: Union[str, Path]) -> pd.DataFrame:
    """ """
    with Tidy(file, separator=_config.parsing.separator) as g:
        x = pd.read_csv(
            g, sep=_config.parsing.separator, header=None, names=_config.parsing.columns
        )
    return x


def parse_blast_file_to_dict(
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
        except KeyError as __k_e:
            raise KeyError(
                f"`thresholds` contains keys absent in entry file : {__k_e}"
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


def _parallel_parsing_helper(blast: BlastFile):
    """ """
    return {blast.target: parse_blast_file_to_dict(blast.file)}


def parse_blast_directory_to_dict(
    directory: Union[str, Path], n_threads: Optional[int] = None
):
    """ """
    if isinstance(directory, str):
        directory = Path(directory)
    elif not isinstance(directory, str):
        raise TypeError(f"Expected `pathlib.Path` or `str` but got {type(directory)}")

    if not directory.exists():
        raise FileNotFoundError(
            f"Specified directory {directory.absolute().as_posix()} does not exist"
        )
    if not directory.is_dir():
        raise ValueError("Expected a directory.")

    n_threads = min(n_threads, mp.cpu_count()) if n_threads else mp.cpu_count()
    # Blast outputs :
    blast_file_ls = list(directory.glob("*.bl"))
    # Blast objects (query, target, path), inderred from the filename :
    _blast_f = lambda x: BlastFile(*parse_strains_from_filename(x.name), x)
    _blasts_ls = [_blast_f(file) for file in blast_file_ls]

    _queries = list(set(bl.query for bl in _blasts_ls))
    _parallel_partition_dict = {
        query: [b for b in _blasts_ls if b.query == query and not b.query == b.target]
        for query in _queries
    }

    _heaviest_load = max(len(files) for files in _parallel_partition_dict.values())
    n_groups = min(n_threads, _heaviest_load)
    blast_dict = dict()

    with mp.Pool(n_groups) as pool:
        for query, files in _parallel_partition_dict.items():
            if query not in blast_dict.keys():
                blast_dict.update({query: dict()})
                results = pool.map(_parallel_parsing_helper, files)
                __ = [results[0].update(result) for result in results[1:]]
                blast_dict[query] = results[0]
            else:
                raise KeyError

    return blast_dict
