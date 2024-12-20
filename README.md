# Hydra Slurm example

This is a collection of examples of how to use Hydra to launch jobs locally and on a Slurm cluster. For more background, read [the Hydra documentation](https://hydra.cc/docs).


## Local setup

Install conda and create a new environment:

```bash
conda env update -f env.yaml --prune
```

add .local/bin to your PATH
```bash
export PATH=$PATH:$HOME/.local/bin
```

## HPC setup

Depending on the infrastructure and cluster, you maybe need to change some modules
```
module swap cluster/donphan
source modules.sh
```

You can always reset this setup using `module purge`.

## Examples

- [src/sleep_pbs/README.md](./src/sleep_pbs/README.md) is an example used to explain interactive and job-based scheduling with PBS and SLURM. The example sleep script is benchmarked for runtime and memory usage with `timeit` and `memray`.
- [src/sleep_hydra/README.md](./src/sleep_hydra/README.md) is the same sleep example and benchmarking, but executed with the Hydra framework. More powerful and flexible, but also more complex.
- [src/dask_jobqueue/README.md](./src/dask_jobqueue/README.md) is an example of how to use Hydra and submitit to launch a Dask jobqueue through the SLURM scheduler. 
- [src/frequencies_hydra/README.md](./src/frequencies_hydra/README.md) is the counting frequencies example with benchmarking. It uses a Python-only configuration, based on hydra-zen.
- [src/dask_batchrunner/README.md](./src/dask_batchrunner/README.md) is an example of how to use the SLURMRunner from dask-jobqueue to launch a Dask cluster on SLURM. It uses either Pixi or vsc-venv to manage the environment. It currently does not use MPI.
- [src/dask_mympi/README.md](./src/dask_mympi/README.md) is an example of how to use the vsc-mympirun to launch a Dask cluster on SLURM. It uses  vsc-venv to manage the environment.

## Common patterns

There are various usage patterns in Hydra to make your life easier. For more information, see the [Hydra documentation on common patterns](https://hydra.cc/docs/patterns/configuring_experiments/).

## Possible improvements

- Allow benchmarking using platform instrumentation and diagnostics ([Slurm](https://saeyslab.github.io/dambi-hpc-guide/advanced/benchmarking.html), [Dask](https://docs.dask.org/en/stable/diagnostics-local.html), Prefect...)
- Optuna sweeper
- Usage with Prefect 

## References

- [hydra_submitit_launcher](https://github.com/facebookresearch/hydra/tree/main/plugins/hydra_submitit_launcher/example)