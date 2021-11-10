"""
iterate over all blast (*.bl) files
"""

import pandas as pd

from gencomp.parsing import (
    config,
    parse_blast_to_dataframe,
    parse_blast_to_dict,
    parse_strains_from_filename,
)
from gencomp.utils import Path as path

data_dir = path("blast_outputs/")


# blast = pd.DataFrame(columns=config.parsing.columns)
blast = dict()
for file in data_dir.glob("*.bl"):
    query, target = parse_strains_from_filename(file.name)
    if query != target:
        # print(f"{query} : {target}")
        if query not in blast.keys():
            blast.update({query: dict()})

        blast[query][target] = parse_blast_to_dict(file)

        # with Tidy(file, separator=_config.parsing.separator) as g:
        #   tmp_df = parse_blast_to_dataframe(file)
        #   tmp_df["query_strain"] = query
        #   tmp_df["query_target"] = target
        #   blast = pd.concat([blast, tmp_df], axis="rows")
