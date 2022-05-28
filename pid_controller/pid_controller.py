from iir_filter import IirFilter

class PidController:
    def __init__(self, p_faktor, i_faktor, d_faktor, iir_faktor, iir_order, maximum):
        self.p_faktor = p_faktor
        self.i_faktor = i_faktor
        self.d_faktor = d_faktor
        self.maximum = maximum

        self.last_error = 0
        self.last_measurement = 0

        self.integrator = 0
        self.differentiator = 0

        self.delta_time = 0.01

        self.iir_error = IirFilter(iir_faktor, iir_order)
        self.iir_measurement = IirFilter(iir_faktor, iir_order)

    def give_output(self, error, measurement):
        error = self.iir_error.give_filtered(error)
        measurement = self.iir_measurement.give_filtered(measurement)

        self._integral(error)
        if self.integrator > self.maximum:
            self.integrator = self.maximum

        elif self.integrator < -self.maximum:
            self.integrator = -self.maximum

        output = self._proportional(error) + self.integrator + self._derivative(measurement)

        self.last_error = error
        self.last_measurement = measurement

        return output

    def _proportional(self, error):
        return self.p_faktor * error

    def _integral(self, error):
        self.integrator = (self.i_faktor * self.delta_time / 2) * (error + self.last_error) + self.integrator
        return self.integrator

    def _derivative(self, measurement):
        self.differentiator = -self.d_faktor * (measurement - self.last_measurement) / self.delta_time
        return self.differentiator
