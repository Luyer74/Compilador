from lark import Lark

l = Lark(open("lexicoysintaxis.lark", "r").read())

try:
  input = open("test.txt", "r").read()
  print(l.parse(input))
  print("Correct Input")
except EOFError:
  print(EOFError)
  print("Incorrect Input")