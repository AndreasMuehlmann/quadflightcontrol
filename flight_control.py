from abc import ABCMeta, abstractmethod

'''
(fl) rotor2 -> \ / <- rotor1 (fr)
                °
(bl) rotor3 -> / \ <- rotor4 (br)

[rotor1, rotor2, rotor2, rotor4]
'''

class FlightControl(metaclass=ABCMeta):
    @abstractmethod
    def give_outputs(self, measurements):
        pass
