# Genomique-Comparee

Génomique Comparée (Cours M2 AMI2B Paris-Saclay)
Students :

    * Théo Roncalli
    * Gustavo Magaña López
    * Anthony Boutard
    
    
## Usage 

Parse the whole `blast_outputs` directory into a dict, containing the best hits.
```python
from gencomp.parsing import parse_blast_directory_to_dict
import numpy as np
import gencomp.core_genome as cgenome

# unidirectional best hits
bh = parse_blast_directory_to_dict("Data/Outputs/")
# bidirectional best hits
bbh = cgenome.search_bbh(bh)
# core genome (list of cliques)
core_genome = cgenome.find_core_genome(bbh, 21)

# random strain subsets sorted by size in increasing order
strains = [
    set(np.random.choice(list(bh.keys()), i, replace=False)) for i in range(2, 21)
]

sub_bbh = cgenome.search_bbh(bh, strains[4])
sub_core_genome = cgenome.find_core_genome(sub_bbh, len(strains[4]))

```

All of the entries of `bh` have been selected according to [our thresholds](https://github.com/gmagannaDevelop/Genomique-Comparee/tree/main/Figures) computed by [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html?highlight=kmeans#sklearn.cluster.KMeans).


## TODO 
 
* Compute Bidirectional Best Hits (should be trivial with the previous dict).
* Compute the clique.


## Installation

First step is cloning the repo (if we publish to PyPI you won't need to clone the repo unless you want to have the development version).
```bash
 # clone the repo
 git clone https://github.com/gmagannaDevelop/Genomique-Comparee.git
```

### Using poetry (recommended)
 
 We recommend using [poetry](https://python-poetry.org/) to install the package as its dependency solver and lock files
 are far more reliable than Anaconda's. This module is developped using `Python 3.8.8`. No support is intended for older Python versions, specially 
 so for `Python 2*` as it has been deprecated.
 
  ```bash
 # ask poetry to install all the dependencies
 poetry install
 # open a new shell within the virtual environment
 poetry shell
 # You are ready to go :)
 ```
 
 **If you don't have poetry installed, run this first**
 ```bash
 curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
 #curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
 ```
  **WARNING**: This assumes `python` points to `python3` on your system. If it is not the case, then you should run the second option.
 
 ### Using Anaconda
 
 ```bash
 # create a new conda environment (you can replace "gencomp" with any name you like)
 conda create -n gencomp python=3.8.8
 # activate it 
 conda activate gencomp
 # install the dependencies using pip
 pip install -r requirements.txt
 ```
 
