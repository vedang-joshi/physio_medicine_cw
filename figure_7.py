from PyDSTool import *
import matplotlib.pyplot as plt
from PyDSTool.Toolbox import phaseplane as pp

pars = {'v_0': 1,
         'k': 10,
         'k_f': 1,
         'v_1': 7.3,
         'V_M2': 65,
         'V_M3': 500,
         'K_2': 1,
         'K_R': 2,
         'K_A': 0.9,
         'm': 2,
         'n': 2,
         'p': 4,
         'beta': 0.301
         }

initialConditionsDict = {'Z': 0, 'Y': 0}

# Set up model
auxiliaryFunctionDict = {'v_2': (['Z'], 'V_M2*((Z^n)/(K_2^n + Z^n))'),
                         'v_3': (['Z','Y'], 'V_M3*((Y^m)/(K_R^m + Y^m))*((Z^p)/(K_A^p + Z^p))')
                         }

Zstr = 'v_0 + v_1*beta - v_2(Z) + v_3(Z,Y) + k_f*Y - k*Z'
Ystr = 'v_2(Z) - v_3(Z,Y) - k_f*Y'

DSargs = args(name='Dupont1990')
DSargs.pars = pars
DSargs.varspecs = {'Z': Zstr, 'Y': Ystr}
DSargs.fnspecs = auxiliaryFunctionDict
DSargs.tdomain = [0,10]                         # set the range of integration.
DSargs.xdomain = {'Z': [-0.5, 1.5], 'Y': [0, 2.2]}
DSargs.ics = initialConditionsDict

testDS = Generator.Vode_ODEsystem(DSargs)
traj = testDS.compute('test')
pts = traj.sample(dt=0.01)

############ Phase plane analysis ###################################

# plot vector field, using a scale exponent to ensure arrows are well spaced
# and sized
pp.plot_PP_vf(testDS, 'Z', 'Y', scale_exp=-0.2)

# only one fixed point, hence [0] at end.
# n=4 uses three starting points in the domain to find any fixed points, to an
# accuracy of eps=1e-8.
fp_coord = pp.find_fixedpoints(testDS, n=5, eps=1e-8)[0]
print(fp_coord)

# n=3 uses three starting points in the domain to find nullcline parts, to an
# accuracy of eps=1e-8, and a maximum step for the solver of 0.1 units.
nullclines_Z, nullclines_Y = pp.find_nullclines(testDS, 'Z', 'Y', n=3, eps=1e-8, max_step=0.1)

# plot the fixed point
plt.plot(fp_coord['Z'], fp_coord['Y'], color='black', marker='^', markersize=7, label='Fixed point', mew=3)

# plot the nullclines
plt.plot(nullclines_Z[:,0], nullclines_Z[:,1], 'b', label='Z nullcline')
plt.plot(nullclines_Y[:,0], nullclines_Y[:,1], 'g', label='Y nullcline')

# plot the trajectory
plt.plot(pts['Z'], pts['Y'], linestyle='-', color='r', linewidth=1, label='Limit cycle')

#plt.plot(x_zoom, y_zoom, c='green', lw=1, label="Zoomed curve")

# plot the event points
#plt.plot(evs['x'], evs['y'], 'rs')

plt.axis('tight')
plt.title('Phase plane diagram')
plt.legend(loc='upper right')
plt.xlabel('Z ($\mu M$)')
plt.ylabel('Y ($\mu M$)')

plt.show()
