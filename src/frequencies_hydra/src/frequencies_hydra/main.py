import logging
import os
from pathlib import Path

import numpy as np
import submitit
from hydra_zen import load_from_yaml, zen

from frequencies_hydra.config import BenchmarkConfig, store

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


def do_task(method, data):
    log.debug(method, data)
    method(data())


def main(method, data, benchmark: BenchmarkConfig) -> None:
    from hydra_zen import to_yaml

    print(f"method:\n{to_yaml(method)}")
    print(f"data:\n{to_yaml(data)}")
    print(f"benchmark:\n{to_yaml(benchmark)}")

    try:
        # see if running on a submitit cluster
        env = submitit.JobEnvironment()
        log.info(f"Running with {env}")
    except RuntimeError:
        pass

    cfg = load_from_yaml(Path(".") / ".hydra" / "hydra.yaml")
    output_dir = Path(cfg.hydra.runtime.output_dir).resolve()

    print(f"Output directory : {output_dir}")
    if benchmark.name in ["runtime", "all"]:
        import timeit

        runtime = timeit.timeit(
            lambda: do_task(method, data), number=1, globals=globals()
        )
        log.info(
            f"Process ID {os.getpid()} executed task {method} {data} in {runtime} seconds"
        )
        runtime_file = output_dir / "runtime.txt"
        runtime_file.write_text(f"{method} {data} {runtime}")
    if benchmark.name in ["memory", "all"]:
        import memray

        memray_file = output_dir / "memray.bin"
        log.info("Starting memory tracking")
        with memray.Tracker(
            file_name=memray_file,
            native_traces=True,
            follow_fork=True,
            memory_interval_ms=1,
        ):
            try:
                do_task(method, data)
            except BaseException as e:
                print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
    if benchmark.name in ["hybrid"]:
        import timeit

        import memray

        memray_file = output_dir / "memray.bin"
        log.info("Starting memory tracking")
        runtime = None
        with memray.Tracker(
            file_name=memray_file,
            native_traces=True,
            follow_fork=True,
            memory_interval_ms=1,
        ):
            try:
                runtime = timeit.timeit(
                    lambda: do_task(method, data), number=1, globals=globals()
                )
            except BaseException as e:
                print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
        log.info(
            f"Process ID {os.getpid()} executed task {cfg.task} in {runtime} seconds"
        )
        runtime_file = output_dir / "runtime.txt"
        runtime_file.write_text(f"{cfg.task.runtime} {runtime}")

    if benchmark.name in ["off"]:
        do_task(method, data)


# Wrapping `train_and_eval` with `zen` makes it compatible with Hydra as a task function
#
# We must specify `pre_call` to ensure that pytorch lightning seeds everything
# *before* any of our configs are instantiated (which will initialize the pytorch
# model whose weights depend on the seed)
# pre_seed = zen(lambda seed: pl.seed_everything(seed))
task_function = zen(
    main,
    # pre_call=pre_seed
)

if __name__ == "__main__":
    # Add all of the configs, that we put in hydra-zen's (local) config store,
    # to Hydra's (global) config store.
    store.add_to_hydra_store(overwrite_ok=True)

    # Generate the CLI For task_function
    task_function.hydra_main(
        config_name="config",
        config_path=None,
        version_base="1.3",
    )
    # Hydra will accept configuration options from
    # the CLI and merge them with the stored configs.
    #
    # hydra-zen then instantiates these configs
    # -- creating the subconfig instances --
    # and passes them to the main function, running the code.
    #
    # Hydra records the exact, reproducible config
    # for each run, and saves the results in an
    # auto-generated, configurable output dir
