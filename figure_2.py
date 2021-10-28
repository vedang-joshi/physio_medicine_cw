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
DSargs.xdomain = {'Z': [-3, 3], 'Y': [-1, 2.5]}
DSargs.ics = initialConditionsDict

testDS = Generator.Vode_ODEsystem(DSargs)

########## Calcium concentrations in time plotting code ###########


traj = testDS.compute('pol')
pts = traj.sample(dt=0.01)

# trajectory
plt.plot(pts['t'], pts['Z'], label='Z trajectory')
plt.plot(pts['t'], pts['Y'], label='Y trajectory')
plt.xlabel('Time (s)')
plt.ylabel('Ca$^{2+}$ in the cytosol ($\mu M$)')
plt.legend(loc='upper right')
plt.title('Oscillations in cytosolic Ca$^{2 +}$')
plt.show()
