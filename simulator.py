import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import pandas as pd 

from measurements_transform import Open, Short

open = Open("OPEN.CSV")
open_complex_data = open.open_parameter()

short = Short("SHORT.CSV")
short_complex_data = short.short_parameter()

#グラフデータ
Frequency = np.arange(60000, 30000001, 59880)
y = 0 * Frequency

#伝送法による減衰比
actual_data = pd.read_csv("TRANSMISSION.CSV", usecols=[0], header=None)
#無損失の場合
C = 102e-12
Z = 50
L = 50**2 * C

omega = Frequency * 2 * np.pi

beta = omega * np.sqrt(C * L)

#スケール用関数
def change(value):
    length = float(value)
    complex = ((np.log(10 ** (abs(actual_data)/20))/length).values).flatten() + np.array(beta) * 1j
    Zins = 50 * np.tanh(complex * length)
    Zino = 50 / np.tanh(complex * length)
    Zins_real = Zins.real
    Zins_imag = Zins.imag
    Zino_real = Zino.real
    Zino_imag = Zino.imag
    line1.set_ydata(Zins_real)
    line2.set_ydata(Zins_imag)
    line3.set_ydata(Zino_real)
    line4.set_ydata(Zino_imag)
    canvas.draw()
    
root = tkinter.Tk()
root.title("matplotlib 埋め込み")



#グラフ用オブジェクト生成
fig = Figure(figsize=(12, 8)) 
ax = fig.add_subplot(1, 1, 1)        
line1, = ax.plot(Frequency, y, color="red", label="short_real")                 
line2, = ax.plot(Frequency, y, color="red", linestyle="dotted", label="short_imag")   
line3, = ax.plot(Frequency, y, color="blue", label="open_real")                 
line4, = ax.plot(Frequency, y, color="blue", linestyle="dotted", label="open_imag")   
ax.plot(Frequency, short_complex_data[0], color="green", linestyle = "dotted")
ax.plot(Frequency, open_complex_data[0], color="black", linestyle = "dotted")
ax.plot(Frequency, short_complex_data[1], color="green", linestyle = "dotted")
ax.plot(Frequency, open_complex_data[1], color="black", linestyle = "dotted")

#Figureを埋め込み
canvas = FigureCanvasTkAgg(fig, root)

canvas.get_tk_widget().pack()

#ツールバーを表示
toolbar=NavigationToolbar2Tk(canvas, root)
ax.set_xlim([60000, 30000000])

#スケール
s = tkinter.Scale(
    root,
    orient="horizontal",    #方向
    command=change,  #調整時に実行
    width=30,
    length=500,
    from_=0,
    to=30,
    resolution=0.1
    )
s.pack()

root.mainloop()
