"""
"""
from pathlib import Path
from typing import Union


def parse_strains_from_filename(file_name: Union[str, Path]):
    """ """
    if isinstance(file_name, Path):
        file_name = file_name.name
    # file.name.rstrip(self._extension).split("-vs-")
    return []
