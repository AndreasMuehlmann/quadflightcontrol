from abc import ABCMeta, abstractmethod


class InterfaceControl(metaclass=ABCMeta):
    @abstractmethod 
    def give_measurements(self):
        pass

    @abstractmethod 
    def send_outputs(self, outputs):
        pass
