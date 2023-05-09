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
Zino = 50 / np.tanh(complex * length)
Zins = 50 * np.tanh(complex * length)
Zins_real = Zins.real
Zins_imag = Zins.imag
Zino_real = Zino.real
Zino_imag = Zino.imag

fig = plt.figure(figsize=(7, 5))

peaks_Zino, _ = find_peaks(Zino_real, height=50)
peaks_Zins, _ = find_peaks(Zins_real, height=50)
plt.plot(Zino_real, color="red")
plt.plot(Zins_real, color="blue")
plt.plot(peaks_Zino, Zino_real[peaks_Zino], "x", color="red")
plt.plot(peaks_Zins, Zins_real[peaks_Zins], "x", color="blue")

peaks_Zino_actual, _ = find_peaks(open_complex_data_real, height=50)
peaks_Zins_actual, _ = find_peaks(short_complex_data_short, height=50)

plt.plot(open_complex_data_real, color="green")
plt.plot(short_complex_data_short, color="purple")
plt.plot(peaks_Zino_actual, open_complex_data_real[peaks_Zino_actual], "o", color="red")
plt.plot(peaks_Zins_actual, short_complex_data_short[peaks_Zins_actual], "o", color="blue")


plt.show()


print("解放時送電端インピーダンスのピーク値インデックス: ", peaks_Zino)
print("短絡時送電端インピーダンスのピーク値インデックス: ", peaks_Zins)
print("解放時送電端インピーダンスのピーク値インデックス(実測値): ",  peaks_Zino_actual)
print("短絡時送電端インピーダンスのピーク値インデックス(実測値): ",  peaks_Zins_actual)


print(Zino[peaks_Zino])
print(Zins[peaks_Zins])
print(open_complex_data[peaks_Zino_actual])
print(short_complex_data[peaks_Zins_actual]) 

print(Zino[peaks_Zino] - open_complex_data[peaks_Zino_actual])
print(Zins[peaks_Zins] - open_complex_data[peaks_Zino_actual])
 
