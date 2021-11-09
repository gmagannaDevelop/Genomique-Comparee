#!/bin/bash


# Generates a blastp database for each protein file (fasta format) contained in the directory [input_path]
# The database is created in the [database_path] directory

# to run:
# bash blast_db_creation.sh


##### PARAMETERS #####

database_path=../Data/Blast_db/
input_path=../Data/Inputs/

##### END PARAMETERS #

##### MAIN #####

if [ ! -d $database_path ]; then
        mkdir $database_path
fi

for species in $input_path*
do
        temp=${species/*\//}
        makeblastdb -in $input_path$temp -dbtype "prot" -out $database_path${temp/.fa*/}

#        ../ncbi-blast-2.12.0+/bin/makeblastdb -in $input_path$temp -dbtype "prot" -out $database_path${temp/.fa*/}
        echo ""
done

##### END MAIN #
