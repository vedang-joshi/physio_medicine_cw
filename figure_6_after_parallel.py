import matplotlib.pyplot as plt
import pickle

vm3_value_list_pkl_file_open = open("vm3_value_list.pkl", 'rb')
vm3_value_list = pickle.load(vm3_value_list_pkl_file_open)
vm3_value_list_pkl_file_open.close()

max_values_list_Z_pkl_file_open = open("max_values_list_Z.pkl", 'rb')
max_values_list_Z = pickle.load(max_values_list_Z_pkl_file_open)
max_values_list_Z_pkl_file_open.close()

plt.plot(vm3_value_list, max_values_list_Z, label='Max Z values', color='red', linestyle='--', marker='o', linewidth=1, markersize=2.5)
plt.title('Amplitude of cytosolic Ca$^{2 +}$ oscillations as a function of $V_{M3}$')
plt.xlabel('Maximum rate of Ca$^{2 +}$ release in intracellular store, $V_{M3}$ ($\mu M s^{-1}$)')
plt.ylabel('Maximum amplitude of Z ($\mu M$)')
plt.legend(loc='upper right')
plt.show()
