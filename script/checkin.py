#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from Bio import SeqIO
from script.config import Config


def is_fagb(filename):
    filetype = ""
    with open(filename, "r") as handle1:
        fasta = SeqIO.parse(handle1, "fasta")
        if any(fasta):
            filetype = "fa"
    with open(filename, "r") as handle2:
        gbk = SeqIO.parse(handle2, "gb")
        if any(gbk):
            filetype = "gb"
    return filetype


def get_fagb(runID: str, input_file: str, execution_type: str, config: Config):
    try:
        filetype = is_fagb(input_file)
    except:
        print(
            "ERROR: The input file is not a standard FASTA/GenBank format! Please check !"
        )
        sys.exit()

    if not filetype:
        print(
            "ERROR: The input file is not a standard FASTA/GenBank format! Please check !"
        )
        sys.exit()

    else:
        if filetype == "fa":
            fasta_file = input_file
            seq_record = SeqIO.parse(input_file, "fasta")
            if len(list(seq_record)) == 1:
                # TODO: do we need this rename here?
                pass
                # for seq_records in SeqIO.parse(input_file, "fasta"):
                #     seq_records.id = runID
                #     SeqIO.write(seq_records, newfile, "fasta")
            elif execution_type == "Metagenome":
                filetype = "multifa"
            else:
                print("ERROR: Input file accepted for one sequence only.")
                sys.exit()
        else:
            # We need to create the required files first in the "workdir"
            seq_record = SeqIO.parse(input_file, "gb")
            if len(list(seq_record)) == 1:
                i = 0
                for seq_records in SeqIO.parse(input_file, "gb"):
                    for seq_feature in seq_records.features:
                        if seq_feature.type == "CDS":
                            if "locus_tag" in seq_feature.qualifiers:
                                continue
                            else:
                                i += 1
                                if i > 10:
                                    print(
                                        "ERROR: Too many CDS do not have locus_tag in GenBank input file! Please check or try FASTA format input!"
                                    )
                                    sys.exit()
                    if len(set(list(str(seq_records.seq)))) == 1:
                        print(
                            "ERROR: The uploaded file is not a standard GenBank format! Please check or try a FASTA format input!"
                        )
                        sys.exit()

                    else:
                        seq_records.id = runID
                        gbk_file = config.gb_dir / (runID + ".gbk")
                        fasta_file = config.fa_dir / (runID + ".fa")
                        SeqIO.write(seq_records, gbk_file, "gb")
                        SeqIO.write(seq_records, fasta_file, "fasta")
            else:
                print("ERROR: Input file accepted for one sequence only.")
                sys.exit()

    return fasta_file, filetype
