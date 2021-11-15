"""
docstring
"""

def search_bbh(bh):
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

from gencomp.parsing import parse_blast_directory_to_dict
blast_data_dict = parse_blast_directory_to_dict("Data/Outputs_tmp")
bbh = search_bbh(blast_data_dict)

import networkx as nx

G = nx.Graph()
G.add_nodes_from(list(bbh.keys()))
edges = []

for query_strain in bbh.keys():
    for target_strain in bbh[query_strain].keys():
        weight = len(bbh[query_strain][target_strain])
        edges.append((query_strain, target_strain, weight)) if weight > 0 else None

G.add_weighted_edges_from(edges)

C = nx.find_cliques(G)
strains_of_the_clique = list(C)