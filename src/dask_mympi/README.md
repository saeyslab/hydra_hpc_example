
Dask-MPI: https://mpi.dask.org/en/latest/index.html
Experimental new runners: https://github.com/jacobtomlinson/dask-runners
Submitit: https://github.com/facebookincubator/submitit

VSC specific:
https://github.com/hpcugent/vsc-mympirun
https://docs.hpc.ugent.be/Linux/setting_up_python_virtual_environments

## vsc-venv (does not work currently)

Run batch job
```
ml switch cluster/donphan
qsub launcher.pbs
```

Run interactively
```
ml switch cluster/donphan
qsub -I
cd $PBS_O_WORKDIR
ml load vsc-venv
source vsc-venv --activate --requirements requirements.txt --modules modules.txt
```

The output log will have a line `Work done`.