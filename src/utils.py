'''
Util functions for the project (read write files)
'''
from systems import *
import matplotlib.pyplot as plt



x = []
y = []

# TODO: Function to read file into array of values
def read_input_from_file(file_name):
    print(f"Extracting values from {file_name}")


def plot_simulation_foh(T,tau,gain,theta_prima,input_to_the_system,disturbance, seconds,ventana):
    #TODO: see if we can use the figura in the window
    plt.ion()
    if(isinstance(input_to_the_system, list)):
        time_to_plot = len(input_to_the_system)
    print("Segundos: (Valor k en el que voy) " + str(seconds))
    y.append(primer_orden(float(T), float(tau), float(gain), int(seconds), float(theta_prima), float(input_to_the_system)) + float(disturbance))
    x.append(len(y) - 1)
    print("Value of primer orden at " + str(seconds) + " is " + str(y))
    plt.plot(x, y, 'r-')
    plt.pause(1)
    plt.show()
    seconds += 1
    ventana.after(1000, plot_simulation_foh(T,tau,gain,theta_prima,input_to_the_system,disturbance, seconds,ventana))
    
    plt.show()