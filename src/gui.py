import tkinter as tk
from tkinter import filedialog
import csv

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from systems import primer_orden, ARX_filter

seconds = 0

input_to_the_system = 0
disturbance_value = 0
tau_value = 1
T_value = 1
gain_value = 0
theta_prima_value = 0

number_of_coefficients = 0
a_list = []
b_list = []
d_value = 0

x = []
y = []


def enter(tipoDePlanta, tipoDeEntrada, perturbacionHab):
    global input_to_the_system
    global disturbance_value
    global tau_value
    global T_value
    global gain_value
    global theta_prima_value

    print("Entrada")
    if tipoDeEntrada.get() == 0:
        print(magnitud_escalon.get())
        input_to_the_system = float(magnitud_escalon.get())
    elif tipoDeEntrada.get() == 1:
        content = buscar_archivo()
        print(content)

        input_to_the_system = content

    print("Perturbacion")
    if perturbacionHab.get() == 0:
        print("No hay Perturbacion")
        disturbance_value = 0
    elif perturbacionHab.get() == 1:
        print(magnitud_escalon_per.get())
        disturbance_value = float(magnitud_escalon_per.get())

    print("Planta")
    if tipoDePlanta.get() == 0:

        gain_value = float(gain.get())
        tau_value = float(tao.get())
        theta_prima_value = float(thetaprima.get())
        T_value = float(periodo.get())
        T_value = T_value if T_value != 0 else 1
        tau_value = tau_value if tau_value != 0 else 1
        #y = primer_orden(float(periodo.get()), float(tao.get()), float(gain.get()), seconds, float(thetaprima.get()), input_to_the_system)
        #plot_simulation_foh(periodo.get(), tao.get(), gain.get(),thetaprima.get(),input_to_the_system,disturbance,seconds, ventana)

    elif tipoDePlanta.get() == 1:


        number_of_coefficients = coe.get()
        a_list = [ int(x) for x in a.get().split(",")]
        b_list = [ int(x) for x in b.get().split(",")]
        d_value = d.get()



def reset():
    global x
    global y
    global seconds
    x = []
    y = []
    ax.clear()
    seconds = 0


def planta():
    tk.Label(ventana, text="Simulador computacional de Plantas",
             font="Verdana 10 bold").grid(row=0, column=2)

    tk.Label(ventana, text="Planta",
             font="Verdana 10 bold").grid(row=1, column=2)

    row_c = 4
    col_c = 0

    etiqueta_gain = tk.Label(ventana, text="Gain").grid(
        row=row_c, column=col_c)
    etiqueta_tao = tk.Label(ventana, text="Tao").grid(
        row=row_c + 1, column=col_c)
    etiqueta_periodo = tk.Label(ventana, text="Periodo").grid(
        row=row_c + 2, column=col_c)
    etiqueta_thetaprima = tk.Label(
        ventana, text="Theta Prima").grid(row=row_c+3, column=col_c)

    row_c = 4
    col_c = 2

    etiqueta_coe = tk.Label(ventana, text="Numero de coeficientes").grid(
        row=row_c, column=col_c)
    etiqueta_a = tk.Label(ventana, text="a's").grid(
        row=row_c + 1, column=col_c)
    etiqueta_b = tk.Label(ventana, text="b's").grid(
        row=row_c + 2, column=col_c)
    etiqueta_d = tk.Label(ventana, text="d's").grid(
        row=row_c + 3, column=col_c)

    gain.grid(row=4, column=0 + 1)
    tao.grid(row=4 + 1, column=0 + 1)
    periodo.grid(row=4 + 2, column=0 + 1)
    thetaprima.grid(row=4 + 3, column=0 + 1)

    coe.grid(row=4, column=2 + 1)
    a.grid(row=4 + 1, column=2 + 1)
    b.grid(row=4 + 2, column=2 + 1)
    d.grid(row=4 + 3, column=2 + 1)

    tk.Radiobutton(ventana, text="FOH", variable=tipoDePlanta,
                   value=0).grid(row=3, column=1)
    tk.Radiobutton(ventana, text="ARX", variable=tipoDePlanta,
                   value=1).grid(row=3, column=3)


