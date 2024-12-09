import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logging.debug("Running " + __file__)

from dask_mpi import initialize
initialize()

logging.debug("Initialized Dask MPI")

from dask.distributed import Client

def main():
    client = Client()
    logging.debug("Client created")
    assert client.submit(lambda x: x + 1, 10).result() == 11
    assert client.submit(lambda x: x + 1, 20, workers=2).result() == 21
    logging.debug("Work done")

if __name__ == "__main__":
    main()