#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import logging

from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Applications import NcbiblastnCommandline

from script.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_deferense_finder(runID, config: Config):
    if not os.path.exists(config.run_id_dir / (runID + ".locus_tag.faa")):
        infaa = config.gb_dir / (runID + ".faa")
    else:
        infaa = config.run_id_dir / (runID + ".locus_tag.faa")

    dfout = config.run_id_dir / ("defense_" + runID)

    defcmd = [
        config.defensefinder,
        "run",
        "-w", "8",
        "--models-dir", config.defensefinder_database,
        "-o", str(dfout),
        str(infaa)
    ]

    try:
        subprocess.run(defcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info(f"DefenseFinder command executed successfully for runID: {runID}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while running DefenseFinder for runID: {runID}")
        logging.error(f"Return code: {e.returncode}")
        logging.error(f"Error message: {e.stderr.decode()}")  # Log standard error output
        return {}

    # Read the results from the output file
    dfdict = {}
    try:
        with open(os.path.join(dfout, "defense_finder_genes.tsv")) as dfres:
            for line in dfres.readlines():
                lines = line.strip().split("\t")
                if lines[0] != "replicon":
                    dfdict[lines[1]] = lines[2].replace("__", ",")
    except FileNotFoundError:
        logging.error(f"Output file not found: {os.path.join(dfout, 'defense_finder_genes.tsv')}")
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
    blastp_cline()


def havalue(value, out):
    blast_filter = {}
    for line in open(out, "r").readlines():
        lines = line.strip().split("\t")
        havalue = (int(lines[3]) / int(lines[12])) * float(lines[2]) / 100
        if havalue >= float(value):
            blast_filter[lines[0]] = lines[1].split("|")[1]
    return blast_filter


def getblast(runID, config):
    arg_out = config.run_id_dir / "arg.m8"
    vf_out = config.run_id_dir / "vf.m8"
    is_out = config.run_id_dir / "is.m8"
    pop_out = config.run_id_dir / "pop.m8"
    metal_out = config.run_id_dir / "metal.m8"
    sym_out = config.run_id_dir / "sym.m8"

    if not os.path.exists(config.run_id_dir / (runID + ".locus_tag.faa")):
        infaa = config.gb_dir / (runID + ".faa")
        infa = config.gb_dir / (runID + ".ffn")
    else:
        infaa = config.run_id_dir / (runID + ".locus_tag.faa")
        infa = config.run_id_dir  / (runID + ".locus_tag.spaceHeader.ffn")

    isblast(infaa, is_out)
    vfblast(infaa, vf_out)
    argblast(infa, arg_out)

    metalblast(infaa, metal_out)
    popblast(infaa, pop_out)
    symblast(infa, sym_out)

    isdict = havalue("0.64", is_out)
    vfdict = havalue("0.64", vf_out)
    argdict = havalue("0.81", arg_out)
    metaldict = havalue("0.64", metal_out)
    popdict = havalue("0.64", pop_out)
    symdict = havalue("0.64", sym_out)

    dfdict = get_deferense_finder(runID, config)

    return argdict, vfdict, isdict, dfdict, metaldict, popdict, symdict
