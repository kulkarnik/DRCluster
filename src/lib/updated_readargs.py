__author__ = 'kulkarnik'
import argparse, os,sys

def arg_parser():
    paraParser = argparse.ArgumentParser(description='Clustering analysis of BLAST output using MDS algorithm')

    ## This argument accepts the name of the directory with all required files
    ##
    ## Inputted directory must contain:
    ## 1. Temp directory (this will store dissimilarity matrix [mds.hdf5] and calculated coordinates [coords.npy])
    ## 2. BLAST results file with the name "results.out"
    ## 3. Text file with namestrings of proteins with the name "names_all"
    ##      namestrings must be in the format: "name of protein","name of family" if you want coloring
    ##
    ## Clustering will create/read from:
    ## 1. temp/mds.hdf5
    ## 2. temp/coords.npy
    ## 3. temp/inity.npy (random generation of points for t-SNE clustering)

    paraParser.add_argument('-f', '--fasta',
                            help="Path to FASTA file",
                            required=True)

    paraParser.add_argument('-dir', '--directory',
                            help="Name of output directory",
                            default=None)

    ## This argument chooses between the bit score and e-value
    ## as the value to generate the distance matrix
    paraParser.add_argument('-val','--value',
                            help="Choose what value to use (bitscore or e-value)",
                            choices=['b','e'], default='e')

    paraParser.add_argument('-search', '--search',
                            help="Choose alignment program (BLAST or HMMER)",
                            choices=['blast', 'hmmer'],
                            default='hmmer')

    paraParser.add_argument('-blast', '--blastpath',
                            help="Path to BLAST bin",
                            default=None)

    paraParser.add_argument('-hmmer', '--hmmerpath',
                            help="Path to hmmer bin",
                            default=None)

    paraParser.add_argument('-align', '--alignfile',
                            help="Jackhmmer or BLAST output file",
                            default=None)
    ## This argument chooses between the 2D and 3D options to
    ## graph the protein clusters
    paraParser.add_argument('-dim','--dimension',
                            help="Choose how many dimensions to use",
                            choices=['2','3'], default='2')

    ## This argument chooses the type of clustering algorithm to use
    ## The choices are:
    ## snepca = run preprocessing of (sparse) pairwise dissimilarity matrix with singular value decomposition (SVD),
    ##          and run final clustering with t-SNE
    ## snemds = run preprocessing of pairwise dissimilarity matrix with multidimensional scaling (MDS),
    ##          and run final clustering with t-SNE
    ## sneonly = run final clustering on pairwise dissimilarity matrix with t-SNE only
    paraParser.add_argument('-type','--type',
                            help="Choose clustering algorithm",
                            choices=['svdsne','mdsonly','sneonly'],default='svdsne')

    paraParser.add_argument('-color','--color',
                            help="Choose coloring scheme: modelability, PFAM, or group",
                            choices=['pfam', 'mod', 'group'],default='mod')

    ## Choose this argument if BLAST results are preparsed and HDF5 dissimilarity matrix has already been populated
    paraParser.add_argument('-parsed', '--preparsed',
                            help="Results have already been parsed into a similarity matrix",
                            action="store_true")

    paraParser.add_argument('-load', '--load',
                            help="Load coordinates from Numpy coordinate matrix")

    ## Choose this argument if clustering algorithm has already been run and coords.npy file is stored
    paraParser.add_argument('-clustered', '--preclustered',
                            help="Clustering algorithm has already been applied",
                            action="store_true")

    paraParser.add_argument('-group', '--group',
                            type=float,
                            help="Group into modeling families")

    ## Choose this argument to plot the coordinates in a PyPlot with matplotlib
    paraParser.add_argument('-plot','--plot',
                            help="Plot coordinates with matplotlib",
                            action="store_true")

    ## Choose this argument to create a new random initialization of points in t-SNE
    paraParser.add_argument('-reinit','--reinitialize',
                            help="Create new random initialization of points",
                            action="store_true")

    args = paraParser.parse_args()

    return args
