import math


memoization_y_k_primer_orden = [-1 for i in range(0,1000)]
memoization_ARX = [-1 for i in range(0,1000)]
def calculate_a1_b1_N(T,tau,k, theta_prima):
    '''
    T : periodo
    tau: tau del sistema
    k: ganancia del sistema,
    theta_prima: retraso del sistema
    '''
    N = theta_prima / T
    a1 = math.exp((-T/tau))
    b1 = k * (1 - a1)
    print(str(a1) + " y( k - 1)" + " + " + str(b1) + "m(k-1-N)" + "donde N es " + str(N))
    return (a1,b1, N)

def calculate_input_to_the_system(k, input_to_the_system):
    # TODO: remove this function and just fill with zeroes in input to the system based on N
    if(k < 0):
        return 0
    try:
        return input_to_the_system[int(k)]
    except Exception as identifier:
        print("fallo el calculo del input con i " + str(k))
    

def calculate_y_k(k,a1,b1,N, input_to_the_system):
    #TODO: Agregar memoization 
    if(k<0):
        return 0
    memoization_y_k_primer_orden[k] = a1 * calculate_y_k(k -1,a1,b1,N,input_to_the_system) + b1 * calculate_input_to_the_system(k -1 -N, input_to_the_system)
    return memoization_y_k_primer_orden[k] 

def primer_orden(T,tau,k, theta_prima, input_to_the_system):
    '''
    T : periodo
    tau: tau del sistema
    k: ganancia del sistema,
    theta_prima: retraso del sistema
    input: Entrada al 
    '''
    a1,b1,N = calculate_a1_b1_N(0.5,4,2,1)
    print("Funcion de primer orden")
    for i in range (0,6):
        print("y({i})")
        print(calculate_y_k(i,a1,b1,N, input_to_the_system))


def calculate_c_ARX(number_of_coefficients, a_values, b_values, delay, k, input_to_the_system):
    #TODO: Agregar memoization 
    if(k <0):
        return 0
    if(memoization_ARX[k]!= -1):
        return memoization_ARX[k]

    value_at_k = 0
    for i in range (1,number_of_coefficients+1):
       value_at_k+=a_values[i - 1]*calculate_c_ARX(number_of_coefficients, a_values, b_values, delay, k - i, input_to_the_system)  
       value_at_k+=b_values[i - 1]*calculate_input_to_the_system(k - delay - i, input_to_the_system)
    
    return value_at_k

def ARX_filter(number_of_coefficients, a_values, b_values, delay,k,input_to_the_system):
    '''
    number_of_coefficients: cantidad de a's y b's en la ecuacion de diferencias
    a_values: coeficientes de a
    b_values: coeficientes de b
    delay: retraso en la funcion
    k: valor de k a plottear (ese y todos los anteriores porque es recursivo)
    input_to_the_system: valores de entrada al sistema (tienen que ser >=k)

    '''
    print("Filtro ARX")
    for i in range (1,k+1):
        print("y({i})")
        print(calculate_c_ARX(number_of_coefficients,a_values,b_values,delay,i,input_to_the_system))

def main():
    print('Proyecto 1 Control Computarizado Paul Vazquez A00819877')
    escalon = [10 for i in range (0,6)]
    b_values = [1,1,1,1,1,1,1]
    entrada_test = b_values
    primer_orden(0.5,4,2,1,escalon)
    ARX_filter(4,[2,3,4,5],b_values,0,3,entrada_test)    

if __name__ == "__main__":
    main()