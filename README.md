[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fowler-lab/bashthebug-consensus-dataset/HEAD)

# BashTheBug dataset for finding the optimal consensus method

## Purpose

This repository contains the raw data tables used in the below scientific preprint that is currently under review at a journal. Its aim is to ensure that the results can be reproduced by other people and therefore a Jupyter notebook is included that allows one to recreate nearly all the figures and tables in the manuscript from the raw data tables.

> *BashTheBug: a crowd of volunteers reproducibly and accurately measure the minimum inhibitory concentrations of 13 antitubercular drugs from photographs of 96-well broth microdilution plates*
> 
> Fowler PW, Wright C, Spiers H, Zhu T, Baeten EML, Hoosdally SW, Gibertoni Cruz AL, Roohi A, Kouchaki S, Walker TM, Peto TEA, Miller G, Lintott C, Clifton D, Crook DW, Walker AS, The CRyPTIC Consortium
> 
> bioRxiv preprint [doi:10.1101/2021.07.20.453060](https://doi.org/10.1101/2021.07.20.453060)

This README will be updated when the manuscript is published in a scientific journal.

## Data tables

These are described in the schema below and are found, as gzipped `csv` files in `tables/`

![title](DATA_SCHEMA.png)

There are two main raw data tables:

`CLASSIFICATIONS` is derived from the CSV exported by the Zooniverse by a Python package [bashthebug](https://github.com/fowler-lab/bashthebug) which is built off a generic Zooniverse class provided by another Python package [pyniverse](https://github.com/fowler-lab/pyniverse).

`PHENOTYPES` contains the measurements (stated here as dilutions) made by laboratory scientists as part of the study published below:

> *Validating a 14-Drug Microtiter Plate Containing Bedaquiline and Delamanid for Large-Scale Research Susceptibility Testing of Mycobacterium tuberculosis*
> 
> Rancoita PMV, Cugnata F, Gibertoni-Cruz AL, Borroni E, Hoosdally SJ, Walker TM, Grazian C,  Davies TJ, Peto TEA, Crook DW, Fowler PW, Cirillo DM and the CRyPTIC consortium
>
> Antimicrob Agent Chemo 2018;62:e00344 [doi:10.1128/AAC.00344-18](https://doi.org/10.1128/AAC.00344-18)

As described in the paper, during that study the laboratory scientists made measurements using a Thermo Fisher Vizion (`VZ`), a mirrored box (`MB`) and a microscope (`MS`). Since the Vizion also took a photograph, a measurement taken by some software, AMyGDA (`IM`).

AMyGDA is described in this paper and the software is available from [here](https://github.com/fowler-lab/amygda).

> Automated detection of bacterial growth on 96-well plates for high-throughput drug susceptibility testing of Mycobacterium tuberculosis.
>
> Fowler PW, Gibertoni Cruz AL, Hoosdally SJ, Jarrett L, Borroni E, et al.  
> 
> Microbiology 2018;164:1522–1530. [doi:10.1099/mic.0.000733](https://doi.org/10.1099/mic.0.000733)
