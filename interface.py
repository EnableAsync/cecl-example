from abc import ABCMeta, abstractmethod


class Cecl(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, param):
        pass
