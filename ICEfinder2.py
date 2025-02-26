#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ICEfinder: Detecting Integrative and Conjugative Elements in Bacteria.
# Meng Wang on Sep-4-2023
# School of Life Sciences & Biotechnology, Shanghai Jiao Tong University
# Version 2.0.1 - Sep 4, 2023
########################################################################


import argparse
from pathlib import Path

from script.checkin import get_fagb
from script.single import _single
from script.metaICE import _meta
from script.config import get_configuration


def add_arguments_to_parser(parser):
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="2.0",
        help="Show ICEfinder version",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="The IceFinder2 configuration.ini file."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="FASTA/Genbank format file, Genbank format file accepted only for single genome.",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        required=True,
        help="Output directory for the results"
    )
    parser.add_argument(
        "-t", "--type", type=str, required=True, help="Genome Type: Single/Metagenome"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ICEfinder",
        usage="python ICEfinder.py -i fasta_file/genbank_file -t Single/Metagenome",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    add_arguments_to_parser(parser)
    args = parser.parse_args()
    input_file = args.input
    execution_type = args.type

    file_name_without_extension = Path(input_file).extension
    runID = file_name_without_extension

    configuration = get_configuration(runID, args.config, args.outdir)

    infile, filetype = get_fagb(runID, input_file, execution_type, configuration)

    if execution_type == "Single":
        _single(runID, infile, filetype, configuration)
    else:
        _meta(runID, infile, configuration)

    print(runID + " done!!")
