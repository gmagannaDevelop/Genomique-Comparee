# Genomique-Comparee

Génomique Comparée (Cours M2 AMI2B Paris-Saclay)
Students :

    * Théo Roncalli
    * Gustavo Magaña López
    * Anthony Boutard

Parse the whole `blast_outputs` directory into a dict, 
using the `gencomp` python package:

```python

from gencomp.parsing import parse_blast_directory_to_dict

blast_data_dict = parse_blast_directory_to_dict("blast_outputs")
```
