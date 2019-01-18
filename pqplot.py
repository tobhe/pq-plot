#!/usr/bin/env python3

# Copyright (c) 2019, Tobias Heider <heidert@nm.ifi.lmu.de>
#
# This file is part of pq-plot. For licensing information please see the file
# LICENSE which is included with pq-plot.

import csv
import sys
import logging
import argparse
import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
import numpy as np

lattice = [
    'kyber1024',
    'FrodoKEM-976',
    'newhope1024cca',
    'NTRU-HRSS-KEM',
    # Saber
    'light_saber',
    'saber',
    'fire_saber',
    # NTRUPrime:
    'sntrup4591761',
    'ntrulpr4591761',
    'ntru-kem-1024',
    'ntrulpr4591761',
    'Titanium_CCA_std',
    'Titanium_CCA_med',
    'Titanium_CCA_hi',
    'Titanium_CCA_super',
    'Ding512',
    'Ding1024',
]

ntru = [
    'NTRU-HRSS-KEM',
    'sntrup4591761',
    'ntrulpr4591761',
    'ntru-kem-443',
    'ntru-kem-743',
    'ntru-kem-1024',
    'ntrulpr4591761',
]

strongest = [
    ''
]


def main():

    parser = argparse.ArgumentParser(description='Plot pq-kem data')
    parser.add_argument('-c', '--category', default='all', help='category of KEMs to plot')
    parser.add_argument('-x', '--xaxis', default='pk', help='column of table to plot on x-axis')
    parser.add_argument('-y', '--yaxis', default='Keypair Average x10^3', help='column of table to plot on y-axis')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    parser.add_argument('-a', '--annotate', action='store_true', help='annotate nodes')
    parser.add_argument('filename', help='input file')
    args = parser.parse_args()

    x_data = args.xaxis
    y_data = args.yaxis

    # Configure logger
    logger = logging.getLogger(__name__)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Select KEM category
    if args.category == 'lattice':
        logger.debug("Plotting lattice KEMs")
        whitelist = lattice
    elif args.category == 'ntru':
        logger.debug("Plotting NTRU KEMs")
        whitelist = ntru
    elif args.category == 'all':
        whitelist = []
    elif args.category == 'all-presentation':
        whitelist = []
    else:
        logger.error('Invalid category: {}, exiting...'.format(args.category))
        sys.exit()

    # read csv file
    with open(args.filename, newline='') as csvfile:

        ax = pl.subplot(111)

        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Specific Implementation']

            if args.category == 'all-presentation':
                try:
                    # Draw Scatterplot
                    xval = float(row[x_data].replace(',', '')) / 1000000
                    yval = float(row[y_data].replace(',', '')) / 1024

                    color = 'r'
                    if row['Problem Category'] == 'Codes':
                        color = 'xkcd:sky blue'
                    elif row['Problem Category'] == 'Lattices':
                        color = 'xkcd:green'
                    elif row['Problem Category'] == 'Isogeny':
                        color = 'xkcd:orange'
                    elif row['Problem Category'] == 'Multivariate':
                        color = 'xkcd:pink'

                    pl.scatter(xval, yval, c=color)

                    # if row['Specific Implementation'] == 'SIKEp751':
                    #   pl.annotate("SIKE", xy=(xval, yval),
                    #               xytext=(-5, -5), textcoords='offset points')
                    if args.annotate:
                        pl.annotate(name, xy=(xval, yval),
                                    xytext=(5, -10), textcoords='offset points')
                    logger.debug("{}: {}, {}".format(name, xval, yval))

                except Exception as e:
                    print("Error: Invalid value for {}: {}".format(
                        row['Specific Implementation'], e))
                    pass
            elif args.category != 'all':
                if name in whitelist:
                    try:
                        xval = float(row[x_data].replace(',', ''))
                        yval = float(row[y_data].replace(',', ''))
                        pl.scatter(xval, yval)
                        pl.annotate(name, xy=(xval, yval),
                                    xytext=(0, 5), textcoords='offset points')
                        logger.debug("{}: {}, {}".format(name, xval, yval))

                    except Exception as e:
                        print("Error: Invalid value for {}: {}".format(
                            row['Specific Implementation'], e))
                        pass
            else:
                try:
                    xval = float(row[x_data].replace(',', ''))
                    yval = float(row[y_data].replace(',', ''))
                    pl.scatter(xval, yval)
                    pl.annotate(name, xy=(xval, yval),
                                xytext=(0, 5), textcoords='offset points')
                    logger.debug("{}: {}, {}".format(name, xval, yval))

                except Exception as e:
                    print("Error: Invalid value for {}: {}".format(
                        row['Specific Implementation'], e))
                    pass

        ax.set_title("Public-key Size to Encryption Speed Comparison")
        ax.set_xlim(left=0.0)
        ax.set_ylim(bottom=0.0)
        ax.grid()

        if args.category == 'all-presentation':
            pl.axhline(y=1.28, xmin=0, xmax=5000 ,linewidth=1, color='red')

            # Specific formatting
            red_patch = mpatches.Patch(color='red', label='RSA-2048')
            green_patch = mpatches.Patch(color='xkcd:green', label='Lattices')
            blue_patch = mpatches.Patch(color='xkcd:sky blue', label='Codes')
            orange_patch = mpatches.Patch(color='xkcd:orange', label='Isogeny')
            pink_patch = mpatches.Patch(color='xkcd:pink', label='Multivariate')
            pl.legend(handles=[red_patch, green_patch, blue_patch, orange_patch, pink_patch])
            pl.ticklabel_format(style = 'plain')
            pl.xlabel("Encryption Speed in 10^6 CPU Cycles")
            pl.ylabel("Public Key Size in KiB")

        else:
            pl.xlabel(x_data)
            pl.ylabel(y_data)
        pl.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
