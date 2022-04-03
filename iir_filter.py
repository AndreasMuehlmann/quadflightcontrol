from collections import deque

class IIR_Filter:

    def __init__(self, faktor, order):
        self.outputs = deque(maxlen=order)
        self.outputs.append(0)

        self.inputs = deque(maxlen=order)

        self.faktor = faktor #between 0 and 1

    def give_filtered(self, input):
        self.inputs.append(input)
        output = (1 - self.faktor) * sum(self.inputs) / len(self.inputs) + self.faktor * sum(self.outputs) / len(self.outputs)
        self.outputs.append(output)

        return output