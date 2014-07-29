__author__ = 'kulkarnik'
import h5py
import csv

##Read FASTA file names and make a list
def read_fasta(fastafile):
    names = []
    colors = []
    with open(fastafile) as f:
        for line in f:
            parts = line.split(",")
            names.append(parts[0].strip().split()[0])
            try:
                colors.append(int(parts[1]))
            except:
                pass
    return names,colors

##Creates handle for results.out file

def open_file(filename):
    tabHandle = open(filename,"rb")
    tabParser = csv.reader(tabHandle, delimiter='\t')

    return tabParser, tabHandle


##Create the distance matrix
##Initialize with 4 (the farthest possible value)
def create_matrix(flag,names):
    f = h5py.File("mds.h5","w")
    if (flag == 'b'):
        dset = f.create_dataset("hdfmat.h5",shape=(len(names),len(names)),fillvalue=4)
    else:
        dset = f.create_dataset("hdfmat.h5",shape=(len(names),len(names)),fillvalue=1)
    return dset


##
