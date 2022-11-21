#Cada sección cuenta con offset de espacio, comenzando con la dirección offset
offset = 1000
from errors import *

class Memoria():
  def __init__(self):
    self.memoria_global = {'int' : [], 'float': [], 'string': [], 'bool' : []}
    self.memoria_local = {'int' : [], 'float': [], 'string': [], 'bool' : []}
    self.memoria_temporal = {'int' : [], 'float': [], 'string': [], 'bool' : [], 'pointer' : []}
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

  def push_temp(self, tipo, valor = 'na'):
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
    if tipo == 'pointer':
      current_size = len(self.memoria_temporal['pointer'])
      if current_size >= offset: 
          raise stackOverflow("Stack memory exceeded!")
      self.memoria_temporal['pointer'].append(valor)
      return current_size + offset * 5 + tempoffset

  def push_const(self, tipo, valor = 'na'):
    constoffset = 13000
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
    self.memoria_temporal = {'int' : [], 'float': [], 'string': [], 'bool' : [], 'pointer' : []}

  def get_value(self, address):
    #Obtener valores globales
    if address >= 1000 and address <= 4999:
      if address <= 1999:
        return self.memoria_global['int'][address - 1000]
      elif address <= 2999:
        return self.memoria_global['float'][address - 2000]
      elif address <= 3999:
        return self.memoria_global['string'][address - 3000]
      elif address <= 4999:
        return self.memoria_global['bool'][address - 4000]
    #Obtener valores locales
    elif address >= 5000 and address <= 8999:
      if address <= 5999:
        return self.memoria_local['int'][address - 5000]
      elif address <= 6999:
        return self.memoria_local['float'][address - 6000]
      elif address <= 7999:
        return self.memoria_local['string'][address - 7000]
      elif address <= 8999:
        return self.memoria_local['bool'][address - 8000]
    #Obtener valores temporales
    elif address >= 9000 and address <= 13999:
      if address <= 9999:
        return self.memoria_temporal['int'][address - 9000]
      elif address <= 10999:
        return self.memoria_temporal['float'][address - 10000]
      elif address <= 11999:
        return self.memoria_temporal['string'][address - 11000]
      elif address <= 12999:
        return self.memoria_temporal['bool'][address - 12000]
      elif address <= 13999:
        return self.memoria_temporal['pointer'][address - 13000]
    #Obtener valores constantes
    elif address >= 14000 and address <= 17999:
      if address <= 14999:
        return self.memoria_constante['int'][address - 14000]
      elif address <= 15999:
        return self.memoria_constante['float'][address - 15000]
      elif address <= 16999:
        return self.memoria_constante['string'][address - 16000]
      elif address <= 17999:
        return self.memoria_constante['bool'][address - 17000]
    
  def assign(self, address, value):
    #Asignar valores globales
    if address >= 1000 and address <= 4999:
      if address <= 1999:
        self.memoria_global['int'][address - 1000] = value
      elif address <= 2999:
        self.memoria_global['float'][address - 2000] = value
      elif address <= 3999:
        self.memoria_global['string'][address - 3000] = value
      elif address <= 4999:
        self.memoria_global['bool'][address - 4000] = value
    #Asignar valores locales
    elif address >= 5000 and address <= 8999:
      if address <= 5999:
        self.memoria_local['int'][address - 5000] = value
      elif address <= 6999:
        self.memoria_local['float'][address - 6000] = value
      elif address <= 7999:
        self.memoria_local['string'][address - 7000] = value
      elif address <= 8999:
        self.memoria_local['bool'][address - 8000] = value
    #Asignar valores temporales
    elif address >= 9000 and address <= 13999:
      if address <= 9999:
        self.memoria_temporal['int'][address - 9000] = value
      elif address <= 10999:
        self.memoria_temporal['float'][address - 10000] = value
      elif address <= 11999:
        self.memoria_temporal['string'][address - 11000] = value
      elif address <= 12999:
        self.memoria_temporal['bool'][address - 12000] = value
      elif address <= 13999:
        self.memoria_temporal['pointer'][address - 13000] = value
    #Asignar valores constantes
    elif address >= 14000 and address <= 17999:
      if address <= 14999:
        self.memoria_constante['int'][address - 14000] = value
      elif address <= 15999:
        self.memoria_constante['float'][address - 15000] = value
      elif address <= 16999:
        self.memoria_constante['string'][address - 16000] = value
      elif address <= 17999:
        self.memoria_constante['bool'][address - 17000] = value    