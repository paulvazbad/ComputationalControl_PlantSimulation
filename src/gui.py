import tkinter  as tk
from tkinter import filedialog
import csv

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import plot_simulation_foh

seconds = 0
def enter(tipoDePlanta, tipoDeEntrada, perturbacionHab):


    print("Entrada")
    if tipoDeEntrada.get() == 0:
        print(magnitud_escalon.get())
        input_to_the_system = magnitud_escalon.get()
    elif tipoDeEntrada.get() == 1:
        content = buscar_archivo()
        print(content)
        input_to_the_system = content

    print("Perturbacion")
    if perturbacionHab.get() == 0:
        print("No hay Perturbacion")
        disturbance = 0
    elif perturbacionHab.get() == 1:
        print(magnitud_escalon_per.get())
        disturbance = magnitud_escalon_per.get()
    print("Planta")
    if tipoDePlanta.get() == 0:

        print(gain.get())
        print(tao.get())
        print(tiempomuerto.get())
        print(periodo.get())
        print(thetaprima.get())

        plot_simulation_foh(periodo.get(), tao.get(), gain.get(),thetaprima.get(),input_to_the_system,disturbance,seconds, ventana)

    elif tipoDePlanta.get() == 1:
        
        print(coe.get())
        print(a.get())
        print(b.get())
        print(d.get())

    

def reset():
    pass

def planta():
    tk.Label(ventana, text = "Simulador computacional de Plantas", font = "Verdana 10 bold").grid(row = 0, column = 2)

    tk.Label(ventana, text = "Planta", font = "Verdana 10 bold").grid(row = 1, column = 2)

    row_c = 4
    col_c = 0

    etiqueta_gain = tk.Label(ventana, text = "Gain").grid(row = row_c, column = col_c)
    etiqueta_tao = tk.Label(ventana, text = "Tao").grid(row = row_c +1, column = col_c)
    etiqueta_tiempomuerto = tk.Label(ventana, text = "Tiempo Muerto").grid(row = row_c +2, column = col_c)
    etiqueta_periodo = tk.Label(ventana, text = "Periodo").grid(row = row_c +3, column = col_c)
    etiqueta_thetaprima = tk.Label(ventana, text = "Theta Prima").grid(row = row_c+4, column = col_c)

    row_c = 4
    col_c = 2

    etiqueta_coe = tk.Label(ventana, text = "Numero de coeficientes").grid(row = row_c, column = col_c)
    etiqueta_a = tk.Label(ventana, text = "a's").grid(row = row_c +1, column = col_c)
    etiqueta_b = tk.Label(ventana, text = "b's").grid(row = row_c +2, column = col_c)
    etiqueta_d = tk.Label(ventana, text = "d's").grid(row = row_c +3, column = col_c)

    gain.grid(row = 4, column = 0 + 1)
    tao.grid(row = 4 + 1, column = 0 + 1)
    tiempomuerto.grid(row = 4 + 2, column = 0 + 1)
    periodo.grid(row = 4 + 3, column = 0 + 1)
    thetaprima.grid(row = 4 + 4, column = 0 + 1)

    coe.grid(row = 4, column = 2 + 1)
    a.grid(row = 4 + 1, column = 2 + 1)
    b.grid(row = 4 + 2, column = 2 + 1)
    d.grid(row = 4 + 3, column = 2 + 1)

    tk.Radiobutton(ventana, text = "FOH", variable = tipoDePlanta, value = 0).grid(row =  3, column = 1)
    tk.Radiobutton(ventana, text = "ARX", variable = tipoDePlanta, value = 1).grid(row = 3, column = 3)

def buscar_archivo():
    file = filedialog.askopenfile(parent=ventana,mode='rb',title='Choose a file')

    if file is not None: 
        content = file.read() 
        return content
    print("no se pudo acceder al archivo")

def entrada():
    entrada_row = 9
    entrada_col = 2

    tk.Label(ventana, text = "Entrada", font = "Verdana 10 bold").grid(row = entrada_row, column = 2)
    tk.Radiobutton(ventana, text = "Escalon", variable = tipoDeEntrada, value = 0).grid(row =  entrada_row+1, column = 1)
    tk.Radiobutton(ventana, text = "Archivo", variable = tipoDeEntrada, value = 1).grid(row = entrada_row+1, column = 2)

    etiqueta_magnitud_escalon = tk.Label(ventana, text = "Magnitud").grid(row = entrada_row + 2, column = entrada_col - 2)
    magnitud_escalon.grid(row = entrada_row + 2, column = entrada_col - 1)

    tk.Button(ventana, text = "Buscar", command = buscar_archivo).grid(row = entrada_row + 2, column = 1 + 1)

def perturbacion():
    per_row = 12
    per_col = 2

    

    tk.Label(ventana, text = "Perturbacion", font = "Verdana 10 bold").grid(row = per_row, column = 2)

    check_box = tk.Checkbutton(ventana, text ="Activar",variable = perturbacionHab, onvalue = 1, offvalue = 0)
    check_box.grid(row = per_row + 1, column = 1)

    etiqueta_magnitud_escalon = tk.Label(ventana, text = "Magnitud").grid(row = per_row + 2, column = per_col - 2)
    magnitud_escalon_per.grid(row = per_row + 2, column = per_col - 1)

def final_buttons():

    tk.Label(ventana, text = "Ejecutar", font = "Verdana 10 bold").grid(row = 17, column = 3)

    tk.Button(ventana, text = "Enter", command = lambda: enter(tipoDePlanta, tipoDeEntrada, perturbacionHab)).grid(row = 18, column = 3)
    tk.Button(ventana, text = "Reset", command = reset).grid(row = 18, column = 4)


ventana = tk.Tk()
ventana.geometry("1000x1000")

tipoDePlanta = tk.IntVar()
tipoDeEntrada = tk.IntVar()
perturbacionHab = tk.IntVar()

gain = tk.Entry(ventana)
tao = tk.Entry(ventana)
tiempomuerto = tk.Entry(ventana)
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


figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, ventana)
chart_type.get_tk_widget().grid(row = 19, column = 6)

ventana.mainloop()