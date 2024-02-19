# Sleep example with PBS

This example implements a task that sleeps for `{runtime}` seconds and holds a Numpy array of `{memory}` megabytes in size. The runtime can be measured with `timeit` and the memory usage with `memray`.

## Installation

### Interactive installation via compute node

This is the recommended approach as it allows debugging the environment installation.

```bash
# On default login node (doduo)
ml swap cluster/donphan
# On donphan login node
qsub -I
# On donphan compute node
cd $PBS_O_WORKDIR
INSTALL=src/sleep_pbs bash runner.pbs
# CTRL+D to logout from the compute node back to the login node
```

### Job-based installation via compute node

```bash
ml swap cluster/donphan
# Submit to queue, will be executed on donphan compute node
qsub runner.pbs -v INSTALL=src/sleep_pbs 
```

Note that activating the environment on the login node instead of the compute node can work, but installing and running can result in an error when loading the Python interpreter e.g. `Illegal instruction`. The modules are created for the compute nodes, not the login nodes. 
```bash
# On default login node (doduo)
ml swap cluster/donphan
# Make sure all environment are deactivated
# Note source instead of bash! can work on donphan login node if already installed
PBS_O_WORKDIR=$PWD ACTIVATE=src/sleep_pbs source runner.pbs
# will fail on donphan login node
PBS_O_WORKDIR=$PWD INSTALL=src/sleep_pbs bash runner.pbs
# ++ python --version
# Illegal instruction     (core dumped)
```

## Run a sleep job

### Interactive

```bash
# On default login node (doduo)
ml swap cluster/donphan
# On donphan login node
qsub -I
# On donphan compute node
cd $PBS_O_WORKDIR
ACTIVATE=src/sleep_pbs script=main.py bash runner.pbs --runtime 1 --memory 1 --output_dir tmp_output
# CTRL+D to logout from the compute node back to the login node
# benchmark results are in ./tmp_output/
```

### Job-based

```bash
ml swap cluster/donphan
# Submit to queue, will be executed on donphan compute node and uses parameter shorthand
qsub runner.pbs -v ACTIVATE=src/sleep_pbs,script=main.py,args="-r 1 -m 1 -o tmp_output"
```

## Multi-jobs

We want to benchmark three different jobs for the parameters `{runtime}` and `{memory}` and plot the results. 
The format of the `tmp_sweep_output/` folder is similar to the `multirun/` folder of Hydra. A current limitation is that everything is executed serially. For more information, look at `parallel`, `joblib` and the [HPC multi-job documentation](https://docs.hpc.ugent.be/macOS/multi_job_submission/).

### Sweep with Python

```bash
ACTIVATE=src/sleep_pbs script=sweep.py bash runner.pbs -s sweep.csv -o tmp_sweep_output
ml load Python matplotlib
python scripts/sleep_plots.py -r src/sleep_pbs/tmp_sweep_output
```

The plots of the benchmarking results show that the measured runtime and memory usage are as expected.

## Using SLURM instead of PBS

You can use the `runner.pbs` shell script to submit a job to the cluster with SLURM in the same way. You just have to replace `qsub -I` with `srun` and `qsub` with `sbatch`. SLURM auto-sets the PBS_O_WORKDIR to the current directory from where you submit. PBS specific comments in the script will not work.

Installation
```bash
ml swap cluster/donphan
INSTALL=src/sleep_pbs srun runner.pbs
```

Run 
```bash
ACTIVATE=src/sleep_pbs script=main.py sbatch runner.pbs --help
```
