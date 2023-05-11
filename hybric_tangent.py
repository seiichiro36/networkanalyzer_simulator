import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from measurements_transform import Open, Short

# 終端、解放時と短絡時の送電端インピーダンスの波形データ
open = Open("OPEN.CSV")
open_complex_data = np.array(open.open_parameter()[2])
open_complex_data_real = open.open_parameter()[0].flatten()

short = Short("SHORT.CSV")
short_complex_data = np.array(short.short_parameter()[2])
short_complex_data_short = short.short_parameter()[0].flatten()

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
Zino_tanh = 1 / np.tanh(complex * length)
Zins_tanh =  np.tanh(complex * length)
Zino_tanh_real = Zino_tanh.real
Zino_tanh_imag = Zino_tanh.imag
Zins_tanh_real = Zins_tanh.real
Zins_tanh_imag = Zins_tanh.imag


fig = plt.figure(figsize=(7, 5))

peaks_Zino, _ = find_peaks(Zino_tanh_real, height=50)
peaks_Zins, _ = find_peaks(Zins_tanh_real, height=50)
plt.plot(Zino_tanh_real, color="red")
plt.plot(Zins_tanh_real, color="blue")
plt.plot(peaks_Zino, Zino_tanh_real[peaks_Zino], "x", color="red")
plt.plot(peaks_Zins, Zins_tanh_real[peaks_Zins], "x", color="blue")

Zino_peaks = peaks_Zino
Zins_peaks = peaks_Zins

if __name__ == "__main__":

    plt.show()