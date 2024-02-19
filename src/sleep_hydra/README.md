# Sleep example with Hydra

This example implements a task that sleeps for `{runtime}` seconds and holds a Numpy array of `{memory}` megabytes in size. The runtime can be measured with `timeit` and the memory usage with `memray`.

Because the multirun output folder has a fixed structure, you can parse the folder with a script and plot the benchmarking metrics. This example script creates plots in the multirun folder when executing the script with a benchmark option.
```bash
ml swap cluster/donphan
# launch interactive session
ACTIVATE=src/sleep_hydra SCRIPT=bash srun --pty runner.pbs
# execute Hydra like normal
python src/sleep_hydra/main.py +sweep='{runtime: 1, memory: 1},{runtime: 2, memory: 10},{runtime: 3, memory: 100}' task.runtime='${sweep.runtime}' task.memory='${sweep.memory}' benchmark=all hydra/launcher=joblib -m
python scripts/sleep_plots.py
```

Note that the configuration `task.sleep=1,2,3 benchmark=runtime,memory` would require 6 tasks and fail on an interactive cluster with a 5 task queue limit.

The runtime plot shows the 3 tasks with increasing sleep length.
<img src="../../resources/sleep_runtime.png">

The memory plot shows the 3 tasks with increasing memory usage.
<img src="../../resources/sleep_memory.png">

## Different launch options explained

### Run locally one task

Note that by default Hydra stores the configuration, logs and output of each run in a unique folder `outputs/{DAY}/{TIME}/`. The output folder contains a `.hydra/` folder specifying the complete configuration used for the run and any output file written to `cfg.output_dir`.

```bash
python src/sleep_hydra/main.py
```
OUTPUT:
```log
Output directory : /kyukon/data/gent/vo/000/gvo00070/vsc43257/hydra_hpc_example/outputs/2023-10-20/11-09-33
[2023-10-20 11:09:34,986][__main__][INFO] - Process ID 1595501 executed task {'runtime': 1, 'memory': 10} in 1.000080016994616 seconds
```

### Run locally multiple tasks sequentially

Note that the multiple runs now each have an output folder in `multirun/{DAY}/{TIME}/`. All process IDs are the same, as the tasks run sequentially in the same process.

```bash
python src/sleep_hydra/main.py task.runtime=1,2,3 -m
```
OUTPUT:
```log
[2023-10-20 11:10:43,219][HYDRA] Launching 3 jobs locally
[2023-10-20 11:10:43,219][HYDRA]        #0 : task.runtime=1
Output directory : /kyukon/data/gent/vo/000/gvo00070/vsc43257/hydra_hpc_example/multirun/2023-10-20/11-10-42/0
[2023-10-20 11:10:44,407][__main__][INFO] - Process ID 1597253 executed task {'runtime': 1, 'memory': 10} in 1.0000840639986563 seconds
[2023-10-20 11:10:44,411][HYDRA]        #1 : task.runtime=2
Output directory : /kyukon/data/gent/vo/000/gvo00070/vsc43257/hydra_hpc_example/multirun/2023-10-20/11-10-42/1
[2023-10-20 11:10:46,501][__main__][INFO] - Process ID 1597253 executed task {'runtime': 2, 'memory': 10} in 2.0000894780096132 seconds
[2023-10-20 11:10:46,503][HYDRA]        #2 : task.runtime=3
Output directory : /kyukon/data/gent/vo/000/gvo00070/vsc43257/hydra_hpc_example/multirun/2023-10-20/11-10-42/2
[2023-10-20 11:10:49,586][__main__][INFO] - Process ID 1597253 executed task {'runtime': 3, 'memory': 10} in 3.0000770180195104 seconds
```

### Run locally multiple tasks in parallel

Note that all process IDs are the different, as each tasks runs in it's own process.

