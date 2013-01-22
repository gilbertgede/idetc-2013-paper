from sympy import symbols             # Import the symbols function
from sympy.physics.mechanics import * # Import mechanics classes and functions

N = 4                                 # Number of links in N-pendulum

q = dynamicsymbols('q:' + str(N))     # Generalized coordinates
u = dynamicsymbols('u:' + str(N))     # Generalized speeds

m = symbols('m:' + str(N))            # Mass of each link
l = symbols('l:' + str(N))            # Length of each link
g, t = symbols('g t')                 # gravity and time symbols

A = ReferenceFrame('A')               # Inertial reference frame
Frames = []                           # List to hold n link frames
P = Point('P')                        # Hinge point of top link
P.set_vel(A, 0)                       # Set velocity of P in A to be zero
Particles = []                        # List to hold N particles
FL = []                               # List to hold N applied forces
kd = []                               # List to hold kinematic ODE's

for i in range(N):
    Ai = A.orientnew('A' + str(i), 'Axis', [q[i], A.z]) # Create a new frame
    Ai.set_ang_vel(A, u[i] * A.z)                       # Set angular velocity
    Frames.append(Ai)                                   # Add it to Frames list

    Pi = P.locatenew('P' + str(i), l[i] * Ai.x)  # Create a new point,
    Pi.v2pt_theory(P, A, Ai)                     # Set velocity
    Pai = Particle('Pa' + str(i), Pi, m[i])      # Create a new particle
    Particles.append(Pai)                        # Add Pai to Particles list

    FL.append((Pi, m[i] * g * A.x)) # Set the force applied at i-th Point
    P = Pi                          # P now represents the lowest Point

    kd.append(q[i].diff(t) - u[i])  # Kinematic ODE:  dq_i / dt - u_i = 0

KM = KanesMethod(A, q_ind=q, u_ind=u, kd_eqs=kd) # Generate EoM's:
fr, frstar = KM.kanes_equations(FL, Particles)   # fr + frstar = 0

# NUMERICAL SIMULATION
from pylab import *
from sympy import Dummy, lambdify
from scipy.integrate import odeint

# Substitution Values
link_m = 0.01 / N
link_l = 1. / N
grav = 9.81
parameter_dict = {g:grav}
for i in range(N):
    parameter_dict.update({l[i]:link_l, m[i]:link_m})
# Used to leave sympy and go to numpy
dummy_symbols = [Dummy() for i in q + u]
temp_dict = dict(zip(q + u, dummy_symbols))
# Actual substition
MM = KM.mass_matrix_full.subs(KM.kindiffdict()).subs(temp_dict).subs(parameter_dict)
Fo = KM.forcing_full.subs(KM.kindiffdict()).subs(temp_dict).subs(parameter_dict)

# Construct the right-hand-side function
m = lambdify(dummy_symbols, MM)
f = lambdify(dummy_symbols, Fo)
def rhs(y, t):
    return array(linalg.solve(m(*y), f(*y))).T[0]

# Initial conditions and time vector
y0 = hstack((arange(N) * 0.01, arange(N) * 0))
t = linspace(0, 10, 1000)

# Integration
y = odeint(rhs, y0, t)

# PLOTTING
for i in range(N):
    figure(1)
    plot(t, y[:, i], label='q'+str(i))
    figure(2)
    plot(t, y[:, i + N], label='u'+str(i))

figure(1)
legend(loc=0)
xlabel('Time (s)')
ylabel('Rotation (rad)')
figure(2)
legend(loc=0)
xlabel('Time (s)')
ylabel('Angular Rate (rad/s)')
show()
