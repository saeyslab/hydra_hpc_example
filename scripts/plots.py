import matplotlib.pyplot as plt
from pathlib import Path
import subprocess
import re
import yaml

def parse_runtime(f):
    x, y = f.read_text().split(' ')
    return int(x), float(y)

def parse_memory(f):
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

def plot_runtime(multirun):
    files = multirun.glob('**/runtime.txt')
    runtimes = [parse_runtime(f) for f in files]
    print(runtimes)
    xs, ys = zip(*runtimes)
    return plt.plot(xs, ys, marker='o')


def get_task(f):
    config_path = (f.parent / '.hydra' / 'config.yaml')
    with open(config_path) as fh:
        config = yaml.safe_load(fh)
    return int(config['task'])

def plot_memory(multirun):
    files = multirun.glob('**/memray.bin')
    memories = [(get_task(f), parse_memory(f)) for f in files]
    print(memories)
    xs, ys = zip(*memories)
    return plt.plot(xs, ys, marker='o')

def get_sorted_files(p):
    return sorted(p.glob('*'))

def main(multirun, output):
    if multirun is None:
        multirun = get_sorted_files(get_sorted_files(Path('multirun'))[-1])[-1]
    if output is None:
        output = multirun
    print(output)

    _ = plot_runtime(multirun)
    plt.title('Runtime (s)')
    plt.savefig(output / 'runtime.png')
    plt.close()

    _ = plot_memory(multirun)
    plt.title('Memory (MB)')
    plt.savefig(output / 'memory.png')
    plt.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--multirun", type=Path, help="Multirun output folder. Is most recent if not specified.")
    parser.add_argument("--output", type=Path, help="Output location of the plots.")
    args = parser.parse_args()
    main(**vars(args))