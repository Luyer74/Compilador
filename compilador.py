from lark import Lark
from luyer import *
from maquina_virtual import VM
l = Lark(open("lexicoysintaxis.lark", "r").read())

try:
  input = open("./pruebas/prueba.ly", "r").read()
  arbol = l.parse(input)
except EOFError:
  print(EOFError)

Luyer().visit_topdown(arbol)
vm = VM(cuadruplos)
vm.execute()