```bash
python src/sleep_hydra/main.py task.runtime=1,2,3 hydra/launcher=joblib -m
```
OUTPUT:
```log
[2023-10-20 11:12:03,084][HYDRA] Joblib.Parallel(n_jobs=-1,backend=loky,prefer=processes,require=None,verbose=0,timeout=None,pre_dispatch=2*n_jobs,batch_size=auto,temp_folder=None,max_nbytes=None,mmap_mode=r) is launching 3 jobs
[2023-10-20 11:12:03,084][HYDRA] Launching jobs, sweep output dir : multirun/2023-10-20/11-11-57
[2023-10-20 11:12:03,085][HYDRA]        #0 : task.runtime=1
[2023-10-20 11:12:03,085][HYDRA]        #1 : task.runtime=2
[2023-10-20 11:12:03,085][HYDRA]        #2 : task.runtime=3
Output directory : /kyukon/data/gent/vo/000/gvo00070/vsc43257/hydra_hpc_example/multirun/2023-10-20/11-11-57/0
Output directory : /kyukon/data/gent/vo/000/gvo00070/vsc43257/hydra_hpc_example/multirun/2023-10-20/11-11-57/1
Output directory : /kyukon/data/gent/vo/000/gvo00070/vsc43257/hydra_hpc_example/multirun/2023-10-20/11-11-57/2
[2023-10-20 11:12:04,881][__main__][INFO] - Process ID 1598945 executed task {'runtime': 1, 'memory': 10} in 1.0003418159903958 seconds
[2023-10-20 11:12:05,912][__main__][INFO] - Process ID 1598949 executed task {'runtime': 2, 'memory': 10} in 2.000080882018665 seconds
[2023-10-20 11:12:06,913][__main__][INFO] - Process ID 1598952 executed task {'runtime': 3, 'memory': 10} in 3.000079121993622 seconds
```

### Run on Slurm with the local test config

Note that by default no logging and print statements are shown, these are stored at `.submitit/` in the output directory next to the output of each run. [`submitit_local`](https://github.com/facebookincubator/submitit/blob/4cf1462d7216f9dcc530daeb703ce07c37cf9d72/submitit/local/local.py#LL99) uses `subprocess` to run the tasks locally, so the functionality and output is similar to joblib.

```bash
python src/sleep_hydra/main.py task.runtime=1,2,3 hydra/launcher=submitit_local -m
```
OUTPUT:
```log
[2023-10-20 11:12:57,639][HYDRA] Submitit 'local' sweep output dir : multirun/2023-10-20/11-12-57
[2023-10-20 11:12:57,641][HYDRA]        #0 : task.runtime=1
[2023-10-20 11:12:57,645][HYDRA]        #1 : task.runtime=2
[2023-10-20 11:12:57,653][HYDRA]        #2 : task.runtime=3
```
### Run on Slurm using the HPC job scheduler

Can only be executed on the HPC cluster.

```bash
python src/sleep_hydra/main.py task.runtime=1,2,3 hydra/launcher=submitit_slurm -m
```
OUTPUT:
```log
[2023-10-20 11:15:04,918][HYDRA] Submitit 'slurm' sweep output dir : multirun/2023-10-20/11-15-04
[2023-10-20 11:15:04,920][HYDRA]        #0 : task.runtime=1
[2023-10-20 11:15:04,924][HYDRA]        #1 : task.runtime=2
[2023-10-20 11:15:04,928][HYDRA]        #2 : task.runtime=3
```

## Specifying resources

For a full list of settings, see the HPC documentation. To see available parameters, run:
```bash
python src/sleep_hydra/main.py hydra/launcher=submitit_slurm --cfg hydra -p hydra.launcher
```

Slurm job with 2 CPUs and 4GB of RAM:
```bash
python src/sleep_hydra/main.py hydra/launcher=submitit_slurm hydra.launcher.cpus_per_task=2 hydra.launcher.mem_gb=4GB
```

## Benchmarking overhead

We can benchmark both runtime and memory in two ways besides `benchmark=runtime` and `benchmark=memory`:

`benchmark=all` will run the task twice, once with `timeit` and once with `memray`.
```bash
# seconds
[(3, 3.000507133983774), (2, 2.0004843850038014), (1, 1.0004661950224545)]
# megabytes
[(100, 95.39), (10, 9.559), (1, 0.999444)]
```

- `benchmark=hybrid` will run the task once with `timeit` inside the `memray` wrapper.
```bash
# seconds
[(3, 3.013979399984237), (2, 2.013261186017189), (1, 1.015038490993902)]
# megabytes
[(100, 96.392), (10, 10.561), (1, 1.001554)]
```

The overhead of `benchmark=hybrid` is negligable for large sizes, it's more important to run multiple times and report the variance. 