import numpy as np
import control
import matplotlib.pyplot as plt


# continuos plant system
T = 0.01

A = np.array([[0, 1], [0, 0]])
B = np.array([[0], [1/50]])
C = np.array([1, 0])
D = np.array([[0]])

plant_sys = control.ss(A, B, C, D)
plant_sys = control.ss2tf(plant_sys)


'''
# discrete plant system
T = 0.01

A = np.array([[1, T], [0, 1.0]])
B = np.array([[1/2*T**2/50], [T/50]])
C = np.array([1, 0])
D = np.array([[0]])

plant_sys = control.ss(A, B, C, D , dt=T)
plant_sys = control.ss2tf(plant_sys)
print(plant_sys)
'''


# Transferfunction Controller (PID): G(s) = (Kd*s^2 + Kp*s + Ki) / s
# Transferfunction Plant: G(s) = 0.02/s^2
# Transferfunction Closed Loop = G(s) = (0.02*(Kd*s^2 + Kp*s + Ki))/(s^3 + 0.02*(Kd*s^2 + Kp*s + Ki))

Kp = 150.0 # 150.0 # 37.5
Ki = 50.0 # 21.09 # 6.25
Kd = 150.0 # 140.5 # 75

controller = control.tf([Kd, Kp, Ki], [1, 0])
closed_loop_sys = control.feedback(controller * plant_sys, 1)
print(closed_loop_sys)
print(f'poles: {control.poles(closed_loop_sys)}')
# print(f'zeros: {control.zeros(closed_loop_sys)}')
print(f'margin: {control.margin(closed_loop_sys)}')

t = np.arange(0, 10, T)

u = np.linspace(0, 10, len(t)) + np.sin(t)

t, y = control.forced_response(closed_loop_sys, T=t, U=u)

plt.plot(t, y)
plt.plot(t, u, label='input')
plt.xlabel('time')
plt.ylabel('position')
plt.title('forced response')
plt.legend(loc='upper left')
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

# control.nichols_plot(closed_loop_sys)
# plt.show()

# control.root_locus(closed_loop_sys)
# plt.show()

'''
u = np.ones_like(t) * 0.5
u[t.size // 2:] = -2
# u = np.sin(t)
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
'''
