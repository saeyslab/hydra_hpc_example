import subprocess
import logging
import os
import sys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def shell_cmd(command):
    """Executes the given command within terminal and returns the output as a string

    :param command: the command that will be executed in the shell
    :type command: str

    :return: the output of the command
    :rtype: str
    """
    process = subprocess.run([command], stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    return process

def main():
    logging.info("Running main")
    logging.info("Python version: %s", sys.version)
    logging.info("Python path: %s", sys.executable)
    
    output = cmd = shell_cmd('module list')
    logging.info("Module list: %s", output)
    if logging.root.level <= logging.DEBUG:
        output = shell_cmd('pip list')
        logging.info("Pip list: %s", output)
    logging.info("Done")

if __name__ == "__main__":
    main()