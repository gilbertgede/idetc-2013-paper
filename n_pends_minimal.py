from sympy import symbols                               # Import the symbols function
from sympy.physics.mechanics import *                   # Import mechanics classes

n = 4                                                   # Number of links in N-pendulum

q = dynamicsymbols('q:' + str(n))                       # Generalized coordinates
u = dynamicsymbols('u:' + str(n))                       # Generalized speeds
m = symbols('m:' + str(n))                              # Mass of each link
l = symbols('l:' + str(n))                              # Length of each link
g, t = symbols('g t')                                   # gravity and time symbols

A = ReferenceFrame('A')                                 # Inertial reference frame
frames = []                                             # List to hold n link frames
P = Point('P')                                          # Hinge point of top link
P.set_vel(A, 0)                                         # Set velocity of P in A to be 0

particles = []                                          # List to hold N particles
forces = []                                             # List to hold N applied forces
kin_odes = []                                           # List to hold kinematic ODE's

for i in range(n):
    Ai = A.orientnew('A' + str(i), 'Axis', [q[i], A.z]) # Create a new frame
    Ai.set_ang_vel(A, u[i] * A.z)                       # Set angular velocity
    frames.append(Ai)                                   # Add it to Frames list

    Pi = P.locatenew('P' + str(i), l[i] * Ai.x)         # Create a new point Pi
    Pi.v2pt_theory(P, A, Ai)                            # Set velocity of Pi
    Pai = Particle('Pa' + str(i), Pi, m[i])             # Create a new particle
    particles.append(Pai)                               # Add Pai to Particles list

    forces.append((Pi, m[i] * g * A.x))                 # Set force applied at i-th Point
    P = Pi                                              # P is now the lowest Point

    kin_odes.append(q[i].diff(t) - u[i])                # Kinematic ODE:  dq_i/dt-u_i=0

kane = KanesMethod(A, q_ind=q, u_ind=u, kd_eqs=kin_odes)# Generate EoM's:
fr, frstar = kane.kanes_equations(forces, particles)    # fr + frstar = 0
