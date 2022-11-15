import collections
from lark import Visitor
from errors import *
from quad import *
from cubo import cubo
from memoria import Memoria

# Directorio de funciones
directorio_funciones = {}

#Código Intermedio
cuadruplos = []

#Pilas 
pilaO = collections.deque()
pOper = collections.deque()
pTipos = collections.deque()
pSaltos = collections.deque()
pLlamadas = collections.deque() 

#Memoria
memoria = Memoria()

#Constantes
dirConsts = {}


class Luyer(Visitor):
    def __init__(self):
        #Variable para guardar el scope actual
        self.scope = ""
        self.par_count = 0
        self.current_function = ""
        self.void_function = False

    def gotomain(self, tree):
        cuadruplos.append(Quad("goto", None, None, "----"))
        pSaltos.append(len(cuadruplos) - 1)

    # Semántica para funciones
    def funcion(self, tree):
        #Obtener el tipo de la función
        try:
            tipo = str(tree.children[0].children[0].children[0])
        except:
            tipo = "void"
        #Obtener el id de la función
        id_funcion = str(tree.children[1])
        #Checar que el nombre de la función no esté en globales
        if id_funcion in directorio_funciones['global']['tabla_vars']:
            raise functionNameError(f"There is already a variable with name {id_funcion}")
        #Si el tipo no es void, entonces hay que manejar un return con el parche
        if tipo != 'void':
            direccion = memoria.push_global(tipo)
            var_return = {'nombre' : id_funcion, 'tipo': tipo, 'direccion' : direccion}
            directorio_funciones['global']['tabla_vars'][id_funcion] = var_return
        self.scope = id_funcion
        #Obtener punto de inicio de la función
        start_quad = len(cuadruplos) + 1
        #Checar si la función ya existe
        if id_funcion in directorio_funciones:
            #Edge case, función llamada global
            if id_funcion == 'global':
                raise functionNameError("Function can't be named global")
            raise functionNameError("Function already exists")
        #Asignar nombre de función a variable para al final meter el tamaño su memoria
        self.current_function = id_funcion
        #Meter funcion en directorio
        directorio_funciones[id_funcion] = {'tipo' : tipo, 'nombre' : id_funcion, 'tabla_vars': {}, 'inicio' : start_quad, 'params': []}

    # Semántica para parámetros de funciones
    def func_vars(self, tree):
        #Obtener el tipo
        tipo = str(tree.children[0].children[0].children[0])
        #Obtener el nombre
        id_parametro = str(tree.children[1])
        #Obtener la tabla
        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        #Validar parámetro
        if id_parametro in tabla_vars:
            raise duplicateVariableError(f"Parameter {id_parametro} is already defined")
        elif id_parametro in directorio_funciones['global']['tabla_vars']:
            raise duplicateVariableError(f"Parameter {id_parametro} is already defined globally")
        #Apartar memoria local para el parámetro
        direccion = memoria.push_local(tipo)
        #Guardar parametros en su tabla
        directorio_funciones[self.scope]['params'].append({'tipo' : tipo, 'direccion': direccion, 'valor': 'na'})
        #Crear parametro
        parametro = {'nombre' : id_parametro, 'tipo' : tipo, 'direccion' : direccion}
        # Insertar en tabla de variables correspondiente a su scope
        tabla_vars[id_parametro] = parametro

    #Punto para el return
    def end_return(self, tree):
        if directorio_funciones[self.current_function]['tipo'] == 'void':
            raise functionVoidError(f"Function {self.current_function} is void. It can't return anything")
        res = pilaO.pop()
        #Agregar cuadruplo de return
        cuadruplos.append(Quad('return', None, None, res))

    #Final de la función
    def endfunc(self, tree):
        #Agregar tamaño de memoria al directorio
        directorio_funciones[self.current_function]['memoria'] = {
            'local' : len(memoria.memoria_local),
            'temporal' : len(memoria.memoria_temporal)
        }
        cuadruplos.append(Quad("endfunc", None, None, None))
        #Limpiar memoria
        memoria.clear_local()
        memoria.clear_temp()
        self.current_function = None

    #Punto para funciones void en estatutos
    def is_void(self, tree):
        self.void_function = True

    #Semántica para llamadas de funciones
    def llamada(self, tree):
        id_funcion = tree.children[0]
        #Checar que función exista
        if id_funcion not in directorio_funciones:
            raise functionNotFound(f"Function {id_funcion} doesn't exist")
        #Checar si función es void
        if self.void_function and directorio_funciones[id_funcion]['tipo'] != 'void':
            raise functionTypeError(f"Function {id_funcion} is non-void, you must assign it")
        #Meter ERA a cuadruplos
        cuadruplos.append(Quad('era', None, None, id_funcion))
        pLlamadas.append({'id': id_funcion, 'par_cont' : 1})
        self.void_function = False

    #Checar parametros
    def check_par(self, tree):
        current_call = pLlamadas[-1]['id']
        current_par = pLlamadas[-1]['par_cont']
        argumento = pilaO.pop()
        tipo_argumento = pTipos.pop()
        param_table = directorio_funciones[current_call]['params']
        #Verificar que no se pase del tamaño de parámetros
        if current_par > len(param_table):
            raise tooManyParams(f"There are too many arguments for function {current_call}")
        #Verificar tipo de argumento en tabla de parámetros
        if tipo_argumento != param_table[current_par - 1]['tipo']:
            raise wrongParamType(f"Expected {param_table[current_par - 1]['tipo']} type argument! Got {tipo_argumento} instead.")
        cuadruplos.append(Quad('parameter', argumento, pLlamadas[-1]['par_cont'], None))
        pLlamadas[-1]['par_cont'] += 1

    #Final de una llamada
    def end_call(self, tree):
        current_call = pLlamadas[-1]['id']
        current_par = pLlamadas[-1]['par_cont']
        #Resetear
        pLlamadas.pop()
        #Verificar la cantidad de parámetros
        param_table = directorio_funciones[current_call]['params']
        if current_par <= len(param_table):
            raise missingParams(f'Missing parameters for function {current_call}')
        #Meter cuádruplo gosub
        cuadruplos.append(Quad('gosub', current_call, None, None))
        #Obtener el tipo de resultado
        tipo = directorio_funciones[current_call]['tipo']
        #Si la función no es void, hay que aplicar el parche
        if tipo != 'void':
            #Parche guadalupano, meter en memoria temporal el resultado
            temp = memoria.push_temp(tipo)
            #Meter en pilas
            pilaO.append(temp)
            pTipos.append(tipo)
            #Obtener dirección global, ahi estará guardado el resultado
            dir_global = directorio_funciones['global']['tabla_vars'][current_call]['direccion']
            #Cuadruplo para asignación de ese temporal
            cuadruplos.append(Quad('=', dir_global, None, temp))
        elif tipo == 'void' and pLlamadas:
            raise functionVoidError(f"Function {current_call} doesn't return anything!")

    def globals(self, tree):
        #Para guardar globales solo cambiamos el scope e iniciamos su parte en el directorio
        self.scope = 'global'
        directorio_funciones[self.scope] = {'tipo' : 'global', 'nombre' : 'global', 'tabla_vars': {}}

    #Semántica para main
    def main_start(self, tree):
        #Cambiar el scope a main y crear tabla de variables correspondiente
        inicio_main = pSaltos.pop()
        cuadruplos[inicio_main].res = len(cuadruplos) + 1
        self.scope = 'main'
        start_quad = len(cuadruplos) + 1
        directorio_funciones[self.scope] = {'tipo' : 'main', 'nombre' : 'main', 'tabla_vars': {}, 'inicio' : start_quad}

    #Semántica para variables
    def vars(self, tree):
        if tree.children == []: return
        #Meter variable a tabla de variables
        tipo = str(tree.children[0].children[0].children[0].children[0])
        nombre = str(tree.children[0].children[1])
        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        #checar doble declaración
        if nombre in tabla_vars:
            raise duplicateVariableError(f"Variable {nombre} is already defined")
        elif nombre in directorio_funciones['global']['tabla_vars']:
            raise duplicateVariableError(f"Variable {nombre} is already defined globally")
        #Apartar y obtener dirección de memoria
        if self.scope == 'global':
            direccion = memoria.push_global(tipo)
        else:
            direccion = memoria.push_local(tipo)
        variable = {'nombre' : nombre, 'tipo' : tipo, 'direccion' : direccion}
        #Si la asignación se realiza en la declaración, hay que meter el tipo y direccion en las pilas
        if tree.children[0].children[2].children and tree.children[0].children[2].children[0].data.value == 'asg_sign':
            pilaO.append(direccion)
            pTipos.append(tipo)
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
        tabla_local = directorio_funciones[self.scope]['tabla_vars']
        tabla_global = directorio_funciones['global']['tabla_vars']
        #checar si la variable está declarada en local
        if name in tabla_local:
            pilaO.append(tabla_local[name]['direccion'])
            pTipos.append(tabla_local[name]['tipo'])
        elif name in tabla_global:
            pilaO.append(tabla_global[name]['direccion'])
            pTipos.append(tabla_global[name]['tipo'])
        else:
            raise variableNotFoundError(f"Variable {name} is not defined.")

    def flo(self, tree):
        value = float(tree.children[0].value)
        if value in dirConsts:
            direccion = dirConsts[value]
        else:
            direccion = memoria.push_const('float', value)
            dirConsts[value] = direccion
        pTipos.append('float')
        pilaO.append(direccion)

    def integ(self, tree):
        value = int(tree.children[0].value)
        if value in dirConsts:
            direccion = dirConsts[value]
        else:
            direccion = memoria.push_const('int', value)
            dirConsts[value] = direccion
        pTipos.append('int')
        pilaO.append(direccion)

    def string(self, tree):
        value = str(tree.children[0].value)
        value = value.replace('"', '')
        if value in dirConsts:
            direccion = dirConsts[value]
        else:
            direccion = memoria.push_const('string', value)
            dirConsts[value] = direccion
        pTipos.append('string')
        pilaO.append(direccion)
    
    def true(self, tree):
        if True in dirConsts:
            direccion = dirConsts[True]
        else:
            direccion = memoria.push_const('bool', True)
            dirConsts[True] = direccion
        pTipos.append('bool')
        pilaO.append(direccion)
    
    def false(self, tree):
        if False in dirConsts:
            direccion = dirConsts[False]
        else:
            direccion = memoria.push_const('bool', False)
            dirConsts[False] = direccion
        pTipos.append('bool')
        pilaO.append(direccion)

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
                res = memoria.push_temp(tipoRes)
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
                res = memoria.push_temp(tipoRes)
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
                res = memoria.push_temp(tipoRes)
                oper = pOper.pop()
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
                res = memoria.push_temp(tipoRes)
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

                cuadruplos.append(Quad("=", op2, None, op1))
                pOper.pop()

    def asignacion(self, tree):
        #Buscar variable en directorio
        name = tree.children[0]
        #Si no se encuentra en directorio, error
        if name in directorio_funciones[self.scope]['tabla_vars']:
            direccion = directorio_funciones[self.scope]['tabla_vars'][name]['direccion']
            tipo = directorio_funciones[self.scope]['tabla_vars'][name]['tipo']

        elif name in directorio_funciones['global']['tabla_vars']:
            direccion = directorio_funciones['global']['tabla_vars'][name]['direccion']
            tipo = directorio_funciones['global']['tabla_vars'][name]['tipo']
        else:
            raise variableNotFoundError(f"Variable {name} is not defined.")
            
        #Push nombre y tipo para futura asignación
        pTipos.append(tipo)
        pilaO.append(direccion)

    def check_if(self, tree):
        #Punto neurálgico para meter gotoF del if
        eval = pilaO.pop()
        pTipos.pop()
        #Generar Cuádruplo
        cuadruplos.append(Quad("gotoF", eval, None, "---"))
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
        cuadruplos.append(Quad("gotoF", eval, None, "---"))
        pSaltos.append(len(cuadruplos) - 1)

    def end_while(self, tree):
        #Punto neurálgico para el final del while, rellenamos check_while y generamos goto al inicio
        end = pSaltos.pop()
        ret = pSaltos.pop()
        cuadruplos.append(Quad("goto", None, None, ret))
        cuadruplos[end].res = len(cuadruplos) + 1

