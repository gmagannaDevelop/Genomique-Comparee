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
from datetime import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def add_extra_criteria(blast: pd.DataFrame, in_place=False) -> pd.DataFrame:
    """Calculate a series of parameters used to
    discriminate which entries should be kept to
    search for a core genome from a series of
    blast files (*.bl)"""

    if not in_place:
        blast = blast.copy()
    blast["coverage"] = (blast["s. end"] - blast["s. start"]) / blast["subject length"]
    blast["log_bit_score"] = np.log(blast["bit score"] + 1)
    blast["log_e_value"] = np.log(blast["e-value"] + np.finfo(float).eps)
    return blast


# TODO : discuss the weighting average
def compute_threshold(
    column: pd.Series, weighted: bool = False, **kmeans_kwargs
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

    data = column.to_numpy().reshape(-1, 1)
    kmeans = KMeans(**_kmeans_kw).fit(data)
    mean1 = kmeans.cluster_centers_[0][0]
    mean2 = kmeans.cluster_centers_[1][0]

    if weighted:
        _prop_upper = kmeans.labels_.mean()
        _propr_lower = 1.0 - _prop_upper
        threshold = _propr_lower * mean1 + _prop_upper * mean2
    else:
        threshold = kmeans.cluster_centers_.mean()

    criteria = {
        "mean1": mean1,
        "mean2": mean2,
        "threshold": threshold,
    }
    return criteria


def plot_criteria(
    column: pd.Series,
    criteria: Dict[str, Union[int, float]],
    show_plot: bool = True,
    save_figure: bool = False,
    figure_filename: Optional[str] = None,
    **hist_kw,
):
    """Plot the computed criteria for the given column.
    'criteria' should be the output of threshold.compute_threshold()
    This function will generate a histogram with the lines corresponding
    to the two found means and the threshold which is calculated
    averaging the means of the two groups, computed via sklearn.cluster.KMeans
    """
    _hist_kw = dict(bins=30)
    if hist_kw:
        _hist_kw.update(hist_kw)
    # Create figure:
    _fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    ax.tick_params(axis="x", rotation=45)

    _n, bins, _patches = plt.hist(column, **_hist_kw)
    _round = partial(round, ndigits=2)
    nbins = list(map(_round, bins))
    plt.xticks(bins, nbins)

    # add vertical lines
    for key, value in criteria.items():
        colour = "r" if key == "threshold" else "g"
        plt.axvline(value, color=colour, label=f"{key} = {_round(value)}")

    # add annotations
    plt.legend()
    plt.title(
        f"Distribution, means, and threshold for '{column.name}'",
        loc="center",
        fontsize=14,
    )

    if save_figure:
        _filename = f"{column.name}-{str(dt.now()).split('.')[0]}.png"
        _filename = figure_filename if figure_filename else _filename
        plt.savefig(_filename)

    if show_plot:
        plt.ion()
        plt.show()
