# Genomique-Comparee

Génomique Comparée (Cours M2 AMI2B Paris-Saclay)
Students :

    * Théo Roncalli
    * Gustavo Magaña López
    * Anthony Boutard

## Installation

### Using poetry (recommended)
sdfsmdf 


## Usage 

Parse the whole `blast_outputs` directory into a dict, 
using the `gencomp` python package:

```python

from gencomp.parsing import parse_blast_directory_to_dict

blast_data_dict = parse_blast_directory_to_dict("blast_outputs")
```

This will give you a dictionnary as follows:

```python
blast_data_dict["query_strain"]["target_strain"]["target_gene"] = "query_gene"
```

All of these entries have been selected according to our thresholds computed by KMeans.

## TODO 
 
* Compute Bidirectional Best Hits (should be trivial with the previous dict).
* Compute the clique.
