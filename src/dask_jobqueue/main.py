import logging
import time
from pathlib import Path
import os
from distributed import fire_and_forget

import hydra
import submitit
from omegaconf import DictConfig
import numpy as np

log = logging.getLogger(__name__)

def get_memory_object(mb):
    # an int in Python is usually 32 bits or 4 bytes
    n_nums = int(mb * 1_000_000 / 4)
    return list(range(n_nums))

def get_memory_object_numpy(mb):
    # np.int is 8 bits or 1 byte
    n_nums = int(mb * 1_000_000)
    arr = np.zeros((n_nums), dtype=np.int8)
    return arr

def do_task_memory(task, client) -> None:
    mem_value = get_memory_object_numpy(task['memory'])
    do_task(task, client)
    del mem_value

def do_subtask(task):
    time.sleep(task["runtime"])

def do_task(task, client):
    from distributed import get_client
    log.debug(task)
    future = client.submit(do_subtask, task)
    future.result()

@hydra.main(version_base=None, config_path="configs", config_name="main")
def main(cfg: DictConfig) -> None:
    try:
        # see if running on a submitit cluster
        env = submitit.JobEnvironment()
        log.info(f"Running with {env}")
    except RuntimeError:
        pass
    print(f"Output directory: {cfg.output_dir}")
    print(f"Path venv: {cfg.path_venv}")
    print(f"Path modules: {cfg.path_modules}")
    output_dir = Path(cfg.output_dir).resolve()

    from dask.distributed import Client
    from distributed import performance_report

    with hydra.utils.instantiate(cfg.cluster) as cluster, Client(cluster) as client:
        with performance_report(filename=(output_dir / "dask-report.html")):
            if cfg.benchmark in ['runtime', 'all']:
                import timeit
                runtime = timeit.timeit(lambda: do_task(cfg.task, client), number=1, globals=globals())
                log.info(f"Process ID {os.getpid()} executed task {cfg.task} in {runtime} seconds")
                runtime_file = output_dir / 'runtime.txt'
                runtime_file.write_text(f'{cfg.task.runtime} {runtime}')
            if cfg.benchmark in ['memory', 'all']:
                import memray
                memray_file = output_dir / 'memray.bin'
                log.info('Starting memory tracking')
                with memray.Tracker(
                    file_name=memray_file,
                    native_traces=True,
                    follow_fork=True,
                    memory_interval_ms=1,
                ):
                    try:
                        do_task_memory(cfg.task, client)
                    except BaseException as e:
                        print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
            if cfg.benchmark in ['hybrid']:
                import timeit
                import memray

                memray_file = output_dir / 'memray.bin'
                log.info('Starting memory tracking')
                runtime = None
                with memray.Tracker(
                    file_name=memray_file,
                    native_traces=True,
                    follow_fork=True,
                    memory_interval_ms=1,
                ):
                    try:
                        runtime = timeit.timeit(lambda: do_task_memory(cfg.task, client), number=1, globals=globals())
                    except BaseException as e:
                        print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
                log.info(f"Process ID {os.getpid()} executed task {cfg.task} in {runtime} seconds")
                runtime_file = output_dir / 'runtime.txt'
                runtime_file.write_text(f'{cfg.task.runtime} {runtime}')

            if cfg.benchmark in ['off']:
                do_task(cfg.task, client)


if __name__ == "__main__":
    main()
