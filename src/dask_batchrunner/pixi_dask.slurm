#!/bin/bash -l
#SBATCH --output=%x_%j.out	# Output file
#SBATCH --error=%x_%j.err	# Error file
#SBATCH --time=00:01:00	# 1 minute time limit

# Resources:
#SBATCH --partition=donphan
# do not request node, so tasks can be distributed across nodes
#SBATCH -n 3      # tasks requested
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=2g # RAM per task

srun --export=ALL python dask_launcher.py