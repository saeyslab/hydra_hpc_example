from dask.distributed import Client
from dask_jobqueue.slurm import SLURMRunner
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

def main():
    # When entering the SLURMRunner context manager processes will decide if they should be
    # the client, schdeduler or a worker.
    # Only process ID 1 executes the contents of the context manager.
    # All other processes start the Dask components and then block here forever.
    logging.debug("Creating Slurm")
    with SLURMRunner(scheduler_file="scheduler-{job_id}.json") as runner:
        logging.debug("SLURMRunner created")
        # The runner object contains the scheduler address info and can be used to construct a client.
        with Client(runner) as client:
            logging.debug("Client created")
            # Wait for all the workers to be ready before continuing.
            client.wait_for_workers(runner.n_workers)
            logging.debug("Workers ready")
            # Then we can submit some work to the Dask scheduler.
            assert client.submit(lambda x: x + 1, 10).result() == 11
            assert client.submit(lambda x: x + 1, 20, workers=2).result() == 21
            logging.debug("Work done")
# When process ID 1 exits the SLURMRunner context manager it sends a graceful shutdown to the Dask processes

if __name__ == "__main__":
    main()