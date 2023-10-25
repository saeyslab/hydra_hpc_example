import logging
import time
from pathlib import Path
import os

import numpy as np

logging.basicConfig(level=logging.INFO)

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

def do_task_memory(runtime, memory) -> None:
    mem_value = get_memory_object_numpy(memory)
    do_task(runtime)
    del mem_value

def do_task(runtime):
    time.sleep(runtime)

def main(runtime, memory, benchmark, output_dir) -> None:
    log.debug(f'runtime {runtime}')
    log.debug(f'memory {memory}')
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory : {output_dir}")
    if benchmark in ['runtime', 'all']:
        import timeit
        seconds = timeit.timeit(lambda: do_task(runtime), number=1, globals=globals())
        log.info(f"Process ID {os.getpid()} executed task runtime={runtime},memory={memory} in {seconds} seconds")
        runtime_file = output_dir / 'runtime.txt'
        runtime_file.write_text(f'{runtime} {seconds}')
    if benchmark in ['memory', 'all']:
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
                do_task_memory(runtime=runtime, memory=memory)
            except BaseException as e:
                print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
    if benchmark in ['hybrid']:
        import timeit
        import memray

        memray_file = output_dir / 'memray.bin'
        log.info('Starting memory tracking')
        seconds = None
        with memray.Tracker(
            file_name=memray_file,
            native_traces=True,
            follow_fork=True,
            memory_interval_ms=1,
        ):
            try:
                seconds = timeit.timeit(lambda: do_task_memory(runtime=runtime, memory=memory), number=1, globals=globals())
            except BaseException as e:
                print(e)  # Output: Command 'exit 1' returned non-zero exit status 1.
        log.info(f"Process ID {os.getpid()} executed task runtime={runtime},memory={memory} in {seconds} seconds")
        runtime_file = output_dir / 'runtime.txt'
        runtime_file.write_text(f'{runtime} {seconds}')

    if benchmark in ['off']:
        do_task(runtime)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--runtime', type=int)
    parser.add_argument('-m', '--memory', type=int)
    parser.add_argument('-b', '--benchmark', type=str, default='hybrid')
    parser.add_argument('-o', '--output_dir', type=Path)
    args = vars(parser.parse_args())
    log.info(args)
    main(**args)
