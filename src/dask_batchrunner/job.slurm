#!/bin/bash -l
#SBATCH --partition=donphan	
#SBATCH --output=%x_%j.out	# Output file
#SBATCH --error=%x_%j.err	# Error file
#SBATCH --time=0-00:10:00	# 10 minute time limit

# Resources:
#SBATCH --ntasks=3 --mem-per-cpu=2g # 3 tasks, 2GB of RAM per task

# Load envionrment
ml load vsc-venv
source vsc-venv --activate --requirements requirements.txt --modules modules.txt

# Run code
srun --export=ALL python dask_launcher.py
