from lark import Lark
from luyer import *
l = Lark(open("lexicoysintaxis.lark", "r").read())

try:
  input = open("test1.txt", "r").read()
  arbol = l.parse(input)
  print("Correct Input")
except EOFError:
  print(EOFError)
  print("Incorrect Input")

Luyer().visit_topdown(arbol)

print(directorio_funciones)
print(pilaO)
print(pOper)
print(pTipos)

cont = 1
for cuad in cuadruplos:
  print(cont)
  cont += 1
  cuad.print_quad()