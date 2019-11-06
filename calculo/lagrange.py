class Lagrange():

  def __init__(self, xi, fxi, x, n):
    self.xi = xi
    self.fxi = fxi
    self.x = x
    self.n = n

  def Lnk(self, k, x, xi):
    l_nk = 1.0
    n = len(xi)
    for i in range(n):
      if (i != k):
        l_nk = l_nk * ( (x - xi[i]) / (xi[k] - xi[i]) )
    return l_nk
  
  def calcular(self):
    P = 0.0
    for k in range(self.n):
      P = P + self.fxi[k]*self.Lnk(k, self.x, self.xi)
    print(P)
    return P

def factory_lagrange(dictValores):
  valores_X = []
  valores_F = []
  px = 0

  for k,v in dictValores.items():
    if "F" in str(k):
      valores_F.append(v)
    elif "PX" in str(k):
      px = v
    elif "X" in str(k):
      valores_X.append(v)
  
  x = px
  xi = valores_X
  fxi = valores_F
  n  = len(xi)
  print((xi, fxi, x, n))
  return Lagrange(xi, fxi, x, n)
