import logging
from pathlib import Path
import csv
import yaml

# import sleep task from main.py
from main import main as do_benchmark

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

def main(sweep, benchmark, output_dir) -> None:
    output_dir = output_dir.resolve()
    output_dir.mkdir(exist_ok=True)
    with sweep.open() as fh:
        params = csv.DictReader(fh)
        log.info(params)
        for i, row in enumerate(params):
            sub_output_dir = output_dir / str(i)
            # make sure to cast the strings from the csv to the right type
            runtime = int(row['runtime'])
            memory = int(row['memory'])
            config_yaml = sub_output_dir / '.hydra' / 'config.yaml'
            config_yaml.parent.mkdir(parents=True)
            config_data = ({
                "task": {
                    "memory": memory,
                    "runtime": runtime
                }
            })
            with config_yaml.open('w') as fp:
                yaml.safe_dump(config_data, fp, indent=4, default_flow_style=False)
            do_benchmark(runtime=runtime, memory=memory, benchmark=benchmark, output_dir=sub_output_dir)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sweep', type=Path)
    parser.add_argument('-b', '--benchmark', type=str, default='hybrid')
    parser.add_argument('-o', '--output_dir', type=Path)
    args = vars(parser.parse_args())
    log.info(args)
    main(**args)
