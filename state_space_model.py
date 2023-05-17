import numpy as np
import control
import matplotlib.pyplot as plt


'''
continuos plant system
T = 0.01

A = np.array([[0, 1], [0, 0]])
B = np.array([[0], [1/50]])
C = np.array([1, 0])
D = np.array([[0]])

plant_sys = control.ss(A, B, C, D)
plant_sys = control.ss2tf(plant_sys)
print(plant_sys)
'''


'''
discrete plant system
T = 0.01

A = np.array([[1, T], [0, 1.0]])
B = np.array([[1/2*T**2/50], [T/50]])
C = np.array([1, 0])
D = np.array([[0]])

plant_sys = control.ss(A, B, C, D , dt=T)
plant_sys = control.ss2tf(plant_sys)
print(plant_sys)
'''


'''
Kp = 1000.0
Ki = 0.0
Kd = 0.0

s = control.TransferFunction([1, 0], [1])
z = control.TransferFunction([1], [1], dt=T)

# Create PID controller transfer function in the Laplace domain
pid_tf = (Kd * s**2 + Kp * s + Ki) / s

# Get the numerator and denominator arrays
num = np.array(pid_tf.num[0][0])
den = np.array(pid_tf.den[0][0])
den = np.concatenate((np.zeros(1), den))

# Create the discrete-time transfer function
controller = control.TransferFunction(num, den, dt=T)

# Print the discrete-time transfer function of the PID controller
print(controller)

closed_loop_sys = control.feedback(controller * plant_sys, 1)
'''


# Transferfunction Controller (PID): G(s) = (Kd*s^2 + Kp*s + Ki) / s
# Transferfunction Plant: G(s) = 0.02/s^2
# Transferfunction Closed Loop = G(s) = (0.02*(Kd*s^2 + Kp*s + Ki))/(s^3 + 0.02*(Kd*s^2 + Kp*s + Ki))

Kp = 150.0
Ki = 50.0
Kd = 150.0

numerator = [0.02 * Kd, 0.02 * Kp, 0.02*Ki]
denomanator = [1, 0.02 * Kd, 0.02 * Kp, 0.02*Ki]
closed_loop_sys = control.TransferFunction(numerator, denomanator)


T = 0.01
t = np.arange(0, 10, T)
u = np.ones_like(t) * 1
u[t.size // 2:] = 1
t, y = control.forced_response(closed_loop_sys, T=t, U=u)

plt.plot(t, y)
plt.plot(t, u, label='input')
plt.xlabel('time')
plt.ylabel('position')
plt.title('forced response')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()

t, y = control.impulse_response(closed_loop_sys, T=t)

plt.plot(t, y)
plt.xlabel('time')
plt.ylabel('position')
plt.title('impulse response')
plt.grid(True)
plt.show()


t, y = control.step_response(closed_loop_sys, T=t)

plt.plot(t, y)
plt.xlabel('time')
plt.ylabel('position')
plt.title('step response')
plt.grid(True)
plt.show()

control.bode_plot(closed_loop_sys)
plt.show()

control.nichols_plot(closed_loop_sys)
plt.show()
