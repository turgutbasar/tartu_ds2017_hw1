'''
Sudoku Game Server - Main
Created on Nov 5 , 2017
@author: basar
'''
# Imports----------------------------------------------------------------------
from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from os.path import abspath, sep
# Main method -----------------------------------------------------------------
if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    # Parsing arguments
    parser = ArgumentParser(description=__info(),
                            version = ___VER)
    args = parser.parse_args()
    print("Initial Server Code")
