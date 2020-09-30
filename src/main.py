import matplotlib.pyplot as plt
import numpy as np

from systems import primer_orden, ARX_filter
from utils import read_input_from_file

def main():
    '''
    main function
    '''
    print('Proyecto 1 Control Computarizado Paul Vazquez A00819877')
    escalon = [10 for i in range(0, 6)]
    b_values = [1, 1, 1, 1, 1, 1, 1]
    entrada_test = b_values
    primer_orden(0.5, 4, 2, 1, escalon)
    ARX_filter(4, [2, 3, 4, 5], b_values, 0, 0, entrada_test)


if __name__ == "__main__":
    main()
