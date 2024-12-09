import submitit
import logging
import os

def add(a, b):
    return a + b

def run_add(executor):
    job = executor.submit(add, 5, 7)  # will compute add(5, 7)
    print(job.job_id)  # ID of your job

    output = job.result()  # waits for completion and returns output
    assert output == 12  # 5 + 7 = 12...  your addition was computed in the cluster


def run_main():
    # try:
    #     # see if running on a submitit cluster
    #     env = submitit.JobEnvironment()
    #     logging.info(f"Running with {env}")
    # except RuntimeError:
    #     logging.debug("Not running on a submitit cluster")
    from main import main
    main()

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def launch():

    # executor is the submission interface (logs are dumped in the folder)
    executor = submitit.AutoExecutor(folder="log_test")
    # set timeout in min, and partition for running the job
    executor.update_parameters(timeout_min=1, slurm_partition="doduo", cpus_per_task=2, nodes=1, tasks_per_node=1)
    run_add(executor)
    run_main()

if __name__ == "__main__":
    launch()