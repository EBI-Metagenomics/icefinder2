import configparser
from dataclasses import dataclass
import tempfile
from pathlib import Path


@dataclass
class Config:
    tmp_dir: Path
    run_id_dir: Path
    fa_dir: Path
    gb_dir: Path
    databases_dir: Path
    # binaries
    kraken: str
    defensefinder: str
    blastp: str
    blastn: str
    seqkit: str
    prodigal: str
    prokka: str
    macsyfinder: str
    hmmsearch: str
    hmmscan2: str
    vmatch: str
    aragorn: str
    mkvtree: str
    # Reference databases
    krakenDB: Path
    defensefinder_database: Path
    virulence_blast_database: Path
    resfinder_blast_database: Path
    metal_blast_database: Path
    degradation_blast_database: Path
    symbiosis_blast_database: Path
    transposase_blast_database: Path
    ete3ncbi_database: Path
    # Results / outdirectory
    outdir: Path


def get_configuration(run_id: str, config_file: str, outdir_path: str) -> Config:
    configuration = configparser.ConfigParser()
    configuration.read(config_file)

    tmp_dir = Path(tempfile.mkdtemp())
    fa_dir = tmp_dir / "fasta"
    gb_dir = tmp_dir / "gbk"
    fa_dir.mkdir(parents=True, exist_ok=True)
    gb_dir.mkdir(parents=True, exist_ok=True)

    outdir = Path(outdir_path)
    outdir.mkdir(exist_ok=True)

    base_databases = Path(configuration["databases_dir"])
    defensefinder_database = base_databases / "macsydata"
    virulence_blast_database = base_databases/ "virulence"
    resfinder_blast_database =base_databases / "resfinder"
    metal_blast_database = base_databases / "metal"
    degradation_blast_database = base_databases / "degradation"
    symbiosis_blast_database = base_databases / "symbiosis"
    transposase_blast_database =  base_databases / "transposase"
    
    # Check them now
    if not defensefinder_database.exists():
        raise FileNotFoundError(f"Missing database: {defensefinder_database}")
    
    if not virulence_blast_database.exists():
        raise FileNotFoundError(f"Missing database: {virulence_blast_database}")
    
    if not resfinder_blast_database.exists():
        raise FileNotFoundError(f"Missing database: {resfinder_blast_database}")
    
    if not metal_blast_database.exists():
        raise FileNotFoundError(f"Missing database: {metal_blast_database}")
    
    if not degradation_blast_database.exists():
        raise FileNotFoundError(f"Missing database: {degradation_blast_database}")
    
    if not symbiosis_blast_database.exists():
        raise FileNotFoundError(f"Missing database: {symbiosis_blast_database}")
    
    if not transposase_blast_database.exists():
        raise FileNotFoundError(f"Missing database: {transposase_blast_database}")

    return Config(
        tmp_dir=tmp_dir,
        run_id_dir=tmp_dir / run_id,
        fa_dir=fa_dir,
        gb_dir=gb_dir,
        kraken=configuration.get("Param", "kraken"),
        krakenDB=configuration.get("Param", "krakenDB"),
        defensefinder=configuration.get("Param", "defensefinder"),
        blastp=configuration.get("Param", "blastp"),
        blastn=configuration.get("Param", "blastn"),
        seqkit=configuration.get("Param", "seqkit"),
        prodigal=configuration.get("Param", "prodigal"),
        prokka=configuration.get("Param", "prokka"),
        macsyfinder=configuration.get("Param", "macsyfinder"),
        hmmsearch=configuration.get("Param", "hmmsearch"),
        defensefinder_database=defensefinder_database,
        virulence_blast_database=virulence_blast_database,
        resfinder_blast_database=resfinder_blast_database,
        metal_blast_database=metal_blast_database,
        degradation_blast_database=degradation_blast_database,
        symbiosis_blast_database=symbiosis_blast_database,
        transposase_blast_database=transposase_blast_database,
        outdir=outdir
    )
