from moving_peak_value import peak_value_difference_list_of_Zino, peak_value_difference_list_of_Zins
import matplotlib.pyplot as plt 


fig = plt.figure(figsize=(7, 5))

ax1 = fig.add_subplot(1, 2, 1)
ax1.set_xlabel("Frequency [Hz]")

ax2 = fig.add_subplot(1, 2, 2)
ax2.set_xlabel("Frequency [Hz]")

ax1.plot(peak_value_difference_list_of_Zino, "x")
ax2.plot(peak_value_difference_list_of_Zins, "o")

plt.show()