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
PC['EQ1'].display(['beta','Z'], stability=True, figure=3)
#black_line_stable = mlines.Line2D([], [], color='black', linewidth=1.5, linestyle='-', label='Stable \n equilibrium \n curve')
#black_line_unstable = mlines.Line2D([], [], color='black', linewidth=1.5, linestyle='--', label='Unstable \n equilibrium \n curve')
#blue_circle = mlines.Line2D([0], [0], marker='o', color='w', label='Hopf \n bifurcation',
#                        markerfacecolor='blue', markersize=8)
#plt.legend(handles=[black_line_stable, black_line_unstable, blue_circle], loc='upper right')
PC['EQ1'].info()
plt.title("Numerical continuation bifurcation diagram of subsystem Z varying $\\beta$ \n H1-H4 family of limit cycles ")
#\n Zoomed into system dynamics at H1")
plt.xlim(-2, 2)


def track_limit_cycles_from_Hopf_bif_point(pycontclass, curve_name, init_point_name):
    '''
    Given a Hopf bifurcation point, track the branch of limit cycles.

    :param pycontclass: In our case, will always be 'PC'
    :param curve_name: Name of limit cycle curve for Hopf bifurcation point (must be unique)
    :param init_point_name: initial Hopf point to start tracking eg. 'EQ1:H1' from equilibrium curve for first
                            Hopf point

    '''
    PCargs.name = curve_name
    PCargs.type = 'LC-C'
    PCargs.initpoint = init_point_name
    PCargs.MinStepSize = 0.005
    PCargs.MaxStepSize = 1.0
    PCargs.StepSize = 0.01
    #PCargs.MaxNumPoints = 4000
    PCargs.LocBifPoints = 'LPC'
    PCargs.SaveEigen = True
    pycontclass.newCurve(PCargs)
    pycontclass[curve_name].forward()
    #pycontclass[curve_name].backward()


def track_hopf_point_curve_from_Hopf_bif_point(pycontclass, curve_name, init_point_name):
    '''
    Given a Hopf bifurcation point, track the hopf point curve .

    :param pycontclass: In our case, will always be 'PC'
    :param curve_name: Name of limit cycle curve for Hopf bifurcation point (must be unique)
    :param init_point_name: initial Hopf point to start tracking eg. 'EQ1:H1' from equilibrium curve for first
                            Hopf point

    '''
    PCargs.name = curve_name
    PCargs.type = 'H-C1'
    PCargs.initpoint = init_point_name
    PCargs.MinStepSize = 0.005
    PCargs.MaxStepSize = 1.0
    PCargs.StepSize = 0.01
    # PCargs.MaxNumPoints = 4000
    PCargs.LocBifPoints = 'all'
    PCargs.SaveEigen = True
    pycontclass.newCurve(PCargs)
    pycontclass[curve_name].forward()
    #pycontclass[curve_name].backward()

# Numerically continue limit cycles from all 4 Hopf points
track_limit_cycles_from_Hopf_bif_point(pycontclass=PC, curve_name='LC_HO1', init_point_name='EQ1:H1')
track_limit_cycles_from_Hopf_bif_point(pycontclass=PC, curve_name='LC_HO2', init_point_name='EQ1:H2')
track_limit_cycles_from_Hopf_bif_point(pycontclass=PC, curve_name='LC_HO3', init_point_name='EQ1:H3')
track_limit_cycles_from_Hopf_bif_point(pycontclass=PC, curve_name='LC_HO4', init_point_name='EQ1:H4')

PC['LC_HO1'].display(['beta','Z_max'], stability=True, figure=3, label='Limit cycle bounds')
PC['LC_HO1'].display(['beta','Z_min'], stability=True, figure=3, label='Limit cycle bounds')

#PC['LC_HO2'].display(['beta','Z_max'], stability=True, figure=3)
#PC['LC_HO2'].display(['beta','Z_min'], stability=True, figure=3)
#PC['LC_HO2'].info()

#PC['LC_HO3'].display(['beta','Z_max'], stability=True, figure=3)
#PC['LC_HO3'].display(['beta','Z_min'], stability=True, figure=3)

PC['LC_HO4'].display(['beta','Z_max'], stability=True, figure=3)
PC['LC_HO4'].display(['beta','Z_min'], stability=True, figure=3)


#purple_line_normal = mlines.Line2D([], [], color='purple', linewidth=1.5, linestyle='-', label='Limit cycle bounds')
purple_line = mlines.Line2D([], [], color='purple', linewidth=1.5, linestyle='-', label='Stable limit cycle')
purple_line_dotted = mlines.Line2D([], [], color='purple', linewidth=1.5, linestyle='--', label='Unstable limit cycle')
red_diamond = mlines.Line2D([0], [0], marker='D', color='w', label='Limit point \n of cycles',
                        markerfacecolor='red', markersize=8)
plt.legend(handles=[purple_line, purple_line_dotted, red_diamond], loc='upper right')
plt.xlim(0.25, 0.8)
plt.ylim(0.15, 1.4)
plt.show()
plt.clf()
