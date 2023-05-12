from matplotlib.ticker import ScalarFormatter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

from measurements_transform import Open, Short

fig = plt.figure(figsize=(7, 5))

ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel("Frequency [Hz]")

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

# 伝搬定数
complex = (actual_data).flatten() + np.array(beta) * 1j

# 教科書より、終端解放時と短絡時の送電端インピーダンスをそれぞれ出力
tanh_of_Zino = 1 / np.tanh(complex * length)
tanh_of_Zins = np.tanh(complex * length)
tanh_of_Zino_real = tanh_of_Zino.real
tanh_of_Zins_real = tanh_of_Zins.real

tanh_open_complex_data = open_complex_data / 50
tanh_short_complex_data = short_complex_data / 50

tanh_open_complex_data_real = tanh_open_complex_data.real
tanh_short_complex_data_real = tanh_short_complex_data.real

peaks_tanh_of_Zino, _ = find_peaks(tanh_of_Zino_real, height=1)
peaks_tanh_of_Zins, _ = find_peaks(tanh_of_Zins_real, height=1)
peaks_tanh_Zino_actual, _ = find_peaks(tanh_open_complex_data_real, height=1)
peaks_tanh_Zins_actual, _ = find_peaks(tanh_short_complex_data_real, height=1)

# ピークの横軸と縦軸の値を取得
tanh_peak_Frequency_of_Zino = Frequency[peaks_tanh_of_Zino]
tanh_peak_Zino_real = tanh_of_Zino_real[peaks_tanh_of_Zino]
tanh_peak_Frequency_of_Zins = Frequency[peaks_tanh_of_Zins]
tanh_peak_Zins_real = tanh_of_Zins_real[peaks_tanh_of_Zins]
tanh_peak_Frequency_of_Zino_actual = Frequency[peaks_tanh_Zino_actual]
tanh_peak_Zino_real_actual = tanh_open_complex_data_real[peaks_tanh_Zino_actual]
tanh_peak_Frequency_of_Zins_actual = Frequency[peaks_tanh_Zins_actual]
tanh_peak_Zins_real_actual = tanh_short_complex_data_real[peaks_tanh_Zins_actual]


# グラフをプロット
ax.plot(Frequency, tanh_of_Zino_real, color="red")  
ax.plot(Frequency, tanh_of_Zins_real, color="blue")  
ax.plot(Frequency, tanh_open_complex_data_real, color="red", linestyle="dotted")  
ax.plot(Frequency, tanh_short_complex_data_real, color="blue", linestyle="dotted")  
ax.plot(tanh_peak_Frequency_of_Zino, tanh_peak_Zino_real, 'x', color="red")
ax.plot(tanh_peak_Frequency_of_Zins, tanh_peak_Zins_real, 'x', color="blue")
ax.plot(tanh_peak_Frequency_of_Zino_actual, tanh_peak_Zino_real_actual, 'o', color="red")
ax.plot(tanh_peak_Frequency_of_Zins_actual, tanh_peak_Zins_real_actual, 'o', color="blue")
fig.tight_layout()

ax.ticklabel_format(style='plain', axis='x')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="x", scilimits=(6, 6))

# print("終端解放時送電端インピーンダンスのピーク値", Zino[peaks_Zino])
# print("終端短絡時送電端インピーンダンスのピーク値(実測)", open_complex_data[peaks_Zino_actual])
# print("終端解放時送電端インピーンダンスのピーク値", Zins[peaks_Zins])
# print("終端短絡時送電端インピーンダンスのピーク値(実測)", short_complex_data[peaks_Zins_actual])

# print("終端解放時送電端インピーンダンスのピーク値(実測値との差)", open_complex_data[peaks_Zino_actual] - Zino[peaks_Zino])
# print("終端短絡時送電端インピーンダンスのピーク値(実測値との差)", short_complex_data[peaks_Zins_actual] - Zins[peaks_Zins])

# tanh_of_open_complex_data = open_complex_data/ 50

print("終端解放時送電端インピーンダンスのピーク値", tanh_of_Zino[peaks_tanh_of_Zino])
print("終端短絡時送電端インピーンダンスのピーク値(実測)", tanh_open_complex_data[peaks_tanh_Zino_actual])
print("終端解放時送電端インピーンダンスのピーク値", tanh_of_Zins[peaks_tanh_of_Zins])
print("終端短絡時送電端インピーンダンスのピーク値(実測)", tanh_short_complex_data[peaks_tanh_Zins_actual])

# print("終端解放時送電端インピーンダンスのピーク値(実測値との差)", open_complex_data[peaks_Zino_actual] - Zino[peaks_Zino])
# print("終端短絡時送電端インピーンダンスのピーク値(実測値との差)", short_complex_data[peaks_Zins_actual] - Zins[peaks_Zins])


# plt.show()