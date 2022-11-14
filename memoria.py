#Cada sección cuenta con offset de espacio, comenzando con la dirección offset
offset = 1000
from errors import *

class Memoria():
  def __init__(self):
    self.memoria_global = {'int' : [], 'float': [], 'string': [], 'bool' : []}
    self.memoria_local = {'int' : [], 'float': [], 'string': [], 'bool' : []}
    self.memoria_temporal = {'int' : [], 'float': [], 'string': [], 'bool' : []}
    self.memoria_constante = {'int' : [], 'float': [], 'string': [], 'bool' : []}

  def push_global(self, tipo):
    if tipo == 'int':
      current_size = len(self.memoria_global['int'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_global['int'].append('na')
      return current_size + offset
    if tipo == 'float':
      current_size = len(self.memoria_global['float'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_global['float'].append('na')
      return current_size + offset * 2
    if tipo == 'string':
      current_size = len(self.memoria_global['string'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_global['string'].append('na')
      return current_size + offset * 3
    if tipo == 'bool':
      current_size = len(self.memoria_global['bool'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_global['bool'].append('na')
      return current_size + offset * 4

  def push_local(self, tipo):
    localoffset = 4000
    if tipo == 'int':
      current_size = len(self.memoria_local['int'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_local['int'].append('na')
      return current_size + offset + localoffset
    if tipo == 'float':
      current_size = len(self.memoria_local['float'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_local['float'].append('na')
      return current_size + offset * 2 + localoffset
    if tipo == 'string':
      current_size = len(self.memoria_local['string'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_local['string'].append('na')
      return current_size + offset * 3 + localoffset
    if tipo == 'bool':
      current_size = len(self.memoria_local['bool'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_local['bool'].append('na')
      return current_size + offset * 4 + localoffset

  def push_temp(self, tipo):
    tempoffset = 8000
    if tipo == 'int':
      current_size = len(self.memoria_temporal['int'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_temporal['int'].append('na')
      return current_size + offset + tempoffset
    if tipo == 'float':
      current_size = len(self.memoria_temporal['float'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_temporal['float'].append('na')
      return current_size + offset * 2 + tempoffset
    if tipo == 'string':
      current_size = len(self.memoria_temporal['string'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_temporal['string'].append('na')
      return current_size + offset * 3 + tempoffset
    if tipo == 'bool':
      current_size = len(self.memoria_temporal['bool'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_temporal['bool'].append('na')
      return current_size + offset * 4 + tempoffset

  def push_const(self, tipo, valor = 'na'):
    constoffset = 12000
    if tipo == 'int':
      current_size = len(self.memoria_constante['int'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_constante['int'].append(valor)
      return current_size + offset + constoffset
    if tipo == 'float':
      current_size = len(self.memoria_constante['float'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_constante['float'].append(valor)
      return current_size + offset * 2 + constoffset
    if tipo == 'string':
      current_size = len(self.memoria_constante['string'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_constante['string'].append(valor)
      return current_size + offset * 3 + constoffset
    if tipo == 'bool':
      current_size = len(self.memoria_constante['bool'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_constante['bool'].append(valor)
      return current_size + offset * 4 + constoffset
    
  def clear_local(self):
    self.memoria_local = {'int' : [], 'float': [], 'string': [], 'bool' : []}

  def clear_temp(self):
    self.memoria_temp = {'int' : [], 'float': [], 'string': [], 'bool' : []}
