from PyDSTool import *
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import pickle


def get_max_amplitude_varying_vm3(VM3):
    # Set up parameter values changing beta for each parameter dictionary set.
    pars_reproduce_paper = {'v_0': 1,
            'k': 10,
            'k_f': 1,
            'v_1': 7.3,
            'V_M2': 65,
            'V_M3': VM3,
            'K_2': 1,
            'K_R': 2,
            'K_A': 0.9,
            'm': 2,
            'n': 2,
            'p': 4,
            'beta': 0.301
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
    pts_reproduce_paper = plotting_traj(generator_object=testDS_Dupont1990_reproduce_paper)
    max_value_Z = np.max(pts_reproduce_paper['Z'][900:])

    return max_value_Z


# array of values of vm3
vm3_value_list = list(range(200, 10000))

filename_vm3_value_list = 'vm3_value_list.pkl'
outfile_filename_vm3_value_list = open(filename_vm3_value_list,'wb')
pickle.dump(vm3_value_list,outfile_filename_vm3_value_list)
outfile_filename_vm3_value_list.close()

def paralellised_loop_append_max_val_z(iteration):
    max_val_z = get_max_amplitude_varying_vm3(VM3=iteration)
    return max_val_z

max_values_list_Z = Parallel(n_jobs=-1)(delayed(paralellised_loop_append_max_val_z)(iteration) for iteration in vm3_value_list)
print(max_values_list_Z)

filename_max_values_list_Z = 'max_values_list_Z.pkl'
outfile_filename_max_values_list_Z = open(filename_max_values_list_Z,'wb')
pickle.dump(max_values_list_Z,outfile_filename_max_values_list_Z)
outfile_filename_max_values_list_Z.close()


plt.plot(vm3_value_list, max_values_list_Z, label='Max Z values', color='red', linestyle='--', marker='o', linewidth=1, markersize=2.5)
plt.title('Amplitude of cytosolic Ca$^{2 +}$ oscillations as a function of $V_{M3}$')
plt.xlabel('Maximum rate of Ca$^{2 +}$ release in intracellular store, $V_{M3}$ ($\mu M s^{-1}$)')
plt.ylabel('Maximum amplitude of Z ($\mu M$)')
plt.legend(loc='upper right')
plt.savefig('varying_vm3.pdf')
