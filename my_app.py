# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import time
from pathlib import Path
import os
import subprocess

import hydra
import submitit
from omegaconf import DictConfig

log = logging.getLogger(__name__)

def do_task(task: int) -> None:
    time.sleep(task)

@hydra.main(version_base=None, config_path="configs", config_name="main")
def my_app(cfg: DictConfig) -> None:
    try:
        # see if running on a submitit cluster
        env = submitit.JobEnvironment()
        log.info(f"Running with {env}")
    except RuntimeError:
        pass
    print(f"Output directory : {cfg.output_dir}")
    output_dir = Path(cfg.output_dir).resolve()
    match cfg.benchmark:
        case 'runtime':
            import timeit
            runtime = timeit.timeit(f"do_task({cfg.task})", number=1, globals=globals())
            log.info(f"Process ID {os.getpid()} executed task {cfg.task} in {runtime} seconds")
            runtime_file = output_dir / 'runtime.txt'
            runtime_file.write_text(f'{cfg.sleep} {runtime}')
        case 'memory':
            import memray
            memray_file = output_dir / 'memray.bin'
            memory_file: Path = output_dir / 'memory.txt'
            log.info('Starting memory tracking')
            with memray.Tracker(
                file_name=memray_file,
                native_traces=True,
                follow_fork=True,
                memory_interval_ms=1,
            ):
                try:
                    do_task(cfg.task)
                except BaseException as e:
                    print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
        case _:
            do_task(cfg.task)

if __name__ == "__main__":
    my_app()