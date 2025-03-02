FROM mambaorg/micromamba:2.0.5

ENV VERSION="2.0"

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="mambaorg/micromamba:2.0.5"
LABEL version="${VERSION}"
LABEL software="ICEfinder2"
LABEL website="https://tool2-mml.sjtu.edu.cn/ICEberg3/ICEfinder.php"
LABEL license="http://creativecommons.org/licenses/by-nc-sa/4.0/"

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yml /tmp/env.yml

RUN micromamba install -y -n base -f /tmp/env.yml \
    && micromamba install -y -n base conda-forge::procps-ng \
    && micromamba env export --name base --explicit > environment.lock \
    && cat environment.lock \
    && micromamba clean -a -y


ENV PATH="$MAMBA_ROOT_PREFIX/bin:$PATH"

USER root

WORKDIR /icefinder2-2.0

# Create a config.ini file and configure Kraken DB path dynamically
RUN cat <<EOL > /icefinder2-2.0/config.ini
[Param]
kraken=$(which kraken2)
krakenDB=/krakenDB
defensefinder=$(which defense-finder)
blastp=$(which blastp)
blastn=$(which blastn)
seqkit=$(which seqkit)
prodigal=$(which prodigal)
prokka=$(which prokka)
macsyfinder=$(which macsyfinder)
hmmsearch=$(which hmmsearch)
hmmscan2=$(which hmmscan)
vmatch=$(which vmatch)
aragorn=$(which aragorn)
mkvtree=$(which mkvtree)
EOL

ENV PATH="$MAMBA_ROOT_PREFIX/bin:/icefinder2-2.0:$PATH"

WORKDIR /icefinder2-2.0
