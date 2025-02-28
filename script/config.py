import configparser
from dataclasses import dataclass
import tempfile
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

@dataclass
class Config:
    tmp_dir: Path
    run_id_dir: Path
    fa_dir: Path
    gb_dir: Path
    databases_dir: Path
    # binaries
    # kraken: str
    defensefinder: str
    blastp: str
    blastn: str
    seqkit: str
    prodigal: str
    prokka: str
    prokka_cores: int
    macsyfinder: str
    hmmsearch: str
    hmmscan: str
    vmatch: str
    aragorn: str
    mkvtree: str
    # IceFinder2 static files (css, js files)
    icefinder2_static_directory: Path
    # Reference databases
    # krakenDB: Path
    defensefinder_database: Path
    virulence_blast_database: Path
    resfinder_blast_database: Path
    metal_blast_database: Path
    degradation_blast_database: Path
    symbiosis_blast_database: Path
    transposase_blast_database: Path
    orit_blast_database: Path
    ete3ncbi_database: Path
    # Results / outdirectory
    outdir: Path


def get_configuration(run_id: str, config_file: str,outdir_path: str) -> Config:
    configuration = configparser.ConfigParser()
    configuration.read(config_file)

    tmp_dir = Path(tempfile.mkdtemp())
    fa_dir = tmp_dir / "fasta"
    gb_dir = tmp_dir / "gbk"
    run_id_dir = tmp_dir / run_id
    fa_dir.mkdir(parents=True, exist_ok=True)
    gb_dir.mkdir(parents=True, exist_ok=True)
    run_id_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Directories")
    logging.info(f"TMP for transient files {tmp_dir}")
    logging.info(f"Fasta directory {fa_dir}")
    logging.info(f"GBK directory {gb_dir}")
    logging.info(f"Run ID directory {run_id_dir}")

    outdir = Path(f"{outdir_path}/{run_id}")
    outdir.mkdir(exist_ok=True)

    databases_dir = Path(configuration.get("Param", "databases_dir"))

    if not databases_dir.exists():
         raise FileNotFoundError(f"Missing database base path: {databases_dir}")

    ete3ncbi_database = Path(configuration.get("Param", "ete3ncbi_database"))

    defensefinder_database = databases_dir / "macsydata"
    virulence_blast_database = databases_dir/ "virulence"
    resfinder_blast_database = databases_dir / "resfinder"
    metal_blast_database = databases_dir / "metal"
    degradation_blast_database = databases_dir / "degradation"
    symbiosis_blast_database = databases_dir / "symbiosis"
    transposase_blast_database =  databases_dir / "transposase"
    orit_blast_database = databases_dir / "oriT_db"

    return Config(
        tmp_dir=tmp_dir,
        run_id_dir=run_id_dir,
        fa_dir=fa_dir,
        gb_dir=gb_dir,
        icefinder2_static_directory=configuration.get("Param", "icefinder2_static_directory"),
        # kraken=configuration.get("Param", "kraken"),
        # krakenDB=configuration.get("Param", "krakenDB"),
        defensefinder=configuration.get("Param", "defensefinder"),
        blastp=configuration.get("Param", "blastp"),
        blastn=configuration.get("Param", "blastn"),
        seqkit=configuration.get("Param", "seqkit"),
        prodigal=configuration.get("Param", "prodigal"),
        prokka=configuration.get("Param", "prokka"),
        prokka_cores=4,
        macsyfinder=configuration.get("Param", "macsyfinder"),
        hmmsearch=configuration.get("Param", "hmmsearch"),
        hmmscan=configuration.get("Param", "hmmscan"),
        vmatch=configuration.get("Param", "vmatch"),
        aragorn=configuration.get("Param", "aragorn"),
        mkvtree=configuration.get("Param", "mkvtree"),
        databases_dir=databases_dir,
        ete3ncbi_database=ete3ncbi_database,
        defensefinder_database=defensefinder_database,
        virulence_blast_database=virulence_blast_database,
        resfinder_blast_database=resfinder_blast_database,
        metal_blast_database=metal_blast_database,
        degradation_blast_database=degradation_blast_database,
        symbiosis_blast_database=symbiosis_blast_database,
        transposase_blast_database=transposase_blast_database,
        orit_blast_database=orit_blast_database,
        outdir=outdir
    )
