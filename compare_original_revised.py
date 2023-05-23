from matplotlib.ticker import ScalarFormatter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

from measurements_transform import Open, Short
from graph import difference_propagation
from graph import difference_phase

fig = plt.figure(figsize=(7, 5))

ax1 = fig.add_subplot(2, 1, 1)
ax1.set_xlabel("Frequency [Hz]")
ax1.set_ylabel("Transmission end impedance[Ω]")
ax2 = fig.add_subplot(2, 1, 2)
ax2.set_xlabel("Frequency [Hz]")
ax2.set_ylabel("Transmission end impedance[Ω]")

# 終端、解放時と短絡時の送電端インピーダンスの波形データ
open = Open("OPEN.CSV")
open_complex_data = np.array(open.open_parameter()[2])
open_complex_data_real = open.open_parameter()[0].flatten()

short = Short("SHORT.CSV")
short_complex_data = np.array(short.short_parameter()[2])
short_complex_data_real = short.short_parameter()[0].flatten()


# ケーブルの長さ
length = 10.8

Frequency = np.arange(60000, 30000001, 59880)
# 位相定数(無損失時)

C = 102e-12
Z = 50
L = 50**2 * C

omega = Frequency * 2 * np.pi

beta = omega * np.sqrt(C * L)

# 伝送法による減衰比(10.8mのケーブルを使用)
actual_data = pd.read_csv("TRANSMISSION.CSV", usecols=[0], header=None)
actual_data = np.log(10 ** (abs(actual_data)/20))/length
actual_data = actual_data.values

# # 伝搬定数
gamma = actual_data.flatten() + (np.array(beta)) * 1j
gamma_revise = actual_data.flatten() + difference_propagation + (np.array(beta) + difference_phase) * 1j 

# 教科書より、終端解放時と短絡時の送電端インピーダンスをそれぞれ出力
Zino = 50 / np.tanh(gamma * length)
Zins = 50 * np.tanh(gamma * length)
Zino_revise = 50 / np.tanh(gamma_revise * length)
Zins_revise = 50 * np.tanh(gamma_revise * length)
Zino_real = Zino.real
Zins_real = Zins.real
Zino_real_revise = Zino_revise.real
Zins_real_revise = Zins_revise.real

peaks_Zino, _ = find_peaks(Zino_real, height=50)
peaks_Zins, _ = find_peaks(Zins_real, height=50)
peaks_Zino_revise, _ = find_peaks(Zino_real, height=50)
peaks_Zins_revise, _ = find_peaks(Zins_real, height=50)
peaks_Zino_actual, _ = find_peaks(open_complex_data_real, height=50)
peaks_Zins_actual, _ = find_peaks(short_complex_data_real, height=50)

# ピークの横軸と縦軸の値を取得
peak_Frequency_of_Zino = Frequency[peaks_Zino]
peak_Zino_real = Zino_real[peaks_Zino]
peak_Frequency_of_Zins = Frequency[peaks_Zins]
peak_Zins_real = Zins_real[peaks_Zins]

peak_Frequency_of_Zino_revise = Frequency[peaks_Zino_revise]
peak_Zino_real_revise = Zino_real[peaks_Zino_revise]
peak_Frequency_of_Zins_revise = Frequency[peaks_Zins_revise]
peak_Zins_real_revise = Zins_real[peaks_Zins_revise]

peak_Frequency_of_Zino_actual = Frequency[peaks_Zino_actual]
peak_Zino_real_actual = open_complex_data_real[peaks_Zino_actual]
peak_Frequency_of_Zins_actual = Frequency[peaks_Zins_actual]
peak_Zins_real_actual = short_complex_data_real[peaks_Zins_actual]


# グラフをプロット
ax1.plot(Frequency, Zino_real, color="red")  
ax1.plot(Frequency, Zins_real, color="blue")  
ax1.plot(Frequency, open_complex_data_real, color="red", linestyle="dotted")  
ax1.plot(Frequency, short_complex_data_real, color="blue", linestyle="dotted")  
ax2.plot(Frequency, Zino_real_revise, color="red")  
ax2.plot(Frequency, Zins_real_revise, color="blue")  
ax2.plot(Frequency, open_complex_data_real, color="red", linestyle="dotted")  
ax2.plot(Frequency, short_complex_data_real, color="blue", linestyle="dotted")  

ax1.plot(peak_Frequency_of_Zino, peak_Zino_real, 'x', color="red")
ax1.plot(peak_Frequency_of_Zins, peak_Zins_real, 'x', color="blue")

ax2.plot(peak_Frequency_of_Zino_revise, peak_Zino_real_revise, 'o', color="red")
ax2.plot(peak_Frequency_of_Zins_revise, peak_Zins_real_revise, 'o', color="blue")
fig.tight_layout()

ax1.ticklabel_format(style='plain', axis='x')
ax1.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax1.ticklabel_format(style="sci",  axis="x", scilimits=(6, 6))

ax2.ticklabel_format(style='plain', axis='x')
ax2.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax2.ticklabel_format(style="sci",  axis="x", scilimits=(6, 6))

plt.show()

    