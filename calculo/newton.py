class Newton():
  def __init__(self, valores_X, valores_F, px):
    self.listaX = valores_X
    self.listaY = valores_F
    self.px = px

  def calcula_diferenca(self, lista, fator):
    lista_resultados = []
    for i in range(0, len(lista)-1):
      dividendo = lista[i+1] - lista[i]
      divisor = self.listaX[i+fator] - self.listaX[i]
      resultado = dividendo / divisor
      lista_resultados.append(resultado)
    return lista_resultados

  def calcula_resultados(self):
    lista_resultados = [self.listaY]
    for i in range(1, len(self.listaX)):
      lista_da_vez = self.calcula_diferenca(lista_resultados[len(lista_resultados)-1], i)
      lista_resultados.append(lista_da_vez)

    return lista_resultados

  def prepara_lista_resultados(self, lista_resultados):
    results_aux = []
    for rest in lista_resultados:
      results_aux.append(rest[0])

    return results_aux
  
  def calcula_diferencas_divididas(self, results):
    final = 0
    resultado_final = 0
    acumulator = 0
    for i in range (0, len(results)):
      vl = self.listaX[i]
      ac_aux = (acumulator * (self.px - vl)) if acumulator != 0 else (self.px - vl)
      acumulator = ac_aux
      try:
        final += acumulator * results[i+1]
      except:
        final = final + self.listaX[0]
    return final

  def calcular(self):
    lista_resultados = self.calcula_resultados()
    results_formatados = self.prepara_lista_resultados(lista_resultados)
    resultado_final = self.calcula_diferencas_divididas(results_formatados)
    return resultado_final

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
