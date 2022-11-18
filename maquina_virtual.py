from luyer import directorio_funciones, memoria as memoria_main
from memoria import Memoria

class VM():
  def __init__(self, quads):
    self.quads = quads
    self.ip = 1
    self.call_stack = []
  
  def execute(self):
    #Iniciar con la memoria del main
    self.call_stack.append(memoria_main)
    # print(self.call_stack[-1].memoria_global)
    #Comenzamos ejecución de cuádruplos
    while(self.quads[self.ip - 1].op != "endprogram"):
      self.execute_quad(self.quads[self.ip - 1])
    # print("end")
    # print(self.call_stack[-1].memoria_global)
    # print(self.call_stack[-1].memoria_local)
    # print(self.call_stack[-1].memoria_temporal)
    # print(self.call_stack[-1].memoria_constante)

  #Manejador de ejecución
  def execute_quad(self, quad):
    # print("executing quad number ", self.ip)
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

  #Una función para cada operación de la MV
  def goto(self, quad):
    #Cambiar instruction pointer al # de cuádruplo
    self.ip = quad.res

  def gotoF(self, quad):
    #Obtener resultado de la condición
    cond = quad.opr1
    value = self.call_stack[-1].get_value(cond)
    # print(value)
    if value == False:
      self.ip = quad.res
    else:
      self.ip += 1

  def print(self, quad):
    #Obtener dirección
    res_dir = quad.res
    value = self.call_stack[-1].get_value(res_dir)
    #Imprimir
    print(value)
    self.ip += 1

  def assign(self, quad):
    #Obtener direcciones
    add1 = quad.opr1
    add2 = quad.res
    #Obtener el valor a asignar
    value = self.call_stack[-1].get_value(add1)
    #Realizar asignación de valor
    self.call_stack[-1].assign(add2, value)
    #Move to next quad
    self.ip += 1

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
    self.ip += 1

      

    