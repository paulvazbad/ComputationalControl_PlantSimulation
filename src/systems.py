'''This module has the auxiliary functions to
calculate ARX filter systems and first order systems '''
import math

# AUX for memoization
memoization_ARX = [-1 for i in range(0, 1000)]

last_y = 0


def calculate_a1_b1_b2_N(T, tau, gain, theta_prima):
    '''
    T : periodo
    tau: tau del sistema
    k: ganancia del sistema,
    theta_prima: retraso del sistema
    '''
    N = int(theta_prima / T)
    theta = theta_prima - N*T
    m = 1 - (theta/T)
    a1 = math.exp((-T/tau))
    b1 = gain * (1 - a1)
    b2 = gain * (math.exp(-(m*T)/tau) - a1)
    print(str(a1) + " y( k - 1)" + " + " + str(b1) +
          "m(k-1-N) + " + str(b2) + "m(k-2-N)" + "donde N es " + str(N))
    return (a1, b1, b2, N)


def calculate_input_to_the_system(k, input_to_the_system):
    # TODO: Check with professor if before 0 we assume 0, consider theta_prima
    if(k < 0):
        return 0
    try:
        if(isinstance(input_to_the_system, list)):
            if(k >= len(input_to_the_system)):
                return input_to_the_system[-1]
            return input_to_the_system[int(k)]
        else:
            return input_to_the_system
    except Exception as identifier:
        print("fallo el calculo del input con i " + str(k) + identifier)


def calculate_y_k_alternative(k, a1, b1, b2, N, input_to_the_system):
    global last_y
    if(k < 0):
        return 0

    # TODO: Test b2
    last_y = a1 * last_y + b1 * calculate_input_to_the_system(
        k - 1 - N, input_to_the_system) + b2 * calculate_input_to_the_system(k - 2 - N, input_to_the_system)

    return last_y


def primer_orden(T, tau, gain, k, theta_prima, input_to_the_system):
    '''
    T : periodo
    tau: tau del sistema
    Gain: ganancia del sistema,
    muestra : muestra del sistema
    theta_prima: retraso del sistema
    input: Entrada al 
    '''
    print("Funcion de primer orden")
    a1, b1, b2, N = calculate_a1_b1_b2_N(T, tau, gain, theta_prima)
    return calculate_y_k_alternative(k, a1, b1, b2, N, input_to_the_system), calculate_input_to_the_system(
        k, input_to_the_system)


def calculate_c_ARX(number_of_coefficients, a_values, b_values, delay, k, input_to_the_system):
    if(k < 0):
        return 0
    if(memoization_ARX[k] != -1):
        return memoization_ARX[k]

    value_at_k = 0
    for i in range(0, number_of_coefficients):
        value_at_k += a_values[i]*calculate_c_ARX(
            number_of_coefficients, a_values, b_values, delay, k - i - 1, input_to_the_system)
        if(i == 1):
            print("Estoy con el coefficiente 1")
        value_at_k += b_values[i] * \
            calculate_input_to_the_system(k - delay - i, input_to_the_system)
    memoization_ARX[k] = value_at_k
    return value_at_k


def ARX_filter(number_of_coefficients, a_values, b_values, delay, k, input_to_the_system):
    '''
    number_of_coefficients: cantidad de a's y b's en la ecuacion de diferencias
    a_values: coeficientes de a
    b_values: coeficientes de b
    delay: retraso en la funcion (N en intervalos de muestreo NO EN SEGUNDOS)
    k: valor de k a plottear (ese y todos los anteriores porque es recursivo)
    input_to_the_system: valores de entrada al sistema (tienen que ser >=k)

    '''
    if(k < 0):
        print("Invalid value of k")
    print(calculate_c_ARX(number_of_coefficients, a_values,
                          b_values, delay, k, input_to_the_system))


def reset_systems():
    global last_y
    global memoization_ARX
    last_y = 0
    memoization_ARX = [-1 for i in range(0, 1000)]

if(__name__ == "__main__"):
    # a1, a2, a3....
    a = [0.8825,0]
    # b0, b1, b2....
    b = [0, 0.235]

    ## NUMBER OF A'S MUST BE EQUAL TO NUMBER OF B'S
    delay = 2
    k = 15
    input_to_the_system = [10, 10, 10,10]
    
    for i in range(0,6):
        print('k: ' + str(i))
        ARX_filter(2,a,b,delay,i,input_to_the_system)
        