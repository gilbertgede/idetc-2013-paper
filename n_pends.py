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

parameters = [g]                                             # Parameter Definitions
parameter_vals = [9.81]                                      # First we define gravity
for i in range(N):
    parameters += [l[i], m[i]]                               # Then each mass
    parameter_vals += [1. / N, 0.01 / N]                     # and length

dummy_symbols = [Dummy() for i in q + u]                     # Necessary to translate
dummy_dict = dict(zip(q + u, dummy_symbols))                 # out of functions of time
kds = KM.kindiffdict()                                       # Need to eliminate qdots
MM = KM.mass_matrix_full.subs(kds).subs(dummy_dict)          # Substituting away qdots
Fo = KM.forcing_full.subs(kds).subs(dummy_dict)              # and in dummy symbols
mm = lambdify(dummy_symbols + parameters, MM)                # The actual call that gets
fo = lambdify(dummy_symbols + parameters, Fo)                # us to a NumPy function

def rhs(y, t, args):                                         # Creating the rhs function
    into = hstack((y, args))                                 # States and parameters
    return array(linalg.solve(mm(*into), fo(*into))).T[0]    # Solving for the udots

y0 = hstack((arange(N) * 0.01, arange(N) * 0))               # Initial conditions, q and u
t = linspace(0, 10, 1000)                                    # Time vector

y = odeint(rhs, y0, t, args=(parameter_vals,))               # Actual integration


f, ax = subplots(2, sharex=True, sharey=False)
f.set_size_inches(6.5, 6.5)

# PLOTTING
for i in range(N):
    ax[0].plot(t, y[:, i], label='q'+str(i))
    ax[1].plot(t, y[:, i + N], label='u'+str(i))

#figure(1)
ax[0].legend(loc=0)
ax[1].legend(loc=0)
ax[1].set_xlabel('Time [s]')
ax[0].set_ylabel('Angle [rad]')
ax[1].set_ylabel('Angular rate [rad/s]')
f.subplots_adjust(hspace=0)
setp(ax[0].get_xticklabels(), visible=False)
tight_layout()
savefig('four_link_pendulum_time_series.eps')
# figure(2)
# legend(loc=0)
# xlabel('Time (s)')
# ylabel('Angular Rate (rad/s)')
#show()
