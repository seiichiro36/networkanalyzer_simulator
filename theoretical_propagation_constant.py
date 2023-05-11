import matplotlib.pyplot as plt
import numpy as np

from actual_damping import actual_data
from characteristic_impedance import Characteristic_impedance
from theoretical import beta
# from graph_pahse import beta




complex = (actual_data).flatten() + np.array(beta) * 1j

Zins = 50 * np.tanh(complex * 4)
Zino = 50 / np.tanh(complex * 4)

characteristic_impedance_theoritical = Characteristic_impedance(Zins, Zino)



if __name__ ==  "__main__":
    Frequency = np.arange(60000, 30000001, 59880)
    fig = plt.figure(figsize=(12, 8))
    
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_xlabel("Frequency [Hx]")
    ax1.set_ylabel("Phase [rad/m]")

    ax1.plot(
        Frequency, characteristic_impedance_theoritical.characteristic_impedance()[0])
    ax1.plot(
        Frequency, characteristic_impedance_theoritical.characteristic_impedance()[0])
    ax1.plot(Frequency, Zins.real)
    ax1.plot(Frequency, Zino.real)
    plt.show()