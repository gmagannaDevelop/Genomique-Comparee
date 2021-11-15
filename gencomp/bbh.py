"""
docstring
"""


def search_bbh(x):
    """
    x[ecoli1][ecoli2][gene1] = gene2
    x[ecoli2][ecoli1][gene2] = gene1

    ssi ils sont bbh
    """
    bbh = dict()
    for q_strain in x.keys():
        if q_strain not in bbh.keys():
            bbh.update({q_strain: dict()})
        else:
            raise KeyError("Duplicate entry found in dict")
        for t_strain in x[q_strain].keys():
            for q_gene in x[q_strain][t_strain].keys():
                _direct = x[q_strain][t_strain][q_gene]
                _inverse = x[t_strain][q_strain].get(_direct, "")
                if _inverse and _inverse == q_gene:
                    pass
                    # ajouter les entr'ees au dico bbh
