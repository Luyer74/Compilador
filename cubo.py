#Define cubo semántico como un diccionario anidado

cubo = {
  '+' : { 
    'int' : {
      'int' : 'int',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'float',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'string',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '-' : { 
    'int' : {
      'int' : 'int',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'float',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERRPR',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '*' : { 
    'int' : {
      'int' : 'int',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'float',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '/' : { 
    'int' : {
      'int' : 'float',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'float',
      'float' : 'float',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '>' : { 
    'int' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'bool',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '<' : { 
    'int' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'bool',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '!=' : { 
    'int' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'bool',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '==' : { 
    'int' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'float' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    },
    'string' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'bool',
      'bool' : 'ERROR'
    },
    'bool' : {
      'int' : 'ERROR',
      'float' : 'ERROR',
      'string' : 'ERROR',
      'bool' : 'ERROR'
    }
  }, 
  '&&' : { 
    'int' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    },
    'float' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    },
    'string' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    },
    'bool' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    }
  }, 
  '||' : { 
    'int' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    },
    'float' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    },
    'string' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    },
    'bool' : {
      'int' : 'bool',
      'float' : 'bool',
      'string' : 'bool',
      'bool' : 'bool'
    }
  }, 
}