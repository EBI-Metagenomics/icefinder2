#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from pathlib import Path

from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Applications import NcbiblastnCommandline

from script.helpers import run_command
from script.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_deferense_finder(run_id: str, annotation_faa: Path, config: Config):

    defense_finder_output = config.run_id_dir / ("defense_" + run_id)

    command = [
        config.defensefinder,
        "run",
        "-w", "8",
        "--models-dir", config.defensefinder_database,
        "-o", defense_finder_output,
        annotation_faa
    ]

    run_command(command)

    # Read the results from the output file
    dfdict = {}
    defense_fider_genes_tsv = defense_finder_output / f"{run_id}_defense_finder_genes.tsv"
    try:
        with open(defense_fider_genes_tsv) as dfres:
            for line in dfres.readlines():
                lines = line.strip().split("\t")
                if lines[0] != "replicon":
                    dfdict[lines[1]] = lines[2].replace("__", ",")
    except FileNotFoundError:
        logging.error(f"Output file not found: {defense_fider_genes_tsv}")
        return {}

    return dfdict


def isblast(faa_file: str, IS_out: str, config: Config):
    blastp_cline = NcbiblastpCommandline(
        cmd=config.blastp,
        query=faa_file,
        db=config.transposase_blast_database,
        evalue=0.0001,
        num_threads=20,
        max_hsps=1,
        num_descriptions=1,
        num_alignments=1,
        outfmt="6 std slen stitle",
        out=IS_out,
    )
    logging.info(f"Command: {blastp_cline}")
    blastp_cline()


def vfblast(faa_file: str, VF_out: str, config: Config):
    blastp_cline = NcbiblastpCommandline(
        cmd=config.blastp,
        query=faa_file,
        db=config.virulence_blast_database,
        evalue=0.0001,
        num_threads=20,
        max_hsps=1,
        num_descriptions=1,
        num_alignments=1,
        outfmt="6 std slen stitle",
        out=VF_out,
    )
    logging.info(f"Command: {blastp_cline}")
    blastp_cline()


def argblast(fa_file: str, arg_out: str, config: Config):
    blastp_cline = NcbiblastnCommandline(
        cmd=config.blastn,
        query=fa_file,
        db=config.resfinder_blast_database,
        evalue=0.0001,
        num_threads=20,
        max_hsps=1,
        num_descriptions=1,
        num_alignments=1,
        outfmt="6 std slen stitle",
        out=arg_out,
    )
    logging.info(f"Command: {blastp_cline}")
    blastp_cline()


def metalblast(faa_file: str, metal_out: str, config: Config):
    blastp_cline = NcbiblastpCommandline(
        cmd=config.blastp,
        query=faa_file,
        db=config.metal_blast_database,
        evalue=0.0001,
        num_threads=20,
        max_hsps=1,
        num_descriptions=1,
        num_alignments=1,
        outfmt="6 std slen stitle",
        out=metal_out,
    )
    logging.info(f"Command: {blastp_cline}")
    blastp_cline()


def popblast(faa_file: str, pop_out: str, config: Config):
    blastp_cline = NcbiblastpCommandline(
        cmd=config.blastp,
        query=faa_file,
        db=config.degradation_blast_database,
        evalue=0.0001,
        num_threads=20,
        max_hsps=1,
        num_descriptions=1,
        num_alignments=1,
        outfmt="6 std slen stitle",
        out=pop_out,
    )
    logging.info(f"Command: {blastp_cline}")
    blastp_cline()


def symblast(faa_file:str , sym_out: str, config: Config):
    blastp_cline = NcbiblastpCommandline(
        cmd=config.blastp,
        query=faa_file,
        db=config.symbiosis_blast_database,
        evalue=0.0001,
        num_threads=20,
        max_hsps=1,
        num_descriptions=1,
        num_alignments=1,
        outfmt="6 std slen stitle",
        out=sym_out,
    )
    logging.info(f"Command: {blastp_cline}")
    blastp_cline()


def havalue(value, out):
    blast_filter = {}
    for line in open(out, "r").readlines():
        lines = line.strip().split("\t")
        havalue = (int(lines[3]) / int(lines[12])) * float(lines[2]) / 100
        if havalue >= float(value):
            blast_filter[lines[0]] = lines[1].split("|")[1]
    return blast_filter


def get_blast_results(run_id: str, annotation_faa: Path, annotation_ffn: Path, config: Config):
    """
    Executes various BLAST analyses on input sequence files and retrieves the results.

    This function performs multiple BLAST analyses (IS, VF, ARG, METAL, POP, SYM) 
    on the provided input files based on the specified run ID and configuration. 
    It generates output files for each analysis and returns dictionaries containing 
    the results.

    :param run_id: The identifier for the current run, used to locate input and output files.
    :type run_id: str
    :param config: A configuration object containing paths for input and output directories.
    :type config: Config

    :return: A tuple containing dictionaries for each analysis:
        - argdict: Results from ARG analysis.
        - vfdict: Results from VF analysis.
        - isdict: Results from IS analysis.
        - dfdict: Results from the deferense finder.
        - metaldict: Results from METAL analysis.
        - popdict: Results from POP analysis.
        - symdict: Results from SYM analysis.
    :rtype: tuple
    """

    annotation_faa_str = str(annotation_faa)
    annotation_ffn_str = str(annotation_ffn)

    # Define output file paths
    arg_output_path = config.run_id_dir / "arg.m8"
    vf_output_path = config.run_id_dir / "vf.m8"
    is_output_path = config.run_id_dir / "is.m8"
    pop_output_path = config.run_id_dir / "pop.m8"
    metal_output_path = config.run_id_dir / "metal.m8"
    sym_output_path = config.run_id_dir / "sym.m8"

    # Execute BLAST analyses
    isblast(annotation_faa_str, is_output_path, config)
    vfblast(annotation_faa_str, vf_output_path, config)
    argblast(annotation_faa_str, arg_output_path, config)
    metalblast(annotation_faa_str, metal_output_path, config)
    popblast(annotation_faa_str, pop_output_path, config)
    symblast(annotation_ffn_str, sym_output_path, config)

    # Retrieve results from each analysis
    is_results = havalue("0.64", is_output_path)
    vf_results = havalue("0.64", vf_output_path)
    arg_results = havalue("0.81", arg_output_path)
    metal_results = havalue("0.64", metal_output_path)
    pop_results = havalue("0.64", pop_output_path)
    sym_results = havalue("0.64", sym_output_path)

    # Get deferense finder results
    deferense_results = get_deferense_finder(run_id, annotation_faa, config)

    return arg_results, vf_results, is_results, deferense_results, metal_results, pop_results, sym_results
