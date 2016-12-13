# Light Curve Similarity Search

A python command line utility to searching for similar light curves useing kernelised distance and vantage points.

### Usage

Usage: ./simsearchutil.py input.txt  [optional flags]

Optional flags:
  -h, --help        Show this help message and exit.
  -p, --plot        Plot submitted light curve with most similar curve in database
  -r, --rebuild     Recreates light curve files vantage point indexes (Run automatically on first use)
  -d, --demo        Loads a random time series from sample data folder and runs similarity search

For example:

python3 ./simsearchutil.py -d

python3 ./simsearchutil.py sample_data/51886.dat_folded -p

### Developers:

Created by Team 2 (Jonne Seleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah)