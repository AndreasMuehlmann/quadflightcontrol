import config as conf


class PidController():
    def __init__(self, p_faktor, i_faktor, d_faktor, max_output, max_integrator):
        self.p_faktor = p_faktor
        self.i_faktor = i_faktor
        self.d_faktor = d_faktor

        self.max_output = max_output
        self.max_integrator = max_integrator

        self.last_error = 0
        self.last_measurement = 0

        self.integrator = 0
        self.differentiator = 0

        self.delta_time = 1 / conf.frequency

    def give_output(self, error, measurement):
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
