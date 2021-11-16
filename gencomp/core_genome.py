"""
docstring
"""

import copy
from typing import Tuple, List, Any, Dict, Optional, Iterable
import numpy as np
import networkx as nx

np.random.seed(1234)


def search_bbh(
    bh: Dict[str, Dict[str, Dict[str, str]]], strain_set: Optional[Iterable[str]] = None
) -> List[Tuple[str, str]]:
    """Search bidirectional best hits"""

    # strain_set = strain_set or bh.keys()
    # strain_set = set(strain_set)

    if strain_set:
        bh = subset_blast_dict(bh, strain_set)
    else:
        strain_set = bh.keys()

    bh = copy.deepcopy(bh)
    bbh = []

    for query_strain in strain_set:
        for target_strain in bh[query_strain].keys():
            for query_gene in bh[query_strain][target_strain].keys():
                _direct = bh[query_strain][target_strain][query_gene]
                _inverse = bh[target_strain][query_strain].get(_direct, "")
                if _inverse == query_gene:
                    _ = bh[target_strain][query_strain].pop(_direct)
                    bbh.append((_direct, _inverse))
    return bbh


def subset_blast_dict(
    bh: Dict[str, Dict[str, Dict[str, str]]], strain_set: Optional[Iterable[str]] = None
) -> List[Tuple[str, str]]:
    """Subset a blast dict, returning a shallow copy"""

    bh_subset = {}
    for query_strain in strain_set:
        bh_subset.update({query_strain: {}})
        for target_strain in set(bh[query_strain].keys()).intersection(strain_set):
            bh_subset[query_strain][target_strain] = bh[query_strain][target_strain]
    return bh_subset


# TODO: change this to yield ?
def find_core_genome(bbh: List[Tuple[str, str]], n_species: int) -> Any:
    """ """
    # Create an empty graph
    G = nx.Graph()
    # Add edges formes by bbhs
    G.add_edges_from(bbh)
    # Find all cliques
    C = nx.find_cliques(G)
    cliques = list(C)

    return [clique for clique in cliques if len(clique) == n_species]
