import tkinter as tk
from tkinter import filedialog
import csv


import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from systems import primer_orden, ARX_filter, reset_systems, calculate_criterios, calculate_salida_del_pid

seconds = 0

input_to_the_system = 0
perturbacion_de_entrada_value = 0
perturbacion_interna_value = 0
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

start_graphing = False
plant_type_flag = 0

# PID variables
reference = 0
error = 0
mk = 0
salida_del_pid = 0
manualAutomatico_value = False

a_pid_list = []
b_pid_list = []
kc_value = 0
kd_value = 0
ki_value  = 0

content = []


def enter(tipoDePlanta, tipoDeEntrada, perturbacionHab, perturbacionInterna):
    global input_to_the_system
    global perturbacion_de_entrada_value
    global perturbacion_interna_value
    global tau_value
    global T_value
    global gain_value
    global theta_prima_value
    global a_list
    global b_list
    global d_value
    global number_of_coefficients
    global start_graphing
    global plant_type_flag
    global manualAutomatico_value

    global a_pid_list
    global b_pid_list
    global kc_value
    global kd_value
    global ki_value

    global content

    start_graphing = True
    plant_type_flag = tipoDePlanta.get()

    print("Entrada")
    if tipoDeEntrada.get() == 0:
        print(magnitud_escalon.get())
        input_to_the_system = 0
        if(magnitud_escalon.get().isnumeric()):
            input_to_the_system = float(magnitud_escalon.get())

    elif tipoDeEntrada.get() == 1:
        input_to_the_system = content

    print("Perturbacion de entrada")
    if len(magnitud_escalon_per.get()) == 0:
        print("No hay Perturbacion")
        perturbacion_de_entrada_value = 0
    else:
        print(magnitud_escalon_per.get())
        perturbacion_de_entrada_value = float(magnitud_escalon_per.get())

    print("Perturbacion interna")
    if len(magnitud_escalon_per_interna.get()) == 0:
        print("No hay Perturbacion")
        perturbacion_interna_value = 0
    else:
        print(magnitud_escalon_per_interna.get())
        perturbacion_interna_value = float(magnitud_escalon_per_interna.get())

    

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

        number_of_coefficients = int(coe.get())
        a_list = [float(x) for x in a.get().split(",")]
        b_list = [float(x) for x in b.get().split(",")]
        d_value = int(d.get())

    manualAutomatico_value = manualAutomatico.get()

    if not manualAutomatico_value:
        if tipoDePID.get() == 0:
            print(var_kc.get(), var_kd.get(), var_ki.get())

            kc_value = float(var_kc.get())
            kd_value = float(var_kd.get())
            ki_value = float(var_ki.get())
        else:
            print(a_pid.get(), b_pid.get())

            a_pid_list = [float(x) for x in a_pid.get().split(",")]
            b_pid_list = [float(x) for x in b_pid.get().split(",")]

def reset():
    global x
    global y
    global y_input
    global seconds
    global start_graphing
    global error

    start_graphing = False
    x = []
    y = []
    y_input = []
    error = 0
    seconds = 0

    axes_out[0].clear()
    axes_out[1].clear()
    axes_out[0].set_title("Output")
    axes_out[1].set_title("Input")
    axes_out[0].set_ylim([0, 60])
    axes_out[1].set_ylim([0, 60])
    
    """
    ax.clear()
    ax_input.clear()
    ax.set_title("Output")
    ax_input.set_title("Input")
    ax.set_ylim([0, 60])
    ax_input.set_ylim([0, 60])

    """

    reset_systems()


