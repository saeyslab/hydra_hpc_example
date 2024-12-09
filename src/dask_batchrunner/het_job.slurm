#!/bin/bash -l
#SBATCH --partition=donphan	# Run on tier3
#SBATCH --output=%x_%j.out	# Output file
#SBATCH --error=%x_%j.err	# Error file
#SBATCH --time=0-00:10:00	# 10 minute time limit

# Resources for first group:
#SBATCH --ntasks=1 --mem-per-cpu=1g # 1 tasks, 1GB of RAM per task

# Separator for groups:
#SBATCH hetjob

# Resources for second group:
#SBATCH --ntasks=2 --mem-per-cpu=2g # 2 tasks, 2GB of RAM per task

# TODO: move this to each srun invocation
ml load vsc-venv
source vsc-venv --activate --requirements requirements.txt --modules modules.txt

# Script for first group:
srun --pack-group 0 python main.py

# Script for second group:
srun --pack-group 1 python main.py
