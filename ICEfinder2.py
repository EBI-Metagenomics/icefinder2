#!/public/software/miniconda3/bin/python
# -*- coding: utf-8 -*-
#
# ICEfinder: Detecting Integrative and Conjugative Elements in Bacteria.
# Meng Wang on Sep-4-2023
# School of Life Sciences & Biotechnology, Shanghai Jiao Tong University
# Version 2.0 - Sep 4, 2023
########################################################################

import os
import argparse
from script.checkin import get_fagb
from script.single import _single
from script.metaICE import _meta
from script.config import get_param

param = get_param()
workdir = param[0]
tmp_dir = os.path.join(workdir,'tmp')
fa_dir = os.path.join(tmp_dir,'fasta') 
gb_dir = os.path.join(tmp_dir,'gbk')

def add_arguments_to_parser(parser):

	parser.add_argument('-v', '--version', action='version', version='2.0',
                        help="Show ICEfinder version")
	parser.add_argument('-i', '--input', type=str, required=True,
                        help='FASTA/Genbank format file, Genbank format file accepted only for single genome.')
	parser.add_argument('-t', '--type', type=str, required=True,
                        help='Genome Type: Single/Metagenome')

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='ICEfinder', usage='python ICEfinder.py -i fasta_file/genbank_file -t Single/Metagenome',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	add_arguments_to_parser(parser)
	args = parser.parse_args()
	intype = args.type
	input_file = args.input

	if not os.path.exists(tmp_dir):
		os.mkdir(tmp_dir)
	if not os.path.exists(gb_dir):
		os.mkdir(gb_dir)
	if not os.path.exists(fa_dir):
		os.mkdir(fa_dir)

	runID = file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]

	infile,filetype = get_fagb(runID,input_file,intype)

	if intype == 'Single':
		_single(runID,infile,filetype)
	else:
		_meta(runID,infile)

	print(runID+' done!!')
