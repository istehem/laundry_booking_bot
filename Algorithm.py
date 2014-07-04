import abc

class Algorithm:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        "starts the algorithm"
        return
    @abc.abstractmethod
    def sleep(self):
        "should return an integer (seconds to sleep)"
