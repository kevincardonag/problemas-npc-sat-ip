import os
import time


def get_files():
    DIR = "./instanciasSAT/"
    names_files = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and name != '__init__.py']
    return names_files


def convert_sat_to_ip():
    try:
        for nombre_archivo in get_files():
            name_file = nombre_archivo.split('.')

            result_file = ''.join(name_file[:-1])

            with open("./instanciasSAT/" + nombre_archivo, "r") as archivo, open("./instanciasMiniZinc/" + result_file + ".mzn", "w") as archivo_escrito:
                for linea in map(lambda x: x.strip(), archivo.readlines()):
                    if linea:
                    	
                        if linea[0] == 'p':
                            list_problem = linea.split()
                            num_variables = int(list_problem[2])

                            archivo_escrito.write("array[1.. " + str(num_variables) + "] of var 0..1: x;" + "\n")
                            archivo_escrito.write("array[1.. " + str(num_variables) + "] of var 0..1: n_x;" + "\n")
                            archivo_escrito.write("constraint forall(i in 1.." + str(num_variables) + ")(x[i] + n_x[i] = 1);" + "\n")

                        if linea[0] != 'c' and linea[0] != 'p':
                            lista_vars = linea.split()
                            restriccion = "constraint "
                            for i in range(len(lista_vars)-1):
                                valor_clausula = int(lista_vars[i])
                                if valor_clausula < 0:
                                    valor_real = str(abs(valor_clausula))
                                    restriccion += "n_x[" + valor_real + "] + "
                                else:
                                    restriccion += "x[" + str(valor_clausula) + "] + "

                            restriccion = restriccion[0:len(restriccion)-3]
                            restriccion += " >= 1;\n"
                            archivo_escrito.write(restriccion)

                archivo_escrito.write("solve satisfy;")

    except Exception as error:
        print(error)


start_time = time.time()
convert_sat_to_ip()
duration = time.time() - start_time
print("Tiempo en segundos: " , duration)
