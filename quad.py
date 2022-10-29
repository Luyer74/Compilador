class Quad():
  def __init__(self, op, opr1, opr2, res):
    self.op = op
    self.opr1 = opr1
    self.opr2 = opr2
    self.res = res
  
  def print_quad(self):
    print(self.op, self.opr1, self.opr2, self.res)
