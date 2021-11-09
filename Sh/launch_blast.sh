#!/bin/bash


# This script executes all possible blastp for the given blast database [database_path] and protein file [input_path] and writes the results ( [query file]-vs-[subject file].bl ) in a new directory [output_path].
# output format : tabular file with the following column organization (see https://www.ncbi.nlm.nih.gov/books/NBK279684/): qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore, qlen, slen, gaps
# 
# [database_path], [input_path] and [input_path] must be given by the user in the PARAMETERS section

# to run
# bash launch_blast.sh

##### PARAMETERS #####

database_path=../Data/Blast_db/
input_path=../Data/Inputs/
output_path=../Data/Outputs/

##### END PARAMETERS #

##### MAIN #####

if [ ! -d $output_path ]; then
        mkdir $output_path
fi

for set1 in $input_path*
do
        temp=${set1/*\//}
        for set2 in $input_path*
        do
                temp_set2=${set2/*\//}
                if [ ! $temp = $temp_set2 ]; then
                        out=$output_path${temp/.fa*/}-vs-${temp_set2/.fa*/.bl}
                        db=$database_path${temp_set2/.fa*/}
                        echo "IN: "$set1
                        echo "DB: "$db
                        echo "OUT: "$out
                        echo "RUNNING BLAST..."
                        echo ""
                        blastp -query $set1 -db $db -out $out -num_threads 2 -outfmt '7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen gaps'
                fi
        done
done

##### END MAIN #
