"""
docstring
"""

import gencomp.parsing as gencomp
from typing import Tuple, List, Any
import networkx as nx

def bbh_dict_from(bh):
    bbh = dict()
    for query_strain in bh.keys():
        if query_strain not in bbh.keys():
            bbh.update({query_strain: dict()})
        else:
            raise KeyError("Duplicate entry found in dict")
        for target_strain in bh[query_strain].keys():
            bbh[query_strain][target_strain] = {}
            for query_gene in bh[query_strain][target_strain].keys():
                _direct = bh[query_strain][target_strain][query_gene]
                _inverse = bh[target_strain][query_strain].get(_direct, "")
                if _inverse and _inverse == query_gene:
                    bbh[query_strain][target_strain][query_gene] = _direct
    return bbh

# TODO: change this to yield ?
def find_core_genome(bbh: List[Tuple[str, str]], n_species: int = 21) -> Any:
    """ """
    # Create an empty graph
    G = nx.Graph()
    # Add edges formes by bbhs
    G.add_edges_from(bbh)
    # Find all cliques
    C = nx.find_cliques(G)
    cliques = list(C)

    return [clique for clique in cliques if len(clique) == n_species]

bh = gencomp.parse_blast_directory_to_dict("Data/Outputs")

def search_bbh(bh, strain_set=None) -> List[Tuple[str, str]]:
    """Search bidirectional best hits"""
    # Copy because we will modify the hits
    bh = bh.copy()

    bbh = list()
    
    strain_set = strain_set or bh.keys()
    #if strain_set is None:
    #    strain_set = bh.keys()
    
    for query_strain in strain_set:
        for target_strain in bh[query_strain].keys():
            for query_gene in bh[query_strain][target_strain].keys():
                _direct = bh[query_strain][target_strain][query_gene]
                _inverse = bh[target_strain][query_strain].get(_direct, "")
                print(_inverse) if _inverse else None
                if _inverse and _inverse == query_gene:
                    _ = bh[target_strain][query_strain].pop(_direct)
                    bbh.append((_direct, _inverse))
    return bbh


import random

random.seed(10)

bh = gencomp.parse_blast_directory_to_dict("Data/Outputs_tmp")

constrained_strain_set = list(bh.keys())
strain_subset = []

strain = random.choice(constrained_strain_set)
strain_subset.append(strain)
constrained_strain_set.remove(strain)

strain = random.choice(constrained_strain_set)
strain_subset.append(strain)
constrained_strain_set.remove(strain)

bbh = search_bbh(bh)





