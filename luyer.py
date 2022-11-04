import collections
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
pSaltos = collections.deque()


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

    def globals(self, tree):
        #Para guardar globales solo cambiamos el scope e iniciamos su parte en el directorio
        self.scope = 'global'
        directorio_funciones[self.scope] = {'tipo' : 'main', 'nombre' : 'main', 'tabla_vars': {}}

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

        #Si la asignación se realiza en la declaración, hay que meter el tipo y nombre en las pilas
        if tree.children[0].children[2].children and tree.children[0].children[2].children[0].data.value == 'asg_sign':
            pilaO.append(nombre)
            pTipos.append(tipo)

        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        #checar doble declaración
        if nombre in tabla_vars:
            raise duplicateVariableError(f"Variable {nombre} is alredady defined.")
        tabla_vars[nombre] = variable
    
    #Funciones para meter operadores a pOper
    def push_mul(self, tree):
        pOper.append('*')

    def push_div(self, tree):
        pOper.append('/')
    
    def push_sum(self, tree):
        pOper.append('+')

    def push_res(self, tree):
        pOper.append('-')

    def push_gt(self, tree):
        pOper.append('<')

    def push_lt(self, tree):
        pOper.append('>')
    
    def push_get(self, tree):
        pOper.append('<=')

    def push_let(self, tree):
        pOper.append('>=')

    def push_eq(self, tree):
        pOper.append('==')

    def push_ne(self, tree):
        pOper.append('!=')

    def push_and(self, tree):
        pOper.append('&&')

    def push_or(self, tree):
        pOper.append('||')
    
    def push_asg(self, tree):
        pOper.append('=')


    #Funciones para meter valores a pilaO y pTipos
    def id(self, tree):
        name = str(tree.children[0].value)

        #checar si la variable está declarada
        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        if name in tabla_vars:
            if 'valor' in tabla_vars[name]:
                pilaO.append(tabla_vars[name]['valor'])
                pTipos.append(tabla_vars[name]['tipo'])
            else:
                raise variableNoValue(f"Variable {name} has no value")
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
        value = value.replace('"', '')
        pTipos.append('string')
        pilaO.append(value)
    
    def true(self, tree):
        pTipos.append('bool')
        pilaO.append(True)
    
    def false(self, tree):
        pTipos.append('bool')
        pilaO.append(False)

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
                # Si el resultado de una división es entera, entonces hay que manejarlo como entero
                if tipoRes == 'float' and pOper[-1] == '/' and res.is_integer():
                    tipoRes = 'int'
                    res = int(res)
                #Generar Cuádruplo
                oper = pOper.pop()
                cuadruplos.append(Quad(oper, op1, op2, res))
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
                cuadruplos.append(Quad(oper, op1, op2, res))
                pilaO.append(res)
                pTipos.append(tipoRes)

    def evaluacion3(self, tree):
        #Tercera evaluación, para comparaciones
        comp = ['<', '>', "==", "!=", "<=", ">="]
        if pOper:
            if pOper[-1] in comp:
                op2 = pilaO.pop()
                op1 = pilaO.pop()
                tipoOp2 = pTipos.pop()
                tipoOp1 = pTipos.pop()
                #checar en cubo semántico
                tipoRes = cubo[pOper[-1]][tipoOp1][tipoOp2]
                if tipoRes == 'ERROR':
                    raise TypeError(f"Invalid operation between {tipoOp1} and {tipoOp2}")
                
                oper = pOper.pop()
                if oper == '<':
                    res = op1 < op2
                elif oper == '>':
                    res = op1 > op2
                elif oper == '==':
                    res = op1 == op2
                elif oper == '>=':
                    res = op1 >= op2
                elif oper == '<=':
                    res = op1 <= op2
                elif oper == '!=':
                    res = op1 != op2
                cuadruplos.append(Quad(oper, op1, op2, res))
                pilaO.append(res)
                pTipos.append(tipoRes)

    def evaluacion4(self, tree):
        #Segunda evaluación, checamos si hay sumas o restas pendientes
        if pOper:
            if pOper[-1] == '&&' or pOper[-1] == '||':
                op2 = pilaO.pop()
                op1 = pilaO.pop()
                tipoOp2 = pTipos.pop()
                tipoOp1 = pTipos.pop()
                #checar en cubo semántico
                tipoRes = cubo[pOper[-1]][tipoOp1][tipoOp2]
                if tipoRes == 'ERROR':
                    raise TypeError(f"Invalid operation between {tipoOp1} and {tipoOp2}")
                res = op1 and op2 if pOper[-1] == '&&' else op1 or op2
                oper = pOper.pop()
                cuadruplos.append(Quad(oper, op1, op2, res))
                pilaO.append(res)
                pTipos.append(tipoRes)

    def push_par(self, tree):
        #Meter fondo falso
        pOper.append('(')
    
    def pop_par(self, tree):
        #Sacar fondo falso
        pOper.pop()

    def assign_val(self, tree):
        if pOper:
            if pOper[-1] == '=':
                op2 = pilaO.pop()
                op1 = pilaO.pop()
                tipoOp2 = pTipos.pop()
                tipoOp1 = pTipos.pop()
                #checar en cubo semántico
                tipoRes = cubo[pOper[-1]][tipoOp1][tipoOp2]
                if tipoRes == 'ERROR':
                    raise TypeError(f"Invalid operation between {tipoOp1} and {tipoOp2}")

                cuadruplos.append(Quad(pOper[-1], op2, None, op1))
                pOper.pop()
                #Asignar valor
                directorio_funciones[self.scope]['tabla_vars'][op1]['valor'] = op2

    def asignacion(self, tree):
        #Buscar variable en directorio
        name = tree.children[0]
        #Si no se encuentra en directorio, error
        if name not in directorio_funciones[self.scope]['tabla_vars']:
            raise variableNotFoundError(f"Variable {name} is not defined.")
        tipo = directorio_funciones[self.scope]['tabla_vars'][name]['tipo']
        #Push nombre y tipo para futura asignación
        pTipos.append(tipo)
        pilaO.append(name)

    def check_if(self, tree):
        #Punto neurálgico para meter gotoF del if
        eval = pilaO.pop()
        pTipos.pop()
        #Generar Cuádruplo
        cuadruplos.append(Quad("gotoF", bool(eval), None, "---"))
        pSaltos.append(len(cuadruplos) - 1)

    def push_else(self, tree):
        #Punto neurálgico para else, metemos goto y llenamos gotoF del if
        cuadruplos.append(Quad("goto", None, None, "---"))
        if_falso = pSaltos.pop()
        pSaltos.append(len(cuadruplos) - 1)
        cuadruplos[if_falso].res = len(cuadruplos) + 1

    def end_if(self, tree):
        #Punto neurálgico para el final del if, sacamos de la pila de saltos y rellenamos
        end = pSaltos.pop()
        cuadruplos[end].res = len(cuadruplos) + 1

    def push_while(self, tree):
        #Punto neurálgico para el inicio del while, metemos cont a la pila de saltos
        pSaltos.append(len(cuadruplos) + 1)

    def check_while(self, tree):
        #Punto neurálgico para evaluar la expresión del while
        eval = pilaO.pop()
        pTipos.pop()
        #Generar Cuádruplo
        cuadruplos.append(Quad("gotoF", bool(eval), None, "---"))
        pSaltos.append(len(cuadruplos) - 1)

    def end_while(self, tree):
        #Punto neurálgico para el final del while, rellenamos check_while y generamos goto al inicio
        end = pSaltos.pop()
        ret = pSaltos.pop()
        cuadruplos.append(Quad("goto", None, None, ret))
        cuadruplos[end].res = len(cuadruplos) + 1

