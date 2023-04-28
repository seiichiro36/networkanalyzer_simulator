import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import numpy as np
import pandas as pd

from measurements_transform import Open, Short

open = Open("OPEN.CSV")
open_complex_data = open.open_parameter()

short = Short("SHORT.CSV")
short_complex_data = short.short_parameter()

# グラフデータ

# 伝送法による減衰比
actual_data = pd.read_csv("TRANSMISSION.CSV", usecols=[0], header=None)
# 無損失の場合
C = 102e-12
Z = 50
L = 50**2 * C

Frequency = np.arange(60000, 30000001, 59880)
omega = Frequency * 2 * np.pi

beta = omega * np.sqrt(C * L)


def _update(frames, Frequency, waveform):
    """グラフを更新するための関数"""

    complex = ((np.log(10 ** (abs(actual_data)/20)).values) /
               frames).flatten() + np.array(beta) * 1j
    Zins = 50 * np.tanh(complex * frames)
    Zino = 50 / np.tanh(complex * frames)

    plt.cla()
    # データを更新 (追加) する
    Frequency = np.arange(60000, 30000001, 59880)
    waveform_short_real = (Zins.real)
    waveform_open_real = (Zino.real)
    # 折れ線グラフを再描画する
    plt.plot(Frequency, waveform_short_real)
    plt.plot(Frequency, waveform_open_real)


def main():
    # 描画領域
    fig = plt.figure(figsize=(10, 6))
    # 描画するデータ (最初は空っぽ)
    waveform_short_real = 0
    waveform_open_real = 0

    params = {
        'fig': fig,
        'func': _update,  # グラフを更新する関数
        'fargs': (Frequency, waveform_short_real),  # 関数の引数 (フレーム番号を除く)
        'fargs': (Frequency, waveform_open_real),  # 関数の引数 (フレーム番号を除く)
        'interval': 10,  # 更新間隔 (ミリ秒)
        'frames': np.arange(1, 30, 0.1),  # フレーム番号を生成するイテレータ
        'repeat': True,
    }
    anime = animation.FuncAnimation(**params)

    # グラフを表示する
    plt.show()

if __name__ == '__main__':
    main()
