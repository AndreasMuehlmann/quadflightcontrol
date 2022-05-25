from abc import ABCMeta, abstractmethod


class InterfaceUser(metaclass=ABCMeta):
    @abstractmethod 
    def give_inputs(seĺf):
        pass

    @abstractmethod 
    def send_outputs(self, outputs):
        pass
