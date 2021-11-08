"""
"""
from pathlib import Path
from typing import Union, List


def parse_strains_from_filename(
    file_name: Union[str, Path], extension: str = ".bl", split_on: str = "-vs-"
) -> List[str, str]:
    """Return a list containing the two compared strains from a filename"""
    if isinstance(file_name, Path):
        file_name = file_name.name
    elif not isinstance(file_name, str):
        raise TypeError(f"Expected `pathlib.Path` or `str` but got {type(file_name)}")
    return file_name.rstrip(extension).split(split_on)
