class functionNameError(Exception):
  pass

class variableNotFoundError(Exception):
  pass

class duplicateVariableError(Exception):
  pass

class variableNoValue(Exception):
  pass

class stackOverflow(Exception):
  pass

class functionNotFound(Exception):
  pass

class wrongParamType(Exception):
  pass

class tooManyParams(Exception):
  pass

class missingParams(Exception):
  pass