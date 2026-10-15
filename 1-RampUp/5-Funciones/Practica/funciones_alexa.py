import math # Aseguramos la importación requerida por la función area_circulo

def que_dia_es(arg):
    """
    Convierte un número entero del 1 al 7 en su día de la semana correspondiente.
    """
    match arg:
        case 1:
            task = "Lunes"
        case 2:
            task = "Martes"
        case 3:
            task = "Miércoles"
        case 4:
            task = "Jueves"
        case 5:
            task = "Viernes"
        case 6:
            task = "Sábado"
        case 7:
            task = "Domingo"
        case _:
            # Caso por defecto si el número no está entre 1 y 7
            task = "no es un día válido"
    return task

def piramide_invertida(num):
    """
    Imprime en consola una estructura de pirámide invertida de números alineados,
    comenzando desde el número recibido hasta el 1 en filas decrecientes.
    """
    # Bucle externo: controla las filas de forma descendente (ej. de 5 a 1)
    for n1 in range(num, 0, -1):
        # Bucle interno: imprime los números de la fila actual de mayor a menor
        for n2 in range(n1, 0, -1):
            print(n2, end = " ")
        print() # Salto de línea al terminar cada fila

def comparacion_dos_num(num1, num2):
    """
    Compara dos números y devuelve una cadena de texto indicando su relación de orden.
    """
    if num1 == num2:
        return "son iguales"
    if num1 > num2:
        return "el primero es mayor que el segundo"
    else:
        return "el segundo es mayor que el primero"

def contador_letra(texto, letra):
    """
    Cuenta cuántas veces aparece una letra específica dentro de un texto,
    sin distinguir entre mayúsculas y minúsculas.
    """
    texto = texto.lower() # Normaliza el texto a minúsculas
    letra = letra.lower() # Normaliza la letra objetivo a minúsculas
    return int(texto.count(letra))

def conteo_letras_dic(string):
    """
    Genera un diccionario que contiene la frecuencia de aparición de cada carácter 
    presente en la cadena de texto proporcionada.
    """
    dic = {}
    # Itera por cada carácter convertido a minúsculas
    for c in string.lower():
        dic[c] = string.count(c)
        
    return dic

def modif_lista(lista, comando, elemento = None):
    """
    Modifica una lista agregando o eliminando un elemento según el comando indicado,
    o la devuelve intacta si las condiciones no se cumplen.
    """
    if comando == "add" and elemento:
        lista.append(elemento) # Añade el elemento al final de la lista
        return lista
    elif comando == "remove" and elemento:
        lista.remove(elemento) # Elimina la primera ocurrencia del elemento
        return lista
    else:
        return lista # Retorna la lista original si no hay cambios

def crea_tu_frase(*args):
    """
    Concatena una cantidad indeterminada de argumentos de texto (cadenas) 
    separándolos por un espacio en blanco.
    """
    return " ".join(args)

def fibonacci(n):
    """
    Calcula de forma recursiva el n-ésimo número de la sucesión de Fibonacci.
    """
    if n <= 1:
        return n # Casos base: f(0) = 0, f(1) = 1
    else:
        # Caso recursivo: suma de los dos términos anteriores
        return (fibonacci(n-1) + fibonacci(n-2))

def area_cuadrado(lado):
    """
    Calcula la superficie de un cuadrado elevando la longitud de su lado al cuadrado.
    """
    return lado**2

def area_triangulo(base, altura):
    """
    Calcula el área de un triángulo aplicando la fórmula estándar: (base * altura) / 2.
    """
    return (base * altura) / 2

def area_circulo(radio):
    """
    Calcula el área de un círculo utilizando el radio provisto y la constante matemática pi.
    """
    return math.pi * (radio **2)