def planta():
    tk.Label(ventana, text="Simulador computacional de Plantas",
             font="Verdana 10 bold").grid(row=0, column=2)

    tk.Label(ventana, text="Planta",
             font="Verdana 10 bold", bg = "white").grid(row=1, column=0, columnspan = 5, sticky='ew')

    row_c = 4
    col_c = 0

    etiqueta_gain = tk.Label(ventana, text="Gain: ").grid(
        row=row_c, column=col_c, sticky = 'e')
    etiqueta_tao = tk.Label(ventana, text="Tau: ").grid(
        row=row_c + 1, column=col_c, sticky = 'e')
    etiqueta_periodo = tk.Label(ventana, text="Periodo: ").grid(
        row=row_c + 2, column=col_c, sticky = 'e')
    etiqueta_thetaprima = tk.Label(
        ventana, text="Theta Prima: ").grid(row=row_c+3, column=col_c, sticky = 'e')

    row_c = 4
    col_c = 2

    etiqueta_coe = tk.Label(ventana, text="Numero de coeficientes: ").grid(
        row=row_c, column=col_c, sticky = 'e')
    etiqueta_a = tk.Label(ventana, text="a's: ").grid(
        row=row_c + 1, column=col_c, sticky = 'e')
    etiqueta_b = tk.Label(ventana, text="b's: ").grid(
        row=row_c + 2, column=col_c, sticky = 'e')
    etiqueta_d = tk.Label(ventana, text="d's: ").grid(
        row=row_c + 3, column=col_c, sticky = 'e')

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
    global content

    file = filedialog.askopenfile(
        parent=ventana, mode='rb', title='Choose a file')

    if file is not None:
        content = file.read()
        content = content.decode("utf-8")
        content = content.splitlines()
        content = [float(i) for i in content]

        return

    print("no se pudo acceder al archivo")


def entrada():
    entrada_row = 9
    entrada_col = 2

    tk.Label(ventana, text="Entrada", font="Verdana 10 bold", bg = "white").grid(
        row=entrada_row, column=0, columnspan = 5, sticky='ew')

    tk.Radiobutton(ventana, text="Escalon", variable=tipoDeEntrada,
                   value=0).grid(row=entrada_row+1, column=1)
    tk.Radiobutton(ventana, text="Archivo", variable=tipoDeEntrada,
                   value=1).grid(row=entrada_row+1, column=2)

    etiqueta_magnitud_escalon = tk.Label(ventana, text="Magnitud: ").grid(
        row=entrada_row + 2, column=entrada_col - 2, sticky = 'e')
    magnitud_escalon.grid(row=entrada_row + 2, column=entrada_col - 1)

    tk.Button(ventana, text="Buscar", command=buscar_archivo).grid(
        row=entrada_row + 2, column=1 + 1)


def perturbacion_de_entrada():
    per_row = 12
    per_col = 2

    tk.Label(ventana, text="Perturbacion de Entrada",
             font="Verdana 10 bold", bg = "white").grid(row=per_row, column=0, columnspan = 5, sticky='ew')

    etiqueta_magnitud_escalon = tk.Label(ventana, text="Magnitud: ").grid(
        row=per_row + 1, column=per_col - 2, sticky = 'e')
    magnitud_escalon_per.grid(row=per_row + 1, column=per_col - 1)


def perturbacion_interna():
    per_row = 15
    per_col = 2

    tk.Label(ventana, text="Perturbacion Interna",
             font="Verdana 10 bold", bg = "white").grid(row=per_row, column=0, columnspan = 5, sticky='ew')

    etiqueta_magnitud_perturbacion_interna = tk.Label(ventana, text="Magnitud: ").grid(
        row=per_row + 1, column=per_col - 2 , sticky = 'e')

    magnitud_escalon_per_interna.grid(row=per_row + 1, column=per_col - 1)


def constantes():

    per_row = 17
    per_col = 2

    tk.Label(ventana, text="Controlador PID",
             font="Verdana 10 bold", bg = "white").grid(row=17, column=0, columnspan = 5, sticky='ew')


    check_box = tk.Checkbutton(
        ventana, text="Manual/Automatico", variable=manualAutomatico, onvalue=1, offvalue=0)
    check_box.grid(row=0, column=0)

    per_row += 1

    choices = {'Ref_IAE', 'Ref_ISE', 'Ref_ITAE',
               'Per_IAE', 'Per_ISE', 'Per_ITAE'}

    popupMenu = tk.OptionMenu(ventana, tipoMetodo, *choices)

    popupMenu.grid(row=per_row + 3, column=per_col - 1)

    etiqueta_constantesPID = tk.Label(ventana, text="Criterio de Sintonía").grid(
        row=per_row + 3, column=per_col - 2)

    tk.Label(ventana, text="Kc: ").grid(row=per_row + 4, column=per_col - 2, sticky = 'e')
    tk.Label(ventana, text="Kd: ").grid(row=per_row + 5, column=per_col - 2, sticky = 'e')
    tk.Label(ventana, text="Ki: ").grid(row=per_row + 6, column=per_col - 2, sticky = 'e')

    kc_tb = tk.Entry(ventana, text=var_kc)
    ki_tb = tk.Entry(ventana, text=var_kd)
    kd_tb = tk.Entry(ventana, text=var_ki)

    kc_tb.grid(row=per_row + 4, column=per_col - 1)
    ki_tb.grid(row=per_row + 5, column=per_col - 1)
    kd_tb.grid(row=per_row + 6, column=per_col - 1)

    tk.Radiobutton(ventana, text="Constantes", variable=tipoDePID,
                   value=0).grid(row=per_row, column=1)
    tk.Radiobutton(ventana, text="ARX", variable=tipoDePID,
                   value=1).grid(row=per_row , column=3)


    tk.Button(ventana, text="Calcular Constantes",
              command=cal_cons).grid(row=per_row + 7, column= per_col - 1)

    tk.Label(ventana, text="Referencia: ").grid(
        row=per_row + 4, column=2, sticky = 'e')
    tk.Label(ventana, text="a's: ").grid(
        row=per_row + 5, column=2, sticky = 'e')
    tk.Label(ventana, text="b's: ").grid(
        row=per_row + 6, column=2, sticky = 'e')

    referencia_pid.grid(row=per_row + 4, column=3)
    a_pid.grid(row=per_row + 5, column=3)
    b_pid.grid(row=per_row + 6, column=3)



def cal_cons():
    if not gain.get() or not thetaprima.get() or not tao.get():
        return

    kc, kd, ki = calculate_criterios(str(tipoMetodo.get()), float(
        gain.get()), float(thetaprima.get()), float(tao.get()))

    var_kc.set(kc)
    var_kd.set(kd)
    var_ki.set(ki)


def final_buttons():

    per_row = 26

    tk.Label(ventana, text="Ejecutar",
             font="Verdana 10 bold", bg = "white").grid(row=per_row, column=0, columnspan = 5, sticky='ew')



    tk.Button(ventana, text="Enter", command=lambda: enter(
        tipoDePlanta, tipoDeEntrada, perturbacionHab, perturbacionInterna)).grid(row=per_row+1, column=0)
    tk.Button(ventana, text="Reset", command=reset).grid(row=per_row+1, column=1)
    


ventana = tk.Tk()
ventana.geometry("750x560")

tipoDePlanta = tk.IntVar()
tipoDeEntrada = tk.IntVar()
perturbacionHab = tk.IntVar()
perturbacionInterna = tk.IntVar()
manualAutomatico = tk.IntVar()
tipoDePID = tk.IntVar()

tipoMetodo = tk.StringVar()

var_kc = tk.DoubleVar()
var_kd = tk.DoubleVar()
var_ki = tk.DoubleVar()


gain = tk.Entry(ventana)
tao = tk.Entry(ventana)
periodo = tk.Entry(ventana)
thetaprima = tk.Entry(ventana)
coe = tk.Entry(ventana)
a = tk.Entry(ventana)
b = tk.Entry(ventana)
d = tk.Entry(ventana)


referencia_pid = tk.Entry(ventana)
a_pid = tk.Entry(ventana)
b_pid = tk.Entry(ventana)

