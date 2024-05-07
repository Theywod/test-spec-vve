import logging
from abc import ABC, abstractmethod

class AlgorithmAbc(ABC):    
    def __init__(self, debug):
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(format="%(asctime)s | %(name)s | %(levelname)s : %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z",
            level=logging.DEBUG)
            logging.debug("Debugging messages activated")
        else:
            logging.basicConfig(format="%(asctime)s | %(levelname)s : %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z",
            level=logging.INFO)

    @abstractmethod
    def process_data(self, data):
        raise NotImplementedError('subclasses must override process_data()!')

    @abstractmethod
    def set_params(self, params):
        raise NotImplementedError('subclasses must override set_params()!')