"""
    Automatically calculate thresholds to filter out
    by using unsupervised learning.
    
    DataFrames passed are assumed to have the following columns
    'query_strain', 'query_target', 'query id', 'subject id', '% identity',
       'alignment length', 'mismatches', 'gap opens', 'gaps', 'q. start',
       'q. end', 's. start', 's. end', 'e-value', 'bit score', 'query length',
       'subject length'

"""

from typing import Dict, Union, Any, Optional
from functools import partial
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def add_extra_criteria(blast: pd.DataFrame) -> pd.DataFrame:
    """Calculate a series of parameters used to
    discriminate which entries should be kept to
    search for a core genome from a series of
    blast files (*.bl)"""

    blast = blast.copy()
    blast["coverage"] = (blast["s. end"] - blast["s. start"]) / blast["subject length"]
    return blast


def compute_threshold(
    column: pd.Series, **kmeans_kwargs
) -> Dict[str, Union[int, float]]:
    """
    Default `kmeans_kwargs`:
        dict(n_clusters=2, random_state=0, verbose=False)

    """
    _kmeans_kw = dict(n_clusters=2, random_state=0, verbose=False)

    if kmeans_kwargs:
        _kmeans_kw.update(kmeans_kwargs)
    if _kmeans_kw["n_clusters"] != 2:
        raise ValueError(
            "\n".join(
                [
                    f"n_clusters={_kmeans_kw['n_clusters']}.",
                    " Should be 2 in order to compute a meaningful threshold",
                ]
            )
        )
    kmeans = KMeans(**_kmeans_kw).fit(column.to_numpy().reshape(-1, 1))
    _criteria = {
        "mean1": kmeans.cluster_centers_[0][0],
        "mean2": kmeans.cluster_centers_[1][0],
        "threshold": kmeans.cluster_centers_.mean(),
    }
    return _criteria


def compute_and_plot_criteria(
    column: pd.Series,
    show_plot: bool = True,
    save_figure: bool = False,
    figure_filename: Optional[str] = None,
    **hist_kw,
):
    """ """
    _hist_kw = dict(bins=30)
    if hist_kw:
        _hist_kw.update(hist_kw)
    # Create figure:
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    ax.tick_params(axis="x", rotation=45)

    _n, bins, _patches = plt.hist(column, **_hist_kw)
    _round = partial(round, ndigits=2)
    nbins = list(map(_round, bins))
    plt.xticks(bins, nbins)

    thresh = compute_threshold(column)
    for key, value in thresh.items():
        colour = "r" if key == "threshold" else "g"
        plt.axvline(value, color=colour, label=f"{key} = {_round(value)}")

    plt.legend()
    plt.title(
        f"Distribution, means, and threshold for '{column.name}'",
        loc="center",
        fontsize=14,
    )
    plt.ion()
    plt.show()
