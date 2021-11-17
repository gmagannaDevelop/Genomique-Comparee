"""
docstring
"""

import copy
from typing import Tuple, List, Any, Dict, Optional, Iterable
import numpy as np
import multiprocessing as mp
import networkx as nx

np.random.seed(1234)


def search_bbh(
    bh: Dict[str, Dict[str, Dict[str, str]]], strain_set: Optional[Iterable[str]] = None
) -> List[Tuple[str, str]]:
    """Search bidirectional best hits"""

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


def find_count_bbh_and_core_genome(
    bh: Dict[str, Dict[str, Dict[str, str]]], strain_set: Optional[Iterable[str]] = None
) -> Tuple[int, int]:
    """Helper function, returning the number of strains in `strain_set` and
    the size of the core genome spawned by the `strain_set`.

    (n_strains, n_genes_in_core_genome)
    """
    if strain_set:
        bh = subset_blast_dict(bh, strain_set)
    else:
        strain_set = bh.keys()

    n_strains = len(strain_set)
    _bbh = search_bbh(bh, strain_set=strain_set)
    return n_strains, len(find_core_genome(_bbh, n_species=n_strains))


# TODO: change this to yield ?
def find_core_genome(bbh: List[Tuple[str, str]], n_species: int) -> Any:
    """Find the list of cliques (genes within the core genome)"""
    # Create an empty graph
    G = nx.Graph()
    # Add edges formed by bbhs
    G.add_edges_from(bbh)
    # Find all cliques
    C = nx.find_cliques(G)
    cliques = list(C)

    return [clique for clique in cliques if len(clique) == n_species]


def find_random_core_genome_of_n(bh: Dict[str, Dict[str, Dict[str, str]]], n: int):
    """
    Danger! Do not call this function in parallel. np.random.choice will yield
    the same result for each one of the parallel workers.
    """
    _rand_subset = set(np.random.choice(list(bh.keys()), n, replace=False))
    _sub_bbh = search_bbh(bh, strain_set=_rand_subset)
    return find_core_genome(_sub_bbh, n_species=n)


def parallel_find_random_core_genomes(
    bh: Dict[str, Dict[str, Dict[str, str]]],
    sizes: Iterable[int],
    batch_size: int,
    n_threads: int,
):
    """For each `size` in `sizes`, compute the core genome for each one
    of randomly selected strain subsets within the batch."""
    _n_threads = min(n_threads, mp.cpu_count())

    _strain_core_genome_size: Dict[str, List[int]] = {
        "n_strains": [],
        "core_genome_size": [],
    }
    with mp.Pool(_n_threads) as pool:
        for size in sizes:
            _rand_subsets = [
                set(np.random.choice(list(bh.keys()), size, replace=False))
                for i in range(batch_size)
            ]
            batch = pool.starmap(
                find_count_bbh_and_core_genome,
                [(bh, _rand_subset) for _rand_subset in _rand_subsets],
            )
            for _size, _cg_size in batch:
                _strain_core_genome_size["n_strains"].append(_size)
                _strain_core_genome_size["core_genome_size"].append(_cg_size)

    return _strain_core_genome_size
