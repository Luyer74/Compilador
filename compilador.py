from lark import Lark
from luyer import *
l = Lark(open("lexicoysintaxis.lark", "r").read())

try:
  input = open("test2.txt", "r").read()
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
print(pDim)
print(memoria.memoria_global)
print(memoria.memoria_constante)
print(memoria.memoria_local)
print(memoria.memoria_temporal)

cont = 1
for cuad in cuadruplos:
  print(cont)
  cont += 1
  cuad.print_quad()