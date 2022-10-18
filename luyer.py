import collections
from os import popen
from lark import Visitor
from errors import *
from quad import *
from cubo import cubo

# Directorio de funciones
directorio_funciones = {}

#Código Intermedio
cuadruplos = []

#Pilas 
pilaO = collections.deque()
pOper = collections.deque()
pTipos = collections.deque()


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

    #Semántica para main
    def main_start(self, tree):
        #Cambiar el scope a main y crear tabla de variables correspondiente
        self.scope = 'main'
        directorio_funciones[self.scope] = {'tipo' : 'main', 'nombre' : 'main', 'tabla_vars': {}}

    #Semántica para variables
    def vars(self, tree):
        if tree.children == []: return
        #Meter variable a tabla de variables
        tipo = str(tree.children[0].children[0].children[0].children[0])
        nombre = str(tree.children[0].children[1])
        variable = {'nombre' : nombre, 'tipo' : tipo}

        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        tabla_vars[nombre] = variable
    

    def push_mul(self, tree):
        pOper.append('*')

    def push_div(self, tree):
        pOper.append('/')
    
    def push_sum(self, tree):
        pOper.append('+')

    def push_res(self, tree):
        pOper.append('-')

    def id(self, tree):
        name = str(tree.children[0].value)

        #checar si la variable está declarada
        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        if name in tabla_vars:
            pilaO.append(name)
        else:
            raise variableNotFoundError(f"Variable {name} is not defined.")

    def flo(self, tree):
        value = float(tree.children[0].value)
        pTipos.append('float')
        pilaO.append(value)

    def integ(self, tree):
        value = int(tree.children[0].value)
        pTipos.append('int')
        pilaO.append(value)

    def string(self, tree):
        value = str(tree.children[0].value)
        pTipos.append('string')
        pilaO.append(value)

    def evaluacion1(self, tree):
        #Primera evaluación, checamos si hay multiplicaciones o divisiones pendientes
        if pOper:
            if pOper[-1] == '*' or pOper[-1] == '/':
                op2 = pilaO.pop()
                op1 = pilaO.pop()
                tipoOp2 = pTipos.pop()
                tipoOp1 = pTipos.pop()
                #checar en cubo semántico
                tipoRes = cubo[pOper[-1]][tipoOp1][tipoOp2]
                if tipoRes == 'ERROR':
                    raise TypeError(f"Invalid operation between {tipoOp1} and {tipoOp2}")
                res = op1 * op2 if pOper[-1] == '*' else op1 / op2
                oper = pOper.pop()
                print(oper, op1, op2, res)
                pilaO.append(res)
                pTipos.append(tipoRes)

    def evaluacion2(self, tree):
        #Segunda evaluación, checamos si hay sumas o restas pendientes
        if pOper:
            if pOper[-1] == '+' or pOper[-1] == '-':
                op2 = pilaO.pop()
                op1 = pilaO.pop()
                tipoOp2 = pTipos.pop()
                tipoOp1 = pTipos.pop()
                #checar en cubo semántico
                tipoRes = cubo[pOper[-1]][tipoOp1][tipoOp2]
                if tipoRes == 'ERROR':
                    raise TypeError(f"Invalid operation between {tipoOp1} and {tipoOp2}")
                res = op1 + op2 if pOper[-1] == '+' else op1 - op2
                oper = pOper.pop()
                print(oper, op1, op2, res)
                pilaO.append(res)
                pTipos.append(tipoRes)
        