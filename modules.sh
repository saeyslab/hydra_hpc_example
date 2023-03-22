#!/bin/bash

module load \
Python/3.10.8-GCCcore-12.2.0 \
Biopython/1.81-foss-2022b \

# https://hpc.vub.be/docs/software/additional_software/#installing-additional-python-packages
pip install --user hydra-core \
hydra-submitit-launcher \
hydra-joblib-launcher \
memray \