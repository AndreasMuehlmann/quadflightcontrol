import config as conf
from iir_filter import IirFilter
from controller import Controller


class PidController(Controller):
    def __init__(self, p_faktor, i_faktor, d_faktor, iir_faktor, iir_order, max_output):
        self.p_faktor = p_faktor
        self.i_faktor = i_faktor
        self.d_faktor = d_faktor

        self.max_output = max_output
        self.max_integrator = self.max_output / 5

        self.last_error = 0
        self.last_measurement = 0

        self.integrator = 0
        self.differentiator = 0

        self.delta_time = 1 / conf.frequency

        self.iir_error = IirFilter(iir_faktor, iir_order)
        self.iir_measurement = IirFilter(iir_faktor, iir_order)

    def give_output(self, error, measurement):
        error = self.iir_error.give_filtered(error)
        measurement = self.iir_measurement.give_filtered(measurement)

        self._integral(error)
        if self.integrator > self.max_integrator:
            self.integrator = self.max_integrator

        elif self.integrator < -self.max_integrator:
            self.integrator = -self.max_integrator

        output = self._proportional(error) + self.integrator + self._derivative(measurement)

        if output > self.max_output:
            output = self.max_output

        elif output < -self.max_output:
            output = -self.max_output

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

    def reset(self):
        self.last_error = 0
        self.last_measurement = 0

        self.integrator = 0
        self.differentiator = 0

        self.iir_error.reset()
        self.iir_measurement.reset()
