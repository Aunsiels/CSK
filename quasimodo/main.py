from quasimodo.default_workflow import DefaultWorkflow
from quasimodo.parameters_reader import ParametersReader
import logging
import socket

name = str(socket.gethostname())

parameters_reader = ParametersReader()
PATTERN_FIRST = (parameters_reader.get_parameter("pattern-first") or "true") == "true"
if PATTERN_FIRST:
    name += "by_pattern"

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename='log_' + name + '.txt',
        filemode='w')

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(filename="log.txt", level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    # Create a workflow
    workflow = DefaultWorkflow()
    print("Choose the stage at which you should begin the processing")
    workflow.print_index()
    stage = int(input())
    workflow.run_from(save=True, idx_from=stage)
