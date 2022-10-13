from lark import Lark
from luyer import *
l = Lark(open("lexicoysintaxis.lark", "r").read())

try:
  input = open("test1.txt", "r").read()
  arbol = l.parse(input)
  # print(l.parse(input))
  print("Correct Input")
except EOFError:
  print(EOFError)
  print("Incorrect Input")

Luyer().visit_topdown(arbol)

print(directorio_funciones)
