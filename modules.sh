# run `conda deactivate` if you have conda

# Load available modules
module load \
Python/3.10.4-GCCcore-11.3.0 \
Biopython/1.79-foss-2022a \
matplotlib/3.5.2-foss-2022a \

# Load pip packages not available as modules
# https://hpc.vub.be/docs/software/additional_software/#installing-additional-python-packages
pip install --user \
hydra-core \
hydra-submitit-launcher \
hydra-joblib-launcher \
memray \

# make sure you run this file with `source` and $(which python) is something like
# /apps/gent/RHEL8/zen2-ib/software/Python/3.10.8-GCCcore-12.2.0/bin/python
# NOT /usr/bin/python