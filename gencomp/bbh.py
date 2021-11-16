"""
docstring
"""

from typing import Tuple, List, Any
import networkx as nx


def search_bbh(bh) -> List[Tuple[str, str]]:
    """Search bidirectional best hits"""
    # Copy because we will modify the hits
    bh = bh.copy()

    bbh = list()
    for query_strain in bh.keys():
        for target_strain in bh[query_strain].keys():
            for query_gene in bh[query_strain][target_strain].keys():
                _direct = bh[query_strain][target_strain][query_gene]
                _inverse = bh[target_strain][query_strain].get(_direct, "")
                if _inverse and _inverse == query_gene:
                    _ = bh[target_strain][query_strain].pop(_direct)
                    bbh.append((_direct, _inverse))
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