def buscar_archivo():
    file = filedialog.askopenfile(
        parent=ventana, mode='rb', title='Choose a file')

    if file is not None:
        content = file.read()
        content = content.decode("utf-8") 
        content = [ int(x) for x in content.split(",")]

        return content
    print("no se pudo acceder al archivo")


def entrada():
    entrada_row = 9
    entrada_col = 2

    tk.Label(ventana, text="Entrada", font="Verdana 10 bold").grid(
        row=entrada_row, column=2)
    tk.Radiobutton(ventana, text="Escalon", variable=tipoDeEntrada,
                   value=0).grid(row=entrada_row+1, column=1)
    tk.Radiobutton(ventana, text="Archivo", variable=tipoDeEntrada,
                   value=1).grid(row=entrada_row+1, column=2)

    etiqueta_magnitud_escalon = tk.Label(ventana, text="Magnitud").grid(
        row=entrada_row + 2, column=entrada_col - 2)
    magnitud_escalon.grid(row=entrada_row + 2, column=entrada_col - 1)

    tk.Button(ventana, text="Buscar", command=buscar_archivo).grid(
        row=entrada_row + 2, column=1 + 1)


def perturbacion():
    per_row = 12
    per_col = 2

    tk.Label(ventana, text="Perturbacion",
             font="Verdana 10 bold").grid(row=per_row, column=2)

    check_box = tk.Checkbutton(
        ventana, text="Activar", variable=perturbacionHab, onvalue=1, offvalue=0)
    check_box.grid(row=per_row + 1, column=1)

    etiqueta_magnitud_escalon = tk.Label(ventana, text="Magnitud").grid(
        row=per_row + 2, column=per_col - 2)
    magnitud_escalon_per.grid(row=per_row + 2, column=per_col - 1)


def final_buttons():

    tk.Label(ventana, text="Ejecutar",
             font="Verdana 10 bold").grid(row=17, column=6)

    tk.Button(ventana, text="Enter", command=lambda: enter(
        tipoDePlanta, tipoDeEntrada, perturbacionHab)).grid(row=18, column=3)
    tk.Button(ventana, text="Reset", command=reset).grid(row=18, column=4)


ventana = tk.Tk()
ventana.geometry("1500x1000")

tipoDePlanta = tk.IntVar()
tipoDeEntrada = tk.IntVar()
perturbacionHab = tk.IntVar()

gain = tk.Entry(ventana)
tao = tk.Entry(ventana)
periodo = tk.Entry(ventana)
thetaprima = tk.Entry(ventana)
coe = tk.Entry(ventana)
a = tk.Entry(ventana)
b = tk.Entry(ventana)
d = tk.Entry(ventana)

magnitud_escalon = tk.Entry(ventana)
magnitud_escalon_per = tk.Entry(ventana)


planta()
entrada()
perturbacion()
final_buttons()


figure = plt.Figure(figsize=(6, 5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, ventana)
chart_type.get_tk_widget().grid(row=19, column=6)

figure_input = plt.Figure(figsize=(6, 5), dpi=100)
ax_input = figure.add_subplot(111)
chart_type_input = FigureCanvasTkAgg(figure_input, ventana)
chart_type_input.get_tk_widget().grid(row=19, column=7)


#ax.axis([0, 60, 0, 100])
# number_of_coefficients, a_values, b_values, delay, k, input_to_the_system
ticks = 0

while True:
    ventana.update_idletasks()
    ventana.update()
    ax.plot(x, y, 'r-')
    #ax.scatter(seconds, y + disturbance_value)
    plt.pause(0.05)
    ticks += 0.05
    chart_type.draw()
    if(ticks >= 0.1):
        if tipoDePlanta.get() == 0:
            y_value = primer_orden(T_value, tau_value, gain_value,
                                   seconds, theta_prima_value, input_to_the_system)
        else:
            #y_value = ARX_filter(int(number_of_coefficients), a_list, b_list, int(d_value), seconds, input_to_the_system )
            pass
        print(y_value)
        y.append(y_value + disturbance_value)
        x.append(len(y) - 1)
        seconds += 1
        ticks = 0
    # plt.show()
