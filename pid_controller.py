import time

class PID_Controller:

    p_faktor = 30
    i_faktor = 15 
    d_faktor = 15

    def __init__(self, error, measurement):
        self.last_error = error
        self.last_measurement = measurement

        self.integrator = 0
        self.differentiator = 0

        self.last_output_time = time.time()
        self.delta_time = self.last_output_time - time.time()

    def give_rpm(self, error, measurement):
        self.delta_time = time.time() - self.last_output_time

        rpm = self._proportional(error) + self._integral(error) + self._derivative(measurement)

        self.last_output_time = time.time()

        self.last_error = error
        self.last_measurement = measurement

        print(f'prop: {self._proportional(error)}, int: {self.integrator}, dev: {self.differentiator}')

        return rpm

    def _proportional(self, error):
        return self.p_faktor * error

    def _integral(self, error):
        self.integrator = (self.i_faktor * self.delta_time / 2) * (error + self.last_error) + self.integrator
        return self.integrator

    def _derivative(self, measurement):
        self.differentiator = -self.d_faktor * (measurement - self.last_measurement) / self.delta_time
        return self.differentiator