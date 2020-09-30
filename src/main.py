import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import time

from systems import primer_orden, ARX_filter
from utils import read_input_from_file

def main():
    '''
    main function
    '''
    #TODO: Main menu 

    print('Proyecto 1 Control Computarizado Paul Vazquez A00819877')
    escalon = [10 for i in range(0, 6)]
    #b_values = [1, 1, 1, 1, 1, 1, 1]
    #entrada_test = b_values
    #primer_orden(0.5, 4, 2, 1, escalon)
    #ARX_filter(4, [2, 3, 4, 5], b_values, 0, 0, entrada_test)

    plt.axis([0, 60, 0, 100])
    seconds = 0
    #TODO: Infinite plot or until last value in input values reached
    while(True):
        # TODO: Add disturbance in plot
        y = primer_orden(0.5, 4, 2, seconds, 1, escalon)
        print("Value of primer orden at " + str(seconds) +" is " + str(y))
        plt.scatter(seconds, y)
        plt.pause(0.5)
        seconds+=1
        escalon.append(10)
    plt.show()

        


if __name__ == "__main__":
    main()
