from hydra_zen import launch
import seaborn as sns

from frequencies_hydra.config import ExperimentConfig
from frequencies_hydra.main import task_function
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


(jobs,) = launch(
    ExperimentConfig,
    task_function,
    overrides=[
        "+method=counter, for_counter, get_or_default, default_dict, try_except, if_contains_else, numpy_freq",
        "+data=small,big",
        "+benchmark=runtime",
    ],
    multirun=True,
)
# alternative, parse jobs from most recent multirun folder
# get most recent multirun folder
# multirun_folder = sorted(Path("outputs").glob("multirun*"))[-1]
# parse object similar to hydra.core.utils.JobReturn from multirun folder yamls in .hydra folder
# contains cfg, working_dir, overrides and hydra_config

runtime_data = []

for j in jobs:
    method = None
    data = None
    # j.cfg
    # get method and data name from overrides config
    for override in j.overrides:
        if "method" in override:
            method = override.split("=")[1]
        if "data" in override:
            data = override.split("=")[1]
    if "method" not in locals() and "data" not in locals():
        raise ValueError("method and data not found in overrides")
    # open runtime.txt and parse runtime
    with open(Path(j.working_dir) / "runtime.txt") as f:
        runtime = f.read().split(" ")[-1]
        runtime_data.append({"Method": method, "Data": data, "Runtime": float(runtime)})

df = pd.DataFrame(runtime_data)
sns.lineplot(data=df, x="Data", y="Runtime", hue="Method")
plt.xlabel("Data Size")
plt.ylabel("Runtime (seconds)")
plt.title("Runtime by Method")
plt.savefig("resources/runtime_by_method.png")
