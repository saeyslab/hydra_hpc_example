# Hydra Slurm example

This is an example of how to use Hydra to launch jobs locally and on a Slurm cluster. For more background, read https://hydra.cc/docs/plugins/submitit_launcher/. This is an extended example of https://github.com/facebookresearch/hydra/tree/main/plugins/hydra_submitit_launcher/example.

The application in `my_app.py` is a Python script that prints the process and task ID. The task is sleeping for a number of seconds, the amount of seconds is defined by the task id. The application is launched with Hydra, which reads in the config files in `configs/` and allows overriding various aspects of the execution.

## Local setup

Install conda and create a new environment:

```bash
conda env update -f env.yaml --prune
```

On the HPC, 

## Different launch options

### Run locally one task

Note that by default Hydra stores the configuration, logs and output of each run in a unique folder `outputs/{DAY}/{TIME}/`. The output folder contains a `my_app.log` file and a `.hydra/` folder specifying the complete configuration used for the run.

```bash
python my_app.py
```

### Run locally multiple tasks sequentially

Note that the multiple runs now each have an output folder in `multirun/{DAY}/{TIME}/`. All process IDs are the same, as the tasks run sequentially in the same process.

```bash
python my_app.py task=1,2,3 -m
```

### Run locally multiple tasks in parallel

Note that all process IDs are the different, as each tasks runs in it's own process.

```bash
python my_app.py task=1,2,3 hydra/launcher=joblib -m
```

### Run on Slurm with the local test config

Note that by default no logging and print statements are shown, these are stored at `.submitit/` in the output directory next to the output of each run. [`submitit_local`](https://github.com/facebookincubator/submitit/blob/4cf1462d7216f9dcc530daeb703ce07c37cf9d72/submitit/local/local.py#LL99) uses `subprocess` to run the tasks locally, so the functionality and output is similar to joblib.

```bash
python my_app.py task=1,2,3 hydra/launcher=submitit_local -m
```

### Run on Slurm using the HPC job scheduler

Can only be executed on the HPC cluster.

```bash
python my_app.py task=1,2,3 hydra/launcher=submitit_slurm -m
```

## Specifying resources

For a full list of settings, see the HPC documentation. To see available parameters, run:
```
python my_app.py hydra/launcher=submitit_slurm --cfg hydra -p hydra.launcher
```

Slurm job with 2 CPUs and 4GB of RAM:
```
python my_app.py hydra/launcher=submitit_slurm hydra.launcher.cpus_per_task=2 hydra.launcher.mem_gb=4GB
```

## Common patterns

There are various usage patterns in Hydra to make your life easier. For more information, see the [Hydra documentation](https://hydra.cc/docs/patterns/configuring_experiments/).

## Possible improvements

- More complex tasks
- Nicer plots
- Hydra Structured configs instead of YAML files
- Allow benchmarking using platform instrumentation and diagnostics ([Slurm](https://saeyslab.github.io/dambi-hpc-guide/advanced/benchmarking.html), [Dask](https://docs.dask.org/en/stable/diagnostics-local.html), Prefect...)
- More complex Hydra config
- Optuna sweeper
- Usage with Dask
- Usage with Prefect 