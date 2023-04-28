import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import pandas as pd 

from measurements_transform import Open, Short

open = Open("OPEN.CSV")
open_complex_data = open.open_parameter()

short = Short("SHORT.CSV")
short_complex_data = short.short_parameter()

#グラフデータ
Frequency = np.arange(60000, 30000001, 59880)

#伝送法による減衰比
actual_data = pd.read_csv("TRANSMISSION.CSV", usecols=[0], header=None)
#無損失の場合
C = 102e-12
Z = 50
L = 50**2 * C

omega = Frequency * 2 * np.pi

beta = omega * np.sqrt(C * L)

Frequency = np.arange(60000, 30000001, 59880)

length = np.arange(0.01, 30.01, (30.0-0.01)/500)  # shape is (501,)
arr2 = np.ones((501, 501))

length_2d = length.reshape(-1, 1)  # reshape to (501, 1)
result = length_2d * arr2  # broadcastable now


complex = (np.log(10 ** (abs(actual_data)/20)).values)/(length).flatten() + np.array(beta) * 1j
Zins = 50 * np.tanh(complex * length)

Zin_real = Zins.real

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(Frequency, Zin_real, result, color='red')

plt.show()
