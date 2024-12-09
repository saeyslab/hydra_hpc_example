This example uses the dask-jobqueue [SLURMRunner](https://jobqueue.dask.org/en/latest/runners-overview.html) as an alternative to `dask-mpi.initialize()`. It does not use MPI currently.


Dask-MPI: https://mpi.dask.org/en/latest/index.html
Experimental new runners: https://github.com/jacobtomlinson/dask-runners
Submitit: https://github.com/facebookincubator/submitit

VSC specific:
https://github.com/hpcugent/vsc-mympirun
https://docs.hpc.ugent.be/Linux/setting_up_python_virtual_environments

## Run

Run batch job via vsc-venv environment.
```
sbatch job.slurm
```

Run batch job via Pixi environment. Install [Pixi](https://pixi.sh/latest/) first.
```bash
pixi r sbatch pixi_dask.slurm
```

