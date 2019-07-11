import os
from io import open
from os import scandir, getcwd


def ls(ruta = getcwd()):
    lstFiles = []
    lstDir = os.walk(ruta)
    for root, dirs, files in lstDir:
        for fichero in files:
            nombreFichero, extension = os.path.splitext(fichero)
            if extension == ".cnf":
                lstFiles.append(nombreFichero)
    return lstFiles


try:

    for nombre_archivo in ls('./instanciasSAT/'):
        archivo = open("./instanciasSAT/" + nombre_archivo + ".cnf", "r")
        archivo_escrito = open("./instanciasMiniZinc/" + nombre_archivo + ".mzn", "w")
        for linea in map(lambda x: x.strip(), archivo.readlines()):
            if len(linea) > 0:
                if linea[0] == 'p':
                    list_problem = linea.split()
                    num_variables = int(list_problem[2])
                    for data in range(num_variables*2):
                        if data >= num_variables:
                            archivo_escrito.write("var 0..1: n_x_" + str(data-(num_variables-1))+";\n")
                        else:
                            archivo_escrito.write("var 0..1: x_" + str(data+1)+";\n")

                    for data in range(num_variables):
                        archivo_escrito.write("constraint x_" + str(data+1) + " + n_x_" + str(data+1) + " = 1;\n")

                if linea[0] != 'c' and linea[0] != 'p':
                    lista_vars = linea.split()
                    longitud_clausula = len(lista_vars)-1
                    restriccion = "constraint "
                    for i in range(len(lista_vars)-1):
                        valor_clausula = int(lista_vars[i])
                        if valor_clausula < 0:
                            valor_real = str(abs(valor_clausula))
                            restriccion += "n_x_" + valor_real + " + "
                        else:
                            restriccion += "x_" + str(valor_clausula) + " + "
                    restriccion = restriccion[0:len(restriccion)-3]
                    restriccion += " >= 1;\n"
                    archivo_escrito.write(restriccion)

        archivo_escrito.write("solve satisfy;")
        archivo_escrito.close()
        archivo.close()

except Exception as error:
   print(error)



