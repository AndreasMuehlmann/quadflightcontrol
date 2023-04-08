from collections import deque


class IirFilter:
    def __init__(self, faktor, order):
        self.faktor = faktor  # between 0 and 1
        self.order = order

        self.outputs = deque(maxlen=self.order)
        self.outputs.append(0)

        self.inputs = deque(maxlen=self.order)

    def give_filtered(self, value):
        self.inputs.append(value)
        output = (1 - self.faktor) * sum(self.inputs) / len(self.inputs) + \
            self.faktor * sum(self.outputs) / len(self.outputs)
        self.outputs.append(output)
        return output

    def reset(self):
        self.outputs = deque(maxlen=self.order)
        self.outputs.append(0)

        self.inputs = deque(maxlen=self.order)
