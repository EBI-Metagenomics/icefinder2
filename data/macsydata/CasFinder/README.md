# CasFinder: annotation of CRISPR-Cas systems 

This set of MacSyFinder's models are dedicated to the genomic detection of CRISPR-Cas systems. 

This new version CasFinder v3.1.0 contains 535 HMM proteins profiles and can detect 6 different **types** and 37 different **subtypes** of CRISPR-Cas systems.
	
 |  | CAS_Class1 | CAS_Class1| CAS_Class1| CAS_Class2 | CAS_Class2 | CAS_Class2| 
 | ------ | ------ | ------ |------ | ------ |------ | ------ |
 | **Type** |  Type-I | Type-III | Type-IV | Type-II | Type-V | Type-VI | 
 | **Subtype** |  Subtype-I | Subtype-III | Subtype-IV | Subtype-II | Subtype-V | Subtype-VI | 
| | I-A |  III-A | IV-A | II-A | V-A | VI-A | 
| | I-B |  III-B | IV-B | II-B | V-B | VI-B | 
| | I-C |  III-C | IV-C | II-C | V-C | VI-C | 
| | I-D |  III-D | IV-D |  | V-D | VI-D | 
| | I-E |  III-E | IV-E |  | V-E | VI-X | 
| | I-F |  III-F |  |  | V-F | VI-Y | 
| | I-G |     | | | V-G | | 
| |     |     |  |  | V-H |  | 
| |     |     |  |  | V-I |  | 
| |     |     |  |  | V-K |  |

The known *cas* operons have from 1 to 13 genes encoding very diverse proteins, among which several nucleases and helicases with DNA and/or RNA binding domains.
Putative *cas* genes are searched by sequence similarity using HMM protein profiles downloaded from  [[1]](https://doi.org/10.1093/nar/gky425)[[2]](https://doi.org/10.1038/s41579-019-0299-x)[[3]](https://doi.org/10.1038/s41592-021-01124-4). The assignment of a gene to a given system is decided based on its compliance with the content and organization defined in different models (one model per type and subtype). Within a model, components can be defined as mandatory, accessory, neutral or forbidden (see [MacSyFinder's documentation](http://macsyfinder.readthedocs.io/en/latest/)). 

- *Mandatory* components are typically genes that are specific to a subtype (or type) of CRISPR-Cas systems.
- *Accessory* components correspond to genes that can be shared between different subtypes (or types). 
- *Neutral* components are genes associated with known CRISPR-Cas systems that are not specific to them. 
- *Forbidden* components correspond to genes that cannot belong to a defined subtype and are useful for distinguishing closely related subtypes (e.g. CAS_Class2-Subtype-II-A, CAS_Class2-Subtype-II-C).

Cas systems are identified at the type or subtype level using increasingly specific system descriptions. Atypical systems (i.e. not respecting any of the previously defined rules) or degraded systems (i.e. not allowing to distinguish the type of the system) are identified as **CAS_Clusters**. As CRISPR-Cas systems are very diverse (in terms of size and composition), the different decision rules are even more diverse, and all specifications and models are available (in the directory called **definitions**).

> Note: All models previously defined in CasFinder v2.0.3 include in [CRISPRCasFinder](https://crisprcas.i2bc.paris-saclay.fr/CrisprCasFinder/Index) [[1]](https://doi.org/10.1093/nar/gky425) have been rewritten to be compatible with the new version of macsyfinder v2.0rc7 and updated to take into account the most recently proposed nomenclature [[2]](https://www.nature.com/articles/s41579-019-0299-x)[[3]](https://doi.org/10.1038/s41592-021-01124-4).
These latest versions of macsyfinder and CasFinder will be integrated in CRISPRCasFinder as soon as possible.

> Note: Currently, macsyfinder v2.0rc4 and CasFinder v3.0.0 are used in [DefenseFinder](https://defense-finder.mdmparis-lab.com/) [[5]](https://doi.org/10.1038/s41467-022-30269-9), a program detecting a wide range of anti-phage systems, including CRISPR-Cas systems. These latest versions of macsyfinder and CasFinder will be integrated in CRISPRCasFinder as soon as possible.

This new version : 

* provides the possibility to detect more subtypes than the previous ones
* greatly improves the detection of tandem systems 
* improves the detection of degenerated and atypical systems
* with macsyfinder version 1, it was necessary to run the models providing typing and subtyping independently. This is no longer necessary, and all models can be (and should be) considered at the same time (see below).


To summarize : 

|CasFinder  | | #HMM profiles | # Types | # Subtypes |
| ------ | ---- | ------ |------ | ------ | 
|CasFinder v3.1.0 | latest | 535 | 6 | 37 |
|CasFinder v3.0.0 | [DefenseFinder](https://defense-finder.mdmparis-lab.com/) | 517 | 6 | 33 |
|CasFinder v2.0.3* | [CRISPRCasFinder](https://crisprcas.i2bc.paris-saclay.fr/CrisprCasFinder/Index) | 119 | 6 | 17 |

(*)only comptatible with mascyfinder versions 1


## Installation and Usage with MacSyFinder

First, the `macsyfinder` program should be [installed](http://macsyfinder.readthedocs.io/en/latest/). This will also install the `macsydata` tool that enables to easily install this package of MacSyFinder models from this repository. 

The basic commands to run are then:
```sh
    macsydata install CasFinder
```
to install the CasFinder package. 
```sh
    macsyfinder --db-type ordered_replicon \
		--sequence-db myproteins.fasta \
		--models CasFinder all 		
```

to run the search on your favorite organism's genome (see [MacSyFinder's documentation](http://macsyfinder.readthedocs.io/en/latest/)). 
```sh
    macsyfinder --db-type ordered_replicon \
        	--replicon-topology circular \
		--sequence-db myproteins.fasta \
		--models CasFinder all 		
```	
if you are are lucky enough to deal with a **complete genome**!

> Note: `--models CasFinder all ` is required for highest annotation specificity.

It has to be noted that to ensure the highest annotation specificity, it is recommended to search for **all** available models (systems) in the package at once. An independent search of the subtypes (one by one) could lead to a wrong prediction, as some subtypes are very close genetically to each other.
> Note: `--replicon-topology circular ` is required for complete genome.

We also strongly recommend for **complete genomes** to use the following options: --db-type ordered_replicon and --replicon-topology circular.
First, because if the user considers the genome as **unordered**, then only the composition of the *cas* genes in the genome will be provided and no type, subtype or CAS cluster will be offered.
Secondly, because the systems can be located between the end and the start of the replicon (especially in plasmids). The **circular** option solves this circularity problem.

In this new version, all models are challenged, and those with the highest score and best completeness will be considered the best predictions.
It is therefore important that the parameters specified in the model_conf.xml file are not changed, at the risk of affecting the calculation of the system scores. To ensure the highest annotation specificity, the accessory and exchangeable genes weight should be 1 and the profile coverage 0.4 (as specified in the model-conf.xml file)
```sh
--accessory-weight 1
--exchangeable-weight 1
--coverage-profile 0.4
 ```
These parameters should not be changed by the user in the command line.
The predictions of the CRISPR-Cas systems are reported in the output file named *best_solution.tsv* (for more details, see the [MacSyFinder documentation](https://macsyfinder.readthedocs.io/en/latest/user_guide/outputs.html)).

## References

- [1] Couvin, D., Bernheim, A., Toffano-Nioche, C., Touchon, M.,  Michalik, J.,  Néron, B., Rocha E.P.C,  Vergnaud, G., Gautheret, D., Pourcel, C. (2018)
CRISPRCasFinder, an update of CRISRFinder, includes a portable version, enhanced performance and integrates search for Cas proteins
Nucleic Acids Research, Volume 46, Issue W1, 2 July 2018, Pages W246–W251. [doi:10.1093/nar/gky425](https://doi.org/10.1093/nar/gky425)

- [2] Makarova, K.S., Wolf, Y.I., Iranzo, J., et al. (2020) 
 Evolutionary classification of CRISPR–Cas systems: a burst of class 2 and derived variants. Nat Rev Microbiol 18, 67–83 (2020). [doi:10.1038/s41579-019-0299-x](https://doi.org/10.1038/s41579-019-0299-x)
 
- [3] Xu, C., Zhou, Y., Xiao, Q. et al. (2021)
  Programmable RNA editing with compact CRISPR–Cas13 systems from uncultivated microbes. 
  Nat Methods 18, 499–506 (2021).[doi:10.1038/s41592-021-01124-4](https://doi.org/10.1038/s41592-021-01124-4)
 
- [4] Abby, S.S., Bertrand, N., Ménager, H., Touchon, M., Rocha, E.P.C (2014).
  MacSyFinder: A Program to Mine Genomes for Molecular Systems with an Application to CRISPR-Cas Systems.
  PLoS ONE, 9 (10), pp. e110726. [doi:10.1371/journal.pone.0110726](http://dx.doi.org/10.1371/journal.pone.0110726)

- [5] Tesson, F., Hervé, A., Mordret, E., Touchon, M., d’Humières, C., Cury J., Bernheim, A. (2022) 
  Systematic and quantitative view of the antiviral arsenal of prokaryotes. 
  Nat Commun 13, 2561. [doi:10.1038/s41467-022-30269-9](https://doi.org/10.1038/s41467-022-30269-9)


