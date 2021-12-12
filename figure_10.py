from PyDSTool import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from adjustText import adjust_text

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
DSargs.xdomain = {'Z': [-3, 3], 'Y': [-1, 3]}
DSargs.ics = initialConditionsDict

testDS = Generator.Vode_ODEsystem(DSargs)

# Prepare the system to start close to a steady state
testDS.set(pars = {'beta': 1} )       # Lower bound of the control parameter 'beta'
testDS.set(ics =  {'Z': 0.5, 'Y': 2} )       # Close to one of the steady states present for beta=1

# Set up continuation class
PC = ContClass(testDS)

PCargs = args(name='EQ1', type='EP-C')
PCargs.freepars = ['beta']
PCargs.StepSize = 1e-3
#PCargs.MaxNumPoints = 4500
PCargs.MaxStepSize = 0.1
PCargs.LocBifPoints = 'all'
PCargs.SaveEigen = True
PCargs.SaveJacobian = True
PCargs.verbosity = 2
PC.newCurve(PCargs)

print('Computing curve...')
PC['EQ1'].forward()
PC['EQ1'].backward()
PC['EQ1'].display(['Z','Y'], stability=True, figure=3)
black_line_stable = mlines.Line2D([], [], color='black', linewidth=1.5, linestyle='-', label='Stable \n equilibrium \n curve')
black_line_unstable = mlines.Line2D([], [], color='black', linewidth=1.5, linestyle='--', label='Unstable \n equilibrium \n curve')
blue_circle = mlines.Line2D([0], [0], marker='o', color='w', label='Hopf \n bifurcation',
                        markerfacecolor='blue', markersize=8)
plt.legend(handles=[black_line_stable, black_line_unstable, blue_circle], loc='upper right')
PC['EQ1'].info()
#plt.title("Numerical continuation bifurcation diagram of subsystem Y varying $\\beta$ \n H1-H4 family of limit cycles \n Zoomed into system dynamics at H1")
plt.title("Bifurcation diagram of the system")
plt.xlim(-2, 2)
plt.show()
