from abc import ABCMeta, abstractmethod


class InterfaceControl(metaclass=ABCMeta):
    @abstractmethod 
    def give_measurements():
        pass

    @abstractmethod 
    def send_outputs(outputs):
        pass
