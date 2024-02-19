from dataclasses import dataclass

from hydra_zen import ZenStore, just, make_config, make_custom_builds_fn
from hydra.conf import HydraConf, JobConf

from frequencies_hydra.methods import (
    counter,
    default_dict,
    for_counter,
    get_or_default,
    if_contains_else,
    numpy_freq,
    try_except,
)

from frequencies_hydra.data import smalllist, biglist, arr_smalllist, arr_biglist


@dataclass
class BenchmarkConfig:
    name: str

store = ZenStore(overwrite_ok=True)

method_store = store(group="method")
method_store(just(if_contains_else), name="if_contains_else")
method_store(just(for_counter), name="for_counter")
method_store(just(counter), name="counter")
method_store(just(get_or_default), name="get_or_default")
method_store(just(default_dict), name="default_dict")
method_store(just(numpy_freq), name="numpy_freq")
method_store(just(try_except), name="try_except")

data_store = store(group="data")
data_store(just(smalllist), name="small")
data_store(just(biglist), name="big")
data_store(just(arr_smalllist), name="arr_small")
data_store(just(arr_biglist), name="arr_big")

# Automatically generate and store configs for `benchmark`
benchmark_store = store(group="benchmark")
benchmark_store(BenchmarkConfig("runtime"), name="runtime")
benchmark_store(BenchmarkConfig("memory"), name="memory")
benchmark_store(BenchmarkConfig("all"), name="all")
benchmark_store(BenchmarkConfig("hybrid"), name="hybrid")
benchmark_store(BenchmarkConfig("off"), name="off")

# Configure the top-level function that will be executed from
# the CLI; provide the default model & dataloader configs to
# use.

pbuilds = make_custom_builds_fn(zen_partial=True, populate_full_signature=True)


# The 'top-level' config for our app w/ a specified default
# database and server
ExperimentConfig = make_config(
    method=just(for_counter),
    data=just(smalllist),
    benchmark=BenchmarkConfig(name="all"),
)

# the experiment configs:
# - must be stored under the _global_ package
# - must inherit from `Config`
# experiment_store = store(group="experiment",  package="_global_")

# equivalent to `python my_app.py db=sqlite server.port=8080`
# experiment_store(
#     make_config(
#         hydra_defaults=["_self_", {"override /method": "counter"}],
#         bases=(Config,),
#     ),
#     name="for_counter",
# )


# equivalent to: `python my_app.py db=sqlite server=nginx server.port=8080`
# experiment_store(
#     make_config(
#         hydra_defaults=[
#             "_self_",
#             {"override /method": "if_contains_else"},
#         ],
#         bases=(Config,)
#     ),
#     name="if_contains_else",
# )

# Configure Hydra to change the working dir to match that of the output dir

store(HydraConf(job=JobConf(chdir=True)), name="config", group="hydra")
store(ExperimentConfig, name="config")

# Add all of the configs, that we put in hydra-zen's (local) config store,
# to Hydra's (global) config store.
store.add_to_hydra_store(overwrite_ok=True)