magnitud_escalon = tk.Entry(ventana)
magnitud_escalon_per = tk.Entry(ventana)
magnitud_escalon_per_interna = tk.Entry(ventana)


planta()
entrada()
perturbacion_de_entrada()
perturbacion_interna()
constantes()
final_buttons()




"""

figure = plt.Figure(figsize=(5, 4), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, ventana)
chart_type.get_tk_widget().grid(row=25, column=6)


figure_input = plt.Figure(figsize=(5, 4), dpi=100)
ax_input = figure_input.add_subplot(111)
chart_type_input = FigureCanvasTkAgg(figure_input, ventana)
chart_type_input.get_tk_widget().grid(row=25, column=7)

ax.set_title("Output")
ax_input.set_title("Input")
ax.set_ylim([0, 60])
ax_input.set_ylim([0, 60])

"""







# number_of_coefficients, a_values, b_values, delay, k, input_to_the_system
ticks = 0
X_RANGE = 50
y_value = 100
y_input_val = 100
y_input = []

figure_out, axes_out = plt.subplots(nrows=2, ncols=1, figsize=(8, 5))

axes_out[0].set_title("Output")
axes_out[1].set_title("Input")
axes_out[0].set_ylim([0, 60])
axes_out[1].set_ylim([0, 60])


while True:

    ventana.update_idletasks()
    ventana.update()

    """
    ax.axis([seconds - X_RANGE, seconds, 0, 100])
    ax_input.axis([seconds - X_RANGE, seconds, 0, 100])

    ax.plot(x, y, 'r-')
    ax_input.plot(x, y_input, 'r-')
    """

    

    #ax.scatter(seconds, y + perturbacion_de_entrada_value)
    plt.pause(0.05)
    ticks += 0.05

    """
    chart_type.draw()
    chart_type_input.draw()
    """

    if start_graphing:
        
        axes_out[0].axis([seconds - X_RANGE, seconds, 0, 100])
        axes_out[1].axis([seconds - X_RANGE, seconds, 0, 100])

        axes_out[0].plot(x, y, 'r-')
        axes_out[1].plot(x, y_input, 'r-')
        #figure_out.tight_layout()
        
        # Decidir el tipo de input dependiendo si automatico o Manual
        print("Error" + str(error))
        reference = y_value
        if(manualAutomatico_value== 0):
            # Modo manual (by default)
            print("Modo Manual")

            if tipoDeEntrada.get() == 0:
                mk = input_to_the_system + perturbacion_de_entrada_value
            else:
                mk = input_to_the_system[seconds] + perturbacion_de_entrada_value
            
        else:
            # TODO: reference field en el UI
            ventana.title("Simulador: Modo Automatico")
            error = y_value - reference
            print("Error" + str(error))
            print("Modo Automatico")
            salida_del_pid = calculate_salida_del_pid(
                T_value, float(var_kc.get()), float(var_ki.get()), float(var_kd.get()), error)
            mk = salida_del_pid + perturbacion_de_entrada_value
       
        if(ticks >= 0.1):
            if plant_type_flag == 0:
                y_value, y_input_val = primer_orden(T_value, tau_value, gain_value,
                                                    seconds, theta_prima_value, mk, perturbacion_interna_value)
            elif plant_type_flag == 1:
                print(number_of_coefficients, a_list,
                      b_list, d_value, seconds, mk)
                y_value, y_input_val = ARX_filter(
                    number_of_coefficients, a_list, b_list, d_value, seconds, input_to_the_system, perturbacion_interna_value)


            #ax.set_title("Output: {}".format(y_value))
            #ax_input.set_title("Input: {}".format(y_input_val))

            axes_out[0].set_title("Output: {}".format(y_value))
            axes_out[1].set_title("Input: {}".format(y_input_val))

            y.append(y_value)
            y_input.append(y_input_val)
            x.append(seconds)
            if(seconds >= X_RANGE):
                y.pop(0)
                x.pop(0)
                y_input.pop(0)
            seconds += 1
            ticks = 0
           
        # plt.show()
