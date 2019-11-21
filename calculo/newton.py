class Newton():
  def __init__(self, valores_X, valores_F, px):
    self.listaX = valores_X
    self.listaY = valores_F
    self.px = px

  #def Lnk(self, k, x, xi):
  
  def calcular(self):
    P = 0.0
    for k in range(self.n):
      P = P + self.fxi[k]*self.Lnk(k, self.x, self.xi)
    print(P)
    return P

def factory_newton(dictValores):
  valores_X = []
  valores_F = []
  px = 0

  n = (len(dictValores)-1) // 2

  for i in range (1, n+1):
    chaveX = 'X' + str(i)
    chaveF = 'F' + str(i)

    valores_X.append(dictValores[chaveX])
    valores_F.append(dictValores[chaveF])

  px = dictValores['PX']

  return Newton(valores_X, valores_F, px)
