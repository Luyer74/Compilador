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
pDim = collections.deque()

#Memoria
memoria = Memoria()

#Constantes
dir_consts = {}


class Luyer(Visitor):
    def __init__(self):
        #Variable para guardar el scope actual
        self.scope = ""
        self.par_count = 0
        self.void_function = False
        self.currArr = ""

    def gotomain(self, tree):
        cuadruplos.append(Quad("goto", None, None, "----"))
        pSaltos.append(len(cuadruplos) - 1)
    
    #Semántica para escritura
    def escritura(self, tree):
        res = pilaO.pop()
        pTipos.pop()
        cuadruplos.append(Quad("print", None, None, res))

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
        directorio_funciones[self.scope]['params'].append({'tipo' : tipo, 'direccion': direccion})
        #Crear parametro
        parametro = {'nombre' : id_parametro, 'tipo' : tipo, 'direccion' : direccion}
        # Insertar en tabla de variables correspondiente a su scope
        tabla_vars[id_parametro] = parametro

    #Punto para el return
    def end_return(self, tree):
        function_type = directorio_funciones[self.scope]['tipo']
        if function_type == 'void':
            raise functionVoidError(f"Function {self.scope} is void. It can't return anything")
        res = pilaO.pop()
        tipo_ret = pTipos.pop()
        #Si el tipo de retorno y el tipo de función no coinciden, error
        if tipo_ret != function_type:
            raise returnTypeError(f"Function {self.scope} expects {function_type}, returns {tipo_ret} instead")
        #Agregar cuadruplo de return
        cuadruplos.append(Quad("return", self.scope, None, res))

    #Final de la función
    def endfunc(self, tree):
        #Agregar tamaño de memoria al directorio
        directorio_funciones[self.scope]['memoria'] = {
            'local' : [len(memoria.memoria_local[name]) for name in memoria.memoria_local],
            'temporal' : [len(memoria.memoria_temporal[name]) for name in memoria.memoria_temporal]
        }
        cuadruplos.append(Quad("endfunc", None, None, None))
        #Limpiar memoria
        memoria.clear_local()
        memoria.clear_temp()
        self.scope = None

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
        pOper.append('(')
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
        cuadruplos.append(Quad("parameter", argumento, pLlamadas[-1]['par_cont'], current_call))
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
        cuadruplos.append(Quad('gosub', None, None, current_call))
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
        pOper.pop()

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
    def variable(self, tree):
        if tree.children == []: return
        #Meter variable a tabla de variables
        tipo = str(tree.children[0].children[0].children[0])
        nombre = str(tree.children[1])
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
        if len(tree.children) > 2 :
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
        if value in dir_consts:
            direccion = dir_consts[value]
        else:
            direccion = memoria.push_const('float', value)
            dir_consts[value] = direccion
        pTipos.append('float')
        pilaO.append(direccion)

    def integ(self, tree):
        value = int(tree.children[0].value)
        if value in dir_consts:
            direccion = dir_consts[value]
        else:
            direccion = memoria.push_const('int', value)
            dir_consts[value] = direccion
        pTipos.append('int')
        pilaO.append(direccion)

    def string(self, tree):
        value = str(tree.children[0].value)
        value = value.replace('"', '')
        if value in dir_consts:
            direccion = dir_consts[value]
        else:
            direccion = memoria.push_const('string', value)
            dir_consts[value] = direccion
        pTipos.append('string')
        pilaO.append(direccion)
    
    def true(self, tree):
        if True in dir_consts:
            direccion = dir_consts[True]
        else:
            direccion = memoria.push_const('bool', True)
            dir_consts[True] = direccion
        pTipos.append('bool')
        pilaO.append(direccion)
    
    def false(self, tree):
        if False in dir_consts:
            direccion = dir_consts[False]
        else:
            direccion = memoria.push_const('bool', False)
            dir_consts[False] = direccion
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

    #Puntos neurálgicos para arreglos
    def variable_arr(self, tree):
        if tree.children == []: return
        #Meter variable a tabla de variables
        tipo = str(tree.children[0].children[0].children[0])
        nombre = str(tree.children[1])
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
        variable = {'nombre' : nombre, 'tipo' : tipo, 'direccion' : direccion, 'arr': True, 'dims' : [], 'size' : 1}
        tabla_vars[nombre] = variable
        self.currArr = nombre
    
    def create_node(self, tree):
        #Obtener lista de dimensiones
        dim_list = directorio_funciones[self.scope]['tabla_vars'][self.currArr]['dims']
        R = directorio_funciones[self.scope]['tabla_vars'][self.currArr]['size']
        #El tamaño del nodo estará en la pila como dirección constante
        dir_const = pilaO.pop()
        pTipos.pop()
        #Si la dirección no es temporal entera hay un error en el índice
        if dir_const < 14000 or dir_const > 14999:
            raise indexError("Array indexes can only be initialized with integers")
        rango = memoria.memoria_constante['int'][dir_const-14000]
        R *= rango
        #Crear "nodo" de dimensión
        dim_list.append([rango, None])
        directorio_funciones[self.scope]['tabla_vars'][self.currArr]['size'] = R

    def set_nodes(self, tree):
        #Setear valores de Mn en los nodos de dimensiones
        dim = 0
        dim_list = directorio_funciones[self.scope]['tabla_vars'][self.currArr]['dims']
        R = directorio_funciones[self.scope]['tabla_vars'][self.currArr]['size']
        while dim < len(dim_list):
            m_dim = int(R / (dim_list[dim][0]))
            dim_list[dim][1] = m_dim
            R = m_dim
            dim += 1
        #Apartar memoria
        size = directorio_funciones[self.scope]['tabla_vars'][self.currArr]['size']
        tipo = directorio_funciones[self.scope]['tabla_vars'][self.currArr]['tipo']
        cont = 1
        while cont < size:
            if self.scope != 'global':
                memoria.push_local(tipo)
                cont += 1
            else:
                memoria.push_global(tipo)
                cont += 1
        #Resetear
        self.currArr = None

    def array_access(self, tree):
        #Obtener ID y tipo
        name = str(tree.children[0].value)
        tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        #Verificar que exista en tablas de variables
        if name not in tabla_vars:
            if name in directorio_funciones['global']['tabla_vars']:
                tabla_vars = directorio_funciones['global']['tabla_vars']
            else:
                raise variableNotFoundError(f"Variable {name} is not defined")
        tipo = tabla_vars[name]['tipo']
        #Verificar que sea variable con dimensiones
        if 'arr' not in tabla_vars[name]:
            raise notArrayType(f"Variable {name} is not array-type")
        #Definir dim
        dim = 1
        pDim.append([name, dim, tipo])
        #Pushear fondo falso
        pOper.append('(')

    def check_dim(self, tree):
        #Obtener nodo
        name = pDim[-1][0]
        dim = pDim[-1][1]
        #Checar si es global o local
        if name in directorio_funciones[self.scope]['tabla_vars']:
            tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        elif name in directorio_funciones['global']['tabla_vars']:
            tabla_vars = directorio_funciones['global']['tabla_vars']
        nodos = tabla_vars[name]['dims']
        limS = nodos[dim - 1][0]
        index = pilaO[-1]
        #Verificar límites
        cuadruplos.append(Quad("ver", index, 0, limS))
        #Checar si hay más nodos
        if len(nodos) > dim:
            aux = pilaO.pop()
            tipo_nodo = pTipos.pop()
            if tipo_nodo != 'int':
                raise indexError("Indexes must be integers")
            m_dim = nodos[dim - 1][1]
            #Multiplicar por m en cuádruplo
            temp_1 = memoria.push_temp('int')
            cuadruplos.append(Quad("*", aux, m_dim, temp_1))
            pilaO.append(temp_1)
            pTipos.append('int')
        #Cuadruplo de suma
        if dim > 1:
            aux2 = pilaO.pop()
            aux2_tipo = pTipos.pop()
            aux1 = pilaO.pop()
            aux1_tipo = pTipos.pop()
            if aux2_tipo != 'int' or aux1_tipo != 'int':
                raise indexError("Indexes must be integers")
            temp_2 = memoria.push_temp('int')
            cuadruplos.append(Quad("+", aux1, aux2, temp_2))
            pilaO.append(temp_2)
            pTipos.append('int')

        #Actualizar dim
        pDim[-1][1] += 1

    def end_arr(self, tree):
        #Aux contiene nuestro indice
        aux = pilaO.pop()
        tipo_i = pTipos.pop()
        if tipo_i != 'int':
            raise indexError("Indexes must be integers")
        #Checamos que coincidan las dims
        name = pDim[-1][0]
        dim = pDim[-1][1]
        tipo = pDim[-1][2]
        #Checar si es global o local
        if name in directorio_funciones[self.scope]['tabla_vars']:
            tabla_vars = directorio_funciones[self.scope]['tabla_vars']
        elif name in directorio_funciones['global']['tabla_vars']:
            tabla_vars = directorio_funciones['global']['tabla_vars']
        dim_size = len(tabla_vars[name]['dims'])
        #Error si no coinciden las dimensiones
        if dim_size != dim - 1:
            raise indexError(f"Dimensions for variable {name} do not match")
        #Obtenemos dirección base
        dir_base = tabla_vars[name]['direccion']
        #Creamos dirección temporal pointer
        temp_p = memoria.push_temp('pointer')
        #Generamos cuádruplo de suma de dirB
        cuadruplos.append(Quad("+", aux, dir_base, temp_p))
        pilaO.append(temp_p)
        pTipos.append(tipo)
        pOper.pop()
        pDim.pop()
    
    def endprogram(self,tree):
        cuadruplos.append(Quad("endprogram", None, None, None))
    