import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self, a, b, dt):
        self.a = a
        self.b = b
        self.dt = dt

    def give_t(self, length):
        return np.arange(0, length * self.dt, self.dt)

    def fit(self, p, u):
        data_matrix = self.basis_functions(p[0], model._differentiate(p[0], p[1]), u)
        coefficients, residuals, _, _ = np.linalg.lstsq(data_matrix, p, rcond=None)
        return coefficients

    def _differentiate(self, y_previous, y):
        return (y - y_previous) / self.dt

    def basis_functions(self, start_pos, start_vel, u):
        p_hat = self.predict(start_pos, start_vel, u)
        self.data_matrix = np.column_stack((p_hat, np.ones(len(u)) * np.mean(u)))
        return self.data_matrix

    def predict(self, start_pos, start_vel, u):
        p_hat = []
        p = start_pos + self.b
        v = start_vel
        for step in range(len(u)):
            p_hat.append(p)
            p += v * self.dt + self.a * 1/2 * u[step] * self.dt**2
            v += self.a * u[step] * self.dt
        return p_hat


start = 100
end = 300
measurements = pd.read_csv('experiments/roll_oscillation.csv')
p = measurements['froll'].iloc[start:end].to_numpy()
outputs = pd.read_csv('experiments/roll_oscillation_outputs.csv')
u = outputs['roll_c_o'].iloc[start:end].to_numpy()

model = Model(100, 0, 0.01)
p_hat_hand = model.predict(p[0], model._differentiate(p[0], p[1]), u)

a_first = 100
model = Model(a_first, 0, 0.01)
coefficients = model.fit(p, u)
model.a = a_first * coefficients[0]
model.b = coefficients[1]
p_hat = np.dot(coefficients, model.data_matrix.T)# model.predict(p[0], model._differentiate(p[0], p[1]), u)

print(f'a: {round(coefficients[0], 4)}, b: {round(coefficients[1], 4)}')
t = model.give_t(len(p))
plt.tight_layout()
plt.style.use('fivethirtyeight')
plt.plot(t, p, label='real')
plt.plot(t, p_hat_hand, label='prediction')
plt.plot(t, p_hat, label='prediction_lstsq')
plt.plot(t, u, label='input')
plt.xlabel('time')
plt.ylabel('position')
plt.legend(loc='upper left')
plt.title('Roll Prediction')
plt.show()
