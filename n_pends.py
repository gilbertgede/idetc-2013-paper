from sympy import symbols, Dummy, lambdify
from sympy.physics.mechanics import *

# Number of links
n = 4

# Coordinates, Speeds, and Derivatives thereof
q = dynamicsymbols('q:' + str(n))
qd = dynamicsymbols('q:' + str(n), 1)
u = dynamicsymbols('u:' + str(n))
ud = dynamicsymbols('u:' + str(n), 1)
# Parameters and constants
m = symbols('m:' + str(n))
l = symbols('l:' + str(n))
g = symbols('g')

# The list of frames, starting with the Inertial frame
Frames = [ReferenceFrame('A')]
# Add N frames to the list, each oriented relative to the first frame
[Frames.append(Frames[0].orientnew('A' + str(i), 'Axis', [q[i], Frames[-1].z])) for i in range(n)]
# Set angular velocity for the N frames, relative to the first frame
[Frames[i + 1].set_ang_vel(Frames[0], u[i] * Frames[i + 1].z) for i in range(n)]

# The list of Points, starting with pivot of first link, which has 0 velocity
# in the Inertial Frame
Points = [Point('O')]
Points[0].set_vel(Frames[0], 0)
# Add another Point to the list, located from the previous point, by the ith
# length in each link's x direction
[Points.append(Points[-1].locatenew('P' + str(i), l[i] * Frames[i + 1].x)) for i in range(n)]
# Use the 2 point theory on all the Points, in the Newtonian frame and on the
# current link, from the previous Point
[Points[i + 1].v2pt_theory(Points[i], Frames[0], Frames[i + 1]) for i in range(n)]

# The list of Particles, constructed out of Points and masses
Particles = [Particle('Pa' + str(i), Points[i + 1], m[i]) for i in range(n)]
# The list of forces - just gravity at each point
FL = [(Points[i + 1], m[i] * g * Frames[0].x) for i in range(n)]
# Kinematic Differential Equations in simple form: qd - u = 0
kd = [qd[i] - u[i] for i in range(n)]

# Generate the equations
KM = KanesMethod(Frames[0], q_ind=q, u_ind=u, kd_eqs=kd)
(fr, frstar) = KM.kanes_equations(FL, Particles)

# Substitute Values
link_m = 0.01 / n
link_l = 1. / n
grav = 9.81
parameter_dict = {g:grav}
for i in range(n):
    parameter_dict.update({l[i]:link_l, m[i]:link_m})
# Used to leave sympy and go to numpy
dummy_symbols = [Dummy() for i in q + u]
temp_dict = dict(zip(q + u, dummy_symbols))
# Actual substition
MM = KM.mass_matrix_full.subs(KM.kindiffdict()).subs(temp_dict).subs(parameter_dict)
Fo = KM.forcing_full.subs(KM.kindiffdict()).subs(temp_dict).subs(parameter_dict)

# Numerical Integration
from pylab import *
from scipy.integrate import odeint

# Construct the right-hand-side function
m = lambdify(dummy_symbols, MM)
f = lambdify(dummy_symbols, Fo)
def rhs(y, t):
    return array(linalg.solve(m(*y), f(*y))).T[0]

# Initial conditions and time vector
y0 = hstack((arange(n) * 0.01, arange(n) * 0))
t = linspace(0, 10, 1000)

# Integration
y = odeint(rhs, y0, t)

# Plotting
for i in range(n):
    figure(1)
    plot(t, y[:, i], label='q'+str(i))
    figure(2)
    plot(t, y[:, i + n], label='u'+str(i))

figure(1)
legend(loc=0)
xlabel('Time (s)')
ylabel('Rotation (rad)')
figure(2)
legend(loc=0)
xlabel('Time (s)')
ylabel('Angular Rate (rad/s)')
show()
