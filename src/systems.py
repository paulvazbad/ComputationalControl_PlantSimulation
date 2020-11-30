'''This module has the auxiliary functions to
calculate ARX filter systems and first order systems '''
import math

# AUX for memoization
memoization_ARX = [-1 for i in range(0, 8000)]

last_y = 0

# Previous errors 0 = Error(-1), 1 = Error(-2)
previous_errors = [0, 0, 0, 0]
previous_pid_output = 0

previous_arx_controller_outputs = [0, 0, 0, 0]


MAX_LEN_INPUTS = 5
inputs = [0 for i in range(0, MAX_LEN_INPUTS)]

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
    b1 = gain * (1 - math.exp((-m*T)/tau))
    b2 = gain * (math.exp(-(m*T)/tau) - a1)
    print(str(a1) + " y( k - 1)" + " + " + str(b1) +
          "m(k-1-N) + " + str(b2) + "m(k-2-N)" + "donde N es " + str(N))
    return (a1, b1, b2, N)


def calculate_input_to_the_system(k, input_to_the_system):
    global inputs
    global MAX_LEN_INPUTS

    # TODO: Check with professor if before 0 we assume 0, consider theta_prima
    if(k < 0):
        return 0
    try:
        if(isinstance(input_to_the_system, list)):
            if(k >= len(input_to_the_system)):
                return input_to_the_system[-1]
            return input_to_the_system[int(k)]
        else:
            # TODO: input to the system is not hardcoded
            return inputs[k % MAX_LEN_INPUTS]
    except Exception as identifier:
        print("fallo el calculo del input con i " + str(k) + identifier)


def calculate_y_k_alternative(k, a1, b1, b2, N, input_to_the_system, perturbacion_interna_value):
    global last_y
    global MAX_LEN_INPUTS
   
    if(k < 0):
        return 0

    # TODO: Test b2
    print("Voy a usar: ")
    print("b1 " + str(k-1-N)+" " + str(calculate_input_to_the_system(
        k - 1 - N, input_to_the_system)))
    print("b2 " + str(k-2-N)+" " + str(calculate_input_to_the_system(k -
                                                                     2 - N, input_to_the_system)))
    last_y = a1 * last_y + b1 * calculate_input_to_the_system(
        k - 1 - N, input_to_the_system) + b2 * calculate_input_to_the_system(k - 2 - N, input_to_the_system)

    return last_y + perturbacion_interna_value


def primer_orden(T, tau, gain, k, theta_prima, input_to_the_system, perturbacion_interna_value):
    '''
    T : periodo
    tau: tau del sistema
    Gain: ganancia del sistema,
    muestra : muestra del sistema
    theta_prima: retraso del sistema
    input: Entrada al 
    '''
    print("Funcion de primer orden")
    global inputs
    global MAX_LEN_INPUTS
    a1, b1, b2, N = calculate_a1_b1_b2_N(T, tau, gain, theta_prima)
    if(k > 0):
        inputs[(k - 1) %MAX_LEN_INPUTS] = input_to_the_system
    
    return calculate_y_k_alternative(k, a1, b1, b2, N, input_to_the_system, perturbacion_interna_value), input_to_the_system


def calculate_c_ARX(number_of_coefficients, a_values, b_values, delay, k, input_to_the_system, perturbacion_interna_value):
    global MAX_LEN_INPUTS
    if(k < 0):
        return 0
    if(memoization_ARX[k] != -1):
        return memoization_ARX[k]

    value_at_k = 0
    for i in range(0, number_of_coefficients):
        if(k < 0):
            return 0
        value_at_k += a_values[i]*calculate_c_ARX(
            number_of_coefficients, a_values, b_values, delay, k - i - 1, input_to_the_system, perturbacion_interna_value)
        if(i == 1):
            print("Estoy con el coefficiente 1")
        value_at_k += b_values[i] * \
            calculate_input_to_the_system(
                k - delay - i, input_to_the_system)
    memoization_ARX[k] = value_at_k + perturbacion_interna_value
    return value_at_k + perturbacion_interna_value


