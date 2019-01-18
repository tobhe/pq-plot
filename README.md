# PQ-plot

A small python script to plot post-quantum KEM benchmarks published on [safecrypto.eu](https://www.safecrypto.eu/pqclounge/software-analysis-kem/).

## Usage

```
usage: pqplot.py [-h] [-c CATEGORY] [-x XAXIS] [-y YAXIS] [-v] [-a] filename

Plot pq-kem data

positional arguments:
  filename              input file

optional arguments:
  -h, --help            show this help message and exit
  -c CATEGORY, --category CATEGORY
                        category of KEMs to plot
  -x XAXIS, --xaxis XAXIS
                        column of table to plot on x-axis
  -y YAXIS, --yaxis YAXIS
                        column of table to plot on y-axis
  -v, --verbose         increase output verbosity
  -a, --annotate        annotate nodes
```

## LEGAL

The pq-bench.py file is released under the 2-clause BSD license, see [LICENSE](LICENSE.txt).
The supplied csv file is taken from the [safecrypto.eu online pqc benchmarks](https://www.safecrypto.eu/pqclounge/software-analysis-kem/).
