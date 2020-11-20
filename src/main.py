import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import time

from systems import primer_orden, ARX_filter
from utils import read_input_from_file

MAX_SECONDS_SIMULATION = 1000


def main():
    '''
    main function
    '''
    # TODO: Main menu

    print('Proyecto 1 Control Computarizado Fito Cuan Paul Vazquez A00819877')
    seconds = 0
    disturbance = 0
    time_to_plot = MAX_SECONDS_SIMULATION
    input_to_the_system = 10
    #b_values = [1, 1, 1, 1, 1, 1, 1]
    #entrada_test = b_values
    #primer_orden(0.5, 4, 2, 1, escalon)
    #ARX_filter(4, [2, 3, 4, 5], b_values, 0, 0, entrada_test)
    plt.axis([0, 60, 0, 100])
    x = []
    y_plot = []

    if(isinstance(input_to_the_system, list)):
        time_to_plot = len(input_to_the_system)

    while(seconds < time_to_plot):
        x.append(seconds)
        y = primer_orden(0.5, 3.34, 1, seconds, 1.46, input_to_the_system,0)
        y_plot.append(y[0])
        print("Value of primer orden at " + str(seconds) + " is " + str(y))
       
        plt.scatter(x, y_plot)
        plt.pause(0.5)
        seconds += 1
    plt.show()


if __name__ == "__main__":
    main()
