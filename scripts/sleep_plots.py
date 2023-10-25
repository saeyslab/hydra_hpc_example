import matplotlib.pyplot as plt
from pathlib import Path
import subprocess
import re
from omegaconf import OmegaConf
from typing import Any
import logging
import os

# set log level based on env
logging.basicConfig(level=os.environ.get('LOGLEVEL', logging.INFO))

def parse_runtime(f: Path) -> tuple[int, float]:
    text = f.read_text()
    logging.info(text)
    _, y = text.split(' ')
    return float(y)

def parse_memory(f: Path) -> float | None:
    memory_file = f.parent / 'memory.txt'
    with open(memory_file, 'w') as fh:
        subprocess.run(['python3', '-m', 'memray', 'tree', str(f)], stdout=fh)
    tree = memory_file.read_text()
    regex = r"Peak memory size: ([A-Za-z.0-9]+)"     
    match = re.search(regex, tree)
    peak = match.group(1) if match else 0
    match [peak[:-2], peak[-2:]]:
        case [n, 'KB']:
            return float(n) / 1000
        case [n, 'MB']:
            return float(n)
        case [n, 'GB']:
            return float(n) * 1000
        case [n, _]:
            return float(n)

def plot_runtime(files: list[Path]) -> list[Any]:
    runtimes = [(get_task(f)['runtime'], parse_runtime(f)) for f in files]
    logging.info(runtimes)
    xs, ys = zip(*runtimes)
    return plt.plot(xs, ys, marker='o')


def get_task(f) -> int:
    config_path = (f.parent / '.hydra' / 'config.yaml')
    config = OmegaConf.load(config_path)
    return config['task']

def plot_memory(files) -> plt.Figure: 
    memories = [(get_task(f)['memory'], parse_memory(f)) for f in files]
    logging.info(memories)
    xs, ys = zip(*memories)
    return plt.plot(xs, ys, marker='o')

def get_sorted_files(p) -> list[Path]:
    return sorted(p.glob('*'))

def main(multirun, run_folder, output) -> None:
    if multirun is None and run_folder is None:
        multirun = Path('multirun')
    if run_folder is None:
        run_folder = get_sorted_files(get_sorted_files(multirun)[-1])[-1]
    logging.info(multirun)
    if output is None:
        output = run_folder
    logging.info(output)

    runtime_files = list(run_folder.glob('**/runtime.txt'))
    if runtime_files:
        _ = plot_runtime(runtime_files)
        plt.title('Runtime (s)')
        plt.xlabel('Expected')
        plt.ylabel('Measured')
        plt.savefig(output / 'sleep_runtime.png')
        plt.close()

    memory_files = list(run_folder.glob('**/memray.bin'))
    if memory_files:
        _ = plot_memory(memory_files)
        plt.title('Memory (MB)')
        plt.xlabel('Expected')
        plt.ylabel('Measured')
        plt.savefig(output / 'sleep_memory.png')
        plt.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', "--multirun", type=Path, default='multirun', help="Root locations of all multiruns of which to select the most recent run_folder.")
    parser.add_argument('-r', "--run_folder", type=Path, default=None, help="Specific multirun output folder, instead of most recent.")    
    parser.add_argument('-o', "--output", type=Path, help="Output location of the plots. Defaults to run_folder.")
    args = parser.parse_args()
    logging.info(args)
    main(**vars(args))