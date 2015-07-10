# DRCLUSTER
### Dimensionality Reduction Cluster

Clustering FASTA datasets using dimensionality reduction algorithms.

## Overview

### BLAST+/jackhmmer all vs. all sequence comparison
- BLAST+: Convert FASTA file to protein database and search using FASTA file as query
- jackhmmer: PSI-BLAST-like iterative search of a FASTA query against itself

Results are stored in a abstracted pairwise, symmetric, similarity matrix.

### SVD/t-SNE hybrid dimensionality reduction

Converts high dimensional similarity matrix into low-dimensional embedding while maintaining local manifold structure.

Embedding is stored as a two-dimensional numpy array.

### Plotting

Uses matplotlib to plot embedding with basic annotation tools.


## Pip installation
- We recommend you set up a virtual environment and run the command ```pip install -r requirements.txt```
- Then run ```pip install tsne```. (The setup for tsne requires the numpy module)

- Alternatively, install all the packages in requirements.txt manually.


Required modules:
```
Cython==0.22
matplotlib==1.4.3
scikit-learn==0.16.1
scipy==0.15.1
tsne==0.1.1
```

- Also, you must have a working installation of either BLAST+ or jackhmmer for all vs. all sequence alignment.
- Only BLAST+ will work, legacy BLAST will not work!

## Installing the t-SNE module

- Navigate to the src/lib/tsne/ folder
- Run make clean, then make, and finally make install
- This should create the tsne binaries appropriate for your system

## Walkthrough for minimal usage

Specify the path to the FASTA file using the -f flag. This is require
- ```-f path/to/fasta.ff```

Select sequence alignment type using the -search flag. If no flag is specified, default is HMMER.
- ```-search hmmer```

Either provide a path to HMMER or BLAST executables, or a path to an alignment file.
- ```-align my/hmmer/results```
- ```-bin my/hmmer/bin```
- Ensure that the results file or bin correspond to selected sequence alignment type

Matplotlib generated plot with ```-plot``` flag

Complete DRCluster command:
- ```drcluster -f path/to/fasta.ff -search hmmer -bin path/hmmer/bin -plot```

## Using annotated FASTA files

To get coloring based on modelability and PFAM, format FASTA headers into the following: (note that a comparison to PDB database is required)

> *>*name*;*pfamID;dom#;domlength;fulllength;domevalue;fullevalue;%len;modelability

- Ex. ```>TR42;PF00240;1;63;120;3e-05;4e-4;88;mod```

## List of All Files Generated by DRCluster
    For example fasta file, ex.ff:

1. ex.blast_tbl: all vs. all BLAST output in tabular format

2. sparsedata.txt: similarity matrix derived from BLAST output

3. ex_2d_svdsne_coords.txt: SVD/tSNE generated coordinates for all proteins (in 2D)

4. ex_2D_svdsne_fastacoords.txt: SVD/tSNE generated coordinates for all proteins labeled with fasta header

5. (if -color group flag is on) groups.txt: clusters of proteins after dimensionality reduction as identified by DBSCAN


## List of All Flags

-h, --help
                        show this help message and exit

-f FASTA, --fasta FASTA
                        Path to FASTA file

-dir DIRECTORY, --directory DIRECTORY
                        Name of output directory

-val {b,e}, --value {b,e}
                        Choose what value to use (bitscore or e-value)

-search {blast,hmmer}, --search {blast,hmmer}
                        Choose alignment program (BLAST or HMMER)

-bin EXEBIN, --exebin EXEBIN
                        Path to binary executables, either BLAST or hmmer

-align ALIGNFILE, --alignfile ALIGNFILE
                        Jackhmmer or BLAST output file

-e EVALUE, --evalue EVALUE
                        Evalue for sequence alignment

-dim {2,3,4}, --dimension {2,3,4}
                        Choose how many dimensions to use

-type {svdsne,mdsonly,sneonly}, --type {svdsne,mdsonly,sneonly}
                        Choose clustering algorithm

-theta THETA, --theta THETA
                        Theta value for bh_tsne (Lower value is more accurate,
                        0 is true TSNE

-color {pfam,mod,group}, --color {pfam,mod,group}
                        Choose coloring scheme: modelability, PFAM, or group

-parsed, --preparsed
                        Results have already been parsed into a similarity matrix

-clustered, --preclustered
                        Clustering algorithm has already been applied

-plot, --plot
                        Plot coordinates with matplotlib

-reinit, --reinitialize
                        Create new random initialization of points

-a, --annotated
                        FASTA files are annotated with the PFAM and mod headers

-perp PERPLEXITY, --perplexity PERPLEXITY
                        Set the number of neighbors to use in the t-SNE
                        algorithm

