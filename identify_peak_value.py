
# Zino_peaks = peaks_Zino
# Zins_peaks = peaks_Zins
# peaks_Zino_actual = peaks_Zino_actual
# peaks_Zins_actual = peaks_Zins_actual

# if __name__ == "__main__":

#     plt.show()
from matplotlib.ticker import ScalarFormatter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

from measurements_transform import Open, Short

fig = plt.figure(figsize=(7, 5))

ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("Transmission end impedance[Ω]")

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
Zino = 50 / np.tanh(complex * length)
Zins = 50 * np.tanh(complex * length)
Zino_real = Zino.real
Zins_real = Zins.real

peaks_Zino, _ = find_peaks(Zino_real, height=50)
peaks_Zins, _ = find_peaks(Zins_real, height=50)
peaks_Zino_actual, _ = find_peaks(open_complex_data_real, height=50)
peaks_Zins_actual, _ = find_peaks(short_complex_data_real, height=50)

# ピークの横軸と縦軸の値を取得
peak_Frequency_of_Zino = Frequency[peaks_Zino]
peak_Zino_real = Zino_real[peaks_Zino]
peak_Frequency_of_Zins = Frequency[peaks_Zins]
peak_Zins_real = Zins_real[peaks_Zins]
peak_Frequency_of_Zino_actual = Frequency[peaks_Zino_actual]
peak_Zino_real_actual = open_complex_data_real[peaks_Zino_actual]
peak_Frequency_of_Zins_actual = Frequency[peaks_Zins_actual]
peak_Zins_real_actual = short_complex_data_real[peaks_Zins_actual]


# グラフをプロット
ax.plot(Frequency, Zino_real)  
ax.plot(Frequency, Zins_real)  
ax.plot(Frequency, open_complex_data_real)  
ax.plot(Frequency, short_complex_data_real)  
ax.plot(peak_Frequency_of_Zino, peak_Zino_real, 'x')
ax.plot(peak_Frequency_of_Zins, peak_Zins_real, 'x')
ax.plot(peak_Frequency_of_Zino_actual, peak_Zino_real_actual, 'o')
ax.plot(peak_Frequency_of_Zins_actual, peak_Zins_real_actual, 'o')
fig.tight_layout()

ax.ticklabel_format(style='plain', axis='x')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.ticklabel_format(style="sci",  axis="x", scilimits=(6, 6))

plt.show()

# print("終端解放時送電端員ピーンダンスのピーク値",peak_Frequency_of_Zino)
# print(peak_Frequency_of_Zino_actual)
# print(peak_Frequency_of_Zins)
# print(peak_Frequency_of_Zins_actual)