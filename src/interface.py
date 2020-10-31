from abc import ABCMeta, abstractmethod

class IClaseAdstrac(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def who_are_you(self): pass

class IUsuario(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def soyo(self): pass

