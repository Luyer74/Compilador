from luyer import directorio_funciones, memoria as memoria_main
from memoria import Memoria

class VM():
  def __init__(self, quads):
    self.quads = quads
    self.call_stack = []
    self.ip_stack = [1]
    self.next_mem = None
  
  def execute(self):
    #Iniciar con la memoria del main
    self.call_stack.append(memoria_main)
    # print(self.call_stack[-1].memoria_global)
    # for i, quad in enumerate(self.quads):
    #   print(i + 1)
    #   quad.print_quad()
    #Comenzamos ejecución de cuádruplos
    while(self.quads[self.ip_stack[-1] - 1].op != "endprogram"):
      self.execute_quad(self.quads[self.ip_stack[-1] - 1])
    # print("end")
    # print(self.call_stack[-1].memoria_global)
    # print(self.call_stack[-1].memoria_local)
    # print(self.call_stack[-1].memoria_temporal)
    # print(self.call_stack[-1].memoria_constante)

  #Manejador de ejecución
  def execute_quad(self, quad):
    # print("executing quad number ", self.ip_stack[-1])
    # quad.print_quad()
    if quad.op == "goto":
      self.goto(quad)
    elif quad.op == "=":
      self.assign(quad)
    elif quad.op in ["+", "-", "/", "*", "&&", "||", ">", "<", ">=", "<=", "=="]:
      self.operation(quad)
    elif quad.op == "print":
      self.print(quad)
    elif quad.op == "gotoF":
      self.gotoF(quad)
    elif quad.op == "era":
      self.era(quad)
    elif quad.op == "parameter":
      self.param(quad)
    elif quad.op == "gosub":
      self.gosub(quad)
    elif quad.op == "return":
      self.ret(quad)

  #Una función para cada operación de la MV
  def goto(self, quad):
    #Cambiar instruction pointer al # de cuádruplo
    self.ip_stack[-1] = quad.res

  def gotoF(self, quad):
    #Obtener resultado de la condición
    cond = quad.opr1
    value = self.call_stack[-1].get_value(cond)
    # print(value)
    if value == False:
      self.ip_stack[-1] = quad.res
    else:
      self.ip_stack[-1] += 1

  def print(self, quad):
    #Obtener dirección
    res_dir = quad.res
    value = self.call_stack[-1].get_value(res_dir)
    #Imprimir
    print(value)
    self.ip_stack[-1] += 1

  def assign(self, quad):
    #Obtener direcciones
    add1 = quad.opr1
    add2 = quad.res
    #Obtener el valor a asignar
    value = self.call_stack[-1].get_value(add1)
    #Realizar asignación de valor
    self.call_stack[-1].assign(add2, value)
    #Move to next quad
    self.ip_stack[-1] += 1

  def operation(self, quad):
    #Obtener direcciones
    op = quad.op
    add1 = quad.opr1
    add2 = quad.opr2
    res_dir = quad.res
    #Obtener memoria 
    current_memory = self.call_stack[-1]
    #Obtener valores de las direcciones y realizar operación
    val1 = current_memory.get_value(add1)
    val2 = current_memory.get_value(add2)
    if op == '*': res = val1 * val2
    elif op == '/': res = val1 / val2
    elif op == '+': res = val1 + val2
    elif op == '-': res = val1 - val2
    elif op == '&&': res = val1 and val2
    elif op == '||': res = val1 or val2
    elif op == '>': res = val1 > val2
    elif op == '<': res = val1 < val2
    elif op == '>=': res = val1 >= val2
    elif op == '<=': res = val1 <= val2
    elif op == '==': res = val1 == val2
    #Asignar resultado
    self.call_stack[-1].assign(res_dir, res)
    self.ip_stack[-1] += 1

  def era(self, quad):
    #Obtener nombre de la función
    nombre = quad.res
    memoria_nueva = Memoria()
    #Obtener la cantidad de memoria requerida
    local_size = directorio_funciones[nombre]['memoria']['local']
    temp_size = directorio_funciones[nombre]['memoria']['temporal']
    #Apartar memoria local
    for index, value in enumerate(local_size):
      while value:
        if index == 0:
          memoria_nueva.push_local('int')
        elif index == 1:
          memoria_nueva.push_local('float')
        elif index == 2:
          memoria_nueva.push_local('string')
        elif index == 3:
          memoria_nueva.push_local('bool')
        value -=1
    #Apartar memoria temporal
    for index, value in enumerate(temp_size):
      while value:
        if index == 0:
          memoria_nueva.push_temp('int')
        elif index == 1:
          memoria_nueva.push_temp('float')
        elif index == 2:
          memoria_nueva.push_temp('string')
        elif index == 3:
          memoria_nueva.push_temp('bool')
        elif index == 4:
          memoria_nueva.push_temp('pointer')
        value -=1
    memoria_nueva.memoria_global = self.call_stack[-1].memoria_global
    memoria_nueva.memoria_constante = self.call_stack[-1].memoria_constante
    self.next_mem = memoria_nueva
    self.ip_stack[-1] +=1

  def param(self, quad):
    #Obtener el valor del parámetro
    dir_val = quad.opr1
    val = self.call_stack[-1].get_value(dir_val)
    #Obtener el número del parámetro
    p_num = quad.opr2
    #Obtener la dirección en la siguiente memoria
    function_name = quad.res
    next_addr = directorio_funciones[function_name]['params'][p_num - 1]['direccion']
    #Asignar el valor en la nueva memoria
    self.next_mem.assign(next_addr, val)
    self.ip_stack[-1] += 1
  
  def gosub(self, quad):
    #Obtener nombre
    nombre = quad.res
    #Antes de ir al cuádruplo de la función hay que cambiar a la nueva memoria
    self.call_stack.append(self.next_mem)
    self.next_mem = None
    #Guardamos la instrucción siguiente para regresar a ella
    self.ip_stack[-1] += 1
    #Obtenemos número del cuádruplo para cambiar el IP
    quad_func = directorio_funciones[nombre]['inicio']
    self.ip_stack.append(quad_func)

  def ret(self, quad):
    #Obtener nombre de la función
    nombre = quad.opr1
    #Obtener dirección y el valor a asignar
    dir = quad.res
    value = self.call_stack[-1].get_value(dir)
    #Obtener variable global
    dir_res = directorio_funciones['global']['tabla_vars'][nombre]['direccion']
    #Asignarla a la memoria anterior
    self.call_stack[-2].assign(dir_res, value)
    #Regresar al cuádruplo siguiente de la llamada
    self.ip_stack.pop()
    #Sacar la memoria actual
    self.call_stack.pop()


    