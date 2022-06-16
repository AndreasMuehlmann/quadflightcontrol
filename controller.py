from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, p_faktor, i_faktor, d_faktor, iir_faktor, iir_order, maximum):
        pass

    @abstractmethod
    def give_output(self, error, measurement):
        pass

    @abstractmethod
    def reset(self):
        pass
