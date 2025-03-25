# ICEfinder 2.0

ICEfinder 2.0 - Detecting Integrative and Conjugative Elements in Bacteria.

> [!NOTE]
> This repo contains a copy of https://tool2-mml.sjtu.edu.cn/ICEberg3/Download.html.

## Welcome to use ICEfinder local version

> [!Tip]
> ICEfinder also has a web version, you can access it easily by https://tool2-mml.sjtu.edu.cn/ICEberg3/ICEfinder.php.

## Installation

The local version of ICEfinder2 has been tested in CentOS Linux release 7.7.1908.

To install ICEfinder2, just download the file 'ICEfinder2_linux.tar.gz' from the 'Download' [webpage](https://tool2-mml.sjtu.edu.cn/ICEberg3/Download.html) and then decompress it:

```bash
$ tar -xvzf ICEfinder2_linux.tar.gz
```

ICEfinder2 has multiple programs dependency: 

Hmmer, version 3.1 or greater
BLAST, version 2.10.1+ or greater
Kraken, version 2.0.9-beta or greater (For Metagenome)
seqkit, version 0.12.0
prodigal, V2.6.3
prokka, V1.14.6
defensefinder, v1.0.9
macsyfinder, 2.0rc6
And you need to specify the installation path for the software in the config.ini file.

ICEfinder2 also relies on Python library dependencies:
Biopython
ete3

To test and get familiar with the ICEfinder, you can test the demo files we provide in the 'example/input_demo' directory,
```bash
run `python ICEfinder2.py -i example/input_demo/file -t Single/Metagenome`. You can also compare your output in the 'result'
```
to the results in the directory 'example/result_demo'.

> [!NOTE]
> DefenseFinder and MacSyFinder currently support the specified versions only. We will be conducting version updates later.

## Input data

At present, ICEfinder2 accepts the bacterial genome sequences in the GenBank or FASTA format. 
And You can input a single bacterial sequence (in either FASTA or GenBank format) or multiple metagenome sequences (in FASTA format) for analysis.

Example of list file format:
CP003200.1.gb
NC_000964.3.gb
SRS146999.fna

> [!NOTE]
> A. These three GenBank files are the example for the detection of G- T4SS-type ICEs, G+ T4SS-type ICEs and metagenome ICEs respectively.
> B. For Genbank format, only accept the standard gbk files that contain single contig with full sequence.

## OUTPUT
The output files in the directory 'result/' may include:

### `*_info.json`

The summary json file about the input genome.

```json
 {
     "JobID": "CP003200.1",
     "Submission date": "Fri Oct 1 00:18:44 2023",
     "Sequence name": "CP003200.1",
     "Length": "5333942 bp",
     "GC Content": "57.48 %"
 }
```

### `*_ICEsum.json`

The summary json file about the putative ICE/IME.
```json
 {
     "id": "1",
     "region": "Region1",
     "location": "3433540..3495705",
     "length": "62166",
     "gc": "52.46",
     "type": "T4SS-type ICE",
     "detail": "CP003200.1_ICE4"
    }
```

### `*_ICE*_info.json`

Detailed feature information for each ICE

```json
 {
     "Type": "T4SS-type ICE",
     "Location (nt)": "3433540..3495705",
     "Length (bp)": "62166",
     "GC Content (%)": "52.46",
     "oriT seq": "CCGATTAGGCGCGACCAACCCCTTTAAAGCAGCGTTCCCATTTTTTCGAGCTTGCGAAGAAAAAATAGGCTAAACGCGCGTCTTAAAGGGGTTGGTCGCGCGTAGCGTGCGACGGTGTGCCGCC",
     "DRs": "attL:3433540..3433556(CAGTCAGAGGAGCCAA)  attR:3495689..3495705(CAGTCAGAGGAGCCAA)",
     "Relaxase Type": "MOBC",
     "Mating pair formation systems": "typeT",
     "Close to tRNA": "tRNA-Asn (3433479..3433555) [+]"
 }
```

### `*_ICE*.html, *_ICE*_gene.json`

Detailed gene structure information for each ICE along with web-based visualization results.
```json
 [
    {
        "gene": "KPHS_34550",
        "pos": "3428319..3428709 [-], 391",
        "prod": "hypothetical protein",
        "featu": "Flank"
    },

  ....

    {
        "gene": "KPHS_35020",
        "pos": "3500665..3502288 [-], 1624",
        "prod": "putative lysophospholipase",
        "featu": "Flank"
    }
 ]
```

## Contact

If you have any question for ICEfinder 2.0, please feel free to contact the authors:

- hyou@sjtu.edu.cn
- m.wang@sjtu.edu.cn