def ARX_filter(number_of_coefficients, a_values, b_values, delay, k, input_to_the_system, perturbacion_interna_value):
    '''
    number_of_coefficients: cantidad de a's y b's en la ecuacion de diferencias
    a_values: coeficientes de a
    b_values: coeficientes de b
    delay: retraso en la funcion (N en intervalos de muestreo NO EN SEGUNDOS)
    k: valor de k a plottear (ese y todos los anteriores porque es recursivo)
    input_to_the_system: valores de entrada al sistema (tienen que ser >=k)

    '''
    global MAX_LEN_INPUTS
    if(k < 0):
        print("Invalid value of k")

    if(k > 0):
        inputs[(k - 1) %MAX_LEN_INPUTS] = input_to_the_system

    print(calculate_c_ARX(number_of_coefficients, a_values,
                          b_values, delay, k, input_to_the_system, perturbacion_interna_value))

    return calculate_c_ARX(number_of_coefficients, a_values, b_values, delay, k, input_to_the_system, perturbacion_interna_value), input_to_the_system


def calculate_criterios(criterio, k, t0, tao):

    if criterio == 'Ref_IAE':
        kc = (1.086/k)*(t0/tao)**-0.869
        ki = tao/(0.74-0.13*(t0/tao))
        kd = 0.348*tao*(t0/tao)**0.914

    elif criterio == 'Ref_ITAE':
        kc = (0.965/k)*(t0/tao)**-0.855
        ki = tao/(0.796-0.147*(t0/tao))
        kd = 0.308*tao*(t0/tao)**0.9292

    elif criterio == 'Per_IAE':
        kc = (1.435/k)*(t0/tao)**-0.921
        ki = (tao/0.878)*(t0/tao)**0.749
        kd = 0.482*tao*(t0/tao)**1.137

    elif criterio == 'Per_ISE':
        kc = (1.495/k)*(t0/tao)**-0.945
        ki = (tao/1.101)*(t0/tao)**0.771
        kd = 0.560*tao*(t0/tao)**1.006

    elif criterio == 'Per_ITAE':
        kc = (1.357/k)*(t0/tao)**-0.947
        ki = (tao/0.842)*(t0/tao)**0.738
        kd = 0.381*tao*(t0/tao)**0.995

    return kc, ki, kd


def calculate_salida_del_pid(T, kc, ki, kd, error):
    global previous_errors
    global previous_pid_output
    # TODO: Ask how to calculate mk with a digital pid
    if(ki == 0 or T == 0):
        print("Invalid PID!!!!!!!!!!!!!!")
        return 0

    beta_0 = kc * (1.0 + T/ki + kd/T)
    beta_1 = kc * (-1.0 - (2.0*kd/T))
    beta_2 = kc*(kd/T)

    print("B0 " + str(beta_0) + " B1 "+str(beta_1) + " B2 "+str(beta_2))

    new_pid_output = previous_pid_output + beta_0 * error + \
        beta_1 * previous_errors[0] + beta_2 * previous_errors[1]

    # Save previous errors
    previous_errors[1] = previous_errors[0]
    previous_errors[0] = error
    previous_pid_output = new_pid_output
    return new_pid_output


def calculate_salida_arx_controller(alfas, betas, error):
    global previous_errors
    global previous_arx_controller_outputs
    m = previous_arx_controller_outputs
    new_arx_controller_output = 0
    print(alfas)
    print(betas)
    print("Previous controller outputs: ")
    print(m)
    for i in range(0, 4):
        new_arx_controller_output += alfas[i]*m[i]
        new_arx_controller_output += betas[i+1]*previous_errors[i]
        print("calculating i + " + str(i))
    new_arx_controller_output += betas[0]*error

    previous_arx_controller_outputs.insert(0, new_arx_controller_output)
    previous_arx_controller_outputs.pop()
    previous_errors.insert(0, error)
    previous_errors.pop()

    return new_arx_controller_output


def reset_systems():
    global last_y
    global memoization_ARX
    global previous_errors
    global previous_pid_output
    global inputs
    global MAX_LEN_INPUTS
    global previous_arx_controller_outputs
    last_y = 0
    memoization_ARX = [-1 for i in range(0, 8000)]
    previous_errors = [0, 0, 0, 0]
    previous_pid_output = 0
    inputs = [0 for i in range(0, MAX_LEN_INPUTS)]
    previous_arx_controller_outputs = [0, 0, 0, 0]

if(__name__ == "__main__"):

    #kc,ki,kd = calculate_criterios("Per_ITAE", 1, 1, 1)
    # print(kc,ki,kd)
    '''
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
    '''
