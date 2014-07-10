import abc

class Algorithm:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        "starts the algorithm"
    @abc.abstractmethod
    def sleep(self):
        "should return an integer (seconds to sleep)"
