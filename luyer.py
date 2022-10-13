from lark import Visitor
from errors import *

# Directorio de funciones
directorio_funciones = {}


class Luyer(Visitor):
    def __init__(self):
        #Variable para guardar el scope actual
        self.scope = ""
    # Semántica para funciones
    def funcion(self, tree):
        #Obtener el tipo de la función
        tipo = str(tree.children[0].children[0])
        #Obtener el id de la función
        id_funcion = str(tree.children[1])
        self.scope = id_funcion
        #Checar si la función ya existe
        if id_funcion in directorio_funciones:
            raise functionNameError("Function already exists")

        #Meter funcion en directorio
        directorio_funciones[id_funcion] = {'tipo' : tipo, 'nombre' : id_funcion, 'tabla_vars': {}}

    # Semántica para parámetros de funciones
    def func_vars(self, tree):
        #Obtener el tipo
        tipo = str(tree.children[0].children[0].children[0])
        #Obtener el nombre
        id_parametro = str(tree.children[1])
        #Crear parametro
        parametro = {'nombre' : id_parametro, 'tipo' : tipo}
        # Insertar en tabla de variables correspondiente a su scope
        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        tabla_vars[id_parametro] = parametro
