from PyDSTool import *
import matplotlib.pyplot as plt


# Set up parameter values changing beta for each parameter dictionary set.
pars_reproduce_paper = {'v_0': 1,
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

pars_vary_beta_1 = {'v_0': 1,
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
                        'beta': 0
                        }

pars_vary_beta_2 = {'v_0': 1,
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
                        'beta': 0.201
                        }

pars_vary_beta_3 = {'v_0': 1,
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
                        'beta': 0.601
                        }

pars_vary_beta_4 = {'v_0': 1,
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
                        'beta': 0.801
                        }

# Set up initial conditions dictionary start at Z = Y =0.
initialConditionsDict = {'Z': 0, 'Y': 0}

# Set up model with the auxiliary function and the Z and Y ODE system.
auxiliaryFunctionDict = {'v_2': (['Z'], 'V_M2*((Z^n)/(K_2^n + Z^n))'),
                         'v_3': (['Z','Y'], 'V_M3*((Y^m)/(K_R^m + Y^m))*((Z^p)/(K_A^p + Z^p))')
                         }

Zstr = 'v_0 + v_1*beta - v_2(Z) + v_3(Z,Y) + k_f*Y - k*Z'
Ystr = 'v_2(Z) - v_3(Z,Y) - k_f*Y'


def create_pydstools_generator_object(parameter_set, name):
    '''
    Function to create a pydstools generator object from the ode system as given above.
    :param parameter_set: The set of parameters to apply to system of ODEs.
    :param name: Name of generator (may be used to refer to particular generator)
    :return: Generator object
    '''
    DSargs = args(name=name)
    DSargs.pars = parameter_set
    DSargs.varspecs = {'Z': Zstr, 'Y': Ystr}
    DSargs.fnspecs = auxiliaryFunctionDict
    DSargs.tdomain = [0,10]                         # set the range of integration.
    DSargs.xdomain = {'Z': [-3, 3], 'Y': [-1, 2.5]}
    DSargs.ics = initialConditionsDict

    testDS = Generator.Vode_ODEsystem(DSargs)
    return testDS

def plotting_traj(generator_object):
    '''
    Function to generate trajectories and points based off the generator object
    :param generator_object: generator object obtained from the function 'create_pydstools_generator_object'
    :return: points list
    '''
    traj = generator_object.compute('pol')
    pts = traj.sample(dt=0.01)
    return pts

# Create generator objects and plot trajectories for different parameter values
testDS_Dupont1990_reproduce_paper = create_pydstools_generator_object(parameter_set=pars_reproduce_paper, name='Dupont1990_reproduce_paper')
testDS_Dupont1990_vary_beta_1 = create_pydstools_generator_object(parameter_set=pars_vary_beta_1, name='Dupont1990_reproduce_paper')
testDS_Dupont1990_vary_beta_2 = create_pydstools_generator_object(parameter_set=pars_vary_beta_2, name='Dupont1990_reproduce_paper')
testDS_Dupont1990_vary_beta_3 = create_pydstools_generator_object(parameter_set=pars_vary_beta_3, name='Dupont1990_reproduce_paper')
testDS_Dupont1990_vary_beta_4 = create_pydstools_generator_object(parameter_set=pars_vary_beta_4, name='Dupont1990_reproduce_paper')


pts_reproduce_paper = plotting_traj(generator_object=testDS_Dupont1990_reproduce_paper)
pts_vary_beta_1 = plotting_traj(generator_object=testDS_Dupont1990_vary_beta_1)
pts_vary_beta_2 = plotting_traj(generator_object=testDS_Dupont1990_vary_beta_2)
pts_vary_beta_3 = plotting_traj(generator_object=testDS_Dupont1990_vary_beta_3)
pts_vary_beta_4 = plotting_traj(generator_object=testDS_Dupont1990_vary_beta_4)



########## Calcium concentrations in time plotting code ###########

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
fig.suptitle('Oscillations in cytosolic Ca$^{2 +}$: Varying parameter $\\beta$')

# Set up figure panels:
ax1.plot(pts_reproduce_paper['t'], pts_reproduce_paper['Z'], label='Z trajectory')
ax1.plot(pts_reproduce_paper['t'], pts_reproduce_paper['Y'], label='Y trajectory')

ax2.plot(pts_vary_beta_1['t'], pts_vary_beta_1['Z'], label='Z trajectory')
ax2.plot(pts_vary_beta_1['t'], pts_vary_beta_1['Y'], label='Y trajectory')

ax3.plot(pts_vary_beta_2['t'], pts_vary_beta_2['Z'], label='Z trajectory')
ax3.plot(pts_vary_beta_2['t'], pts_vary_beta_2['Y'], label='Y trajectory')

ax4.plot(pts_vary_beta_3['t'], pts_vary_beta_3['Z'], label='Z trajectory')
ax4.plot(pts_vary_beta_3['t'], pts_vary_beta_3['Y'], label='Y trajectory')

ax5.plot(pts_vary_beta_4['t'], pts_vary_beta_4['Z'], label='Z trajectory')
ax5.plot(pts_vary_beta_4['t'], pts_vary_beta_4['Y'], label='Y trajectory')

fig.supxlabel('Time (s)')
fig.supylabel('Ca$^{2+}$ in the cytosol ($\mu M$)')
ax1.legend(title='$\\beta$ = 0.301', loc='upper right')
ax2.legend(title='$\\beta$ = 0', loc='upper right')
ax3.legend(title='$\\beta$ = 0.201', loc='upper right')
ax4.legend(title='$\\beta$ = 0.601', loc='upper right')
ax5.legend(title='$\\beta$ = 0.801', loc='upper right')

for ax in fig.get_axes():
    ax.label_outer()

plt.show()
