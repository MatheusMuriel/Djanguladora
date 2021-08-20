
class CalculadoraFuncao():    
    def __init__(self, _x5, _x4, _x3, _x2, _x1, _x, _epsilon):
        self.x5 = float(_x5)
        self.x4 = float(_x4)
        self.x3 = float(_x3)
        self.x2 = float(_x2)
        self.x1 = float(_x1)
        self.x  = float(_x)
        self.epsilon = ( 10**( float(_epsilon) ) )
        self.lista_intervalos = []
        
        self.calc_intervalo_real_num = []
        self.interacaoX = []
        self.interacaoFdeX = []
        self.interacaoBmenosA = []


    def calcFdeX(self, interacao):
        return self.x5*interacao**5 + self.x4*interacao**4 + self.x3*interacao**3 + self.x2*interacao**2 + self.x1*interacao + self.x

    def calcularIsolamento(self, intervalo):
        resultadoFinal = []
        
        for _ in range (intervalo*-2):
            result = self.calcFdeX(intervalo)
            intervalo = intervalo + 1
            resultadoFinal.append(result) 

        return resultadoFinal

    def calcularIntervalo(self, array_resultado, intervalo):
        resultadoFinal = []

        for i in range (intervalo*-2-1):
            if (array_resultado[i]<0 and array_resultado[i+1]>0) or (array_resultado[i]>0 and array_resultado[i+1]<0) :
                resultadoFinal.append(intervalo)
                resultadoFinal.append(intervalo+1)
                self.calc_intervalo_real_num.append(array_resultado[i])
                self.calc_intervalo_real_num.append(array_resultado[i+1])
            intervalo = intervalo + 1

        return resultadoFinal

    def calcZeroReais (self, a, b, intervalo):
        resultFdeX = 0
        interacao = (a+b)/2
        criterio_de_parada = abs((b-a)/2)
        resultFdeX = self.calcFdeX(interacao)

        intervalo.adiciona_iteracao(interacao, resultFdeX, criterio_de_parada)
        if criterio_de_parada < self.epsilon:
            self.interacaoX.append(interacao)
            self.lista_intervalos.append(intervalo)
            return self.interacaoX

        print(interacao, resultFdeX, criterio_de_parada)

        self.interacaoX.append(interacao) #esse e o resultado do b - a
        self.interacaoFdeX.append(resultFdeX)
        self.interacaoBmenosA.append(abs(b-a)/2)

        if resultFdeX < 0:
            self.calcZeroReais(a, interacao, intervalo)
        if resultFdeX > 0:
            self.calcZeroReais(interacao, b, intervalo)

    def filtraParaCalcular(self, calc_intervalo_real_num, calc_intervalo):
        #calcZeroReais(0, 1)
        tamanho_array = len(calc_intervalo)

        for i in range (0, tamanho_array, 2):
            if calc_intervalo_real_num[i] > 0:
                # Printa o Intervalo
                print(calc_intervalo[i], calc_intervalo[i+1])
                intervalo = Intervalo(calc_intervalo[i], calc_intervalo[i+1])
                self.calcZeroReais(calc_intervalo[i], calc_intervalo[i+1], intervalo)
            else:
                # Printa o Intervalo
                print(calc_intervalo[i], calc_intervalo[i+1])
                intervalo = Intervalo(calc_intervalo[i+1], calc_intervalo[i])
                self.calcZeroReais(calc_intervalo[i+1], calc_intervalo[i], intervalo)
            
    def calcular(self):
        intervalo = -5
        resultado = self.calcularIsolamento(intervalo)
        calc_intervalo = self.calcularIntervalo(resultado, intervalo)
        self.filtraParaCalcular(self.calc_intervalo_real_num, calc_intervalo)

        return(self.lista_intervalos)

"""
Tad para representar um resposta
"""
class Intervalo():

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.iteracao_contador = 0
        self.iteracoes = {}

    def adiciona_iteracao(self, x, f_de_x, b_menos_a):
        self.iteracao_contador += 1
        iteracao = self.iteracao_contador
        chave = iteracao
        valor = [x, f_de_x, b_menos_a]

        self.iteracoes[chave] = valor


def factor(x5, x4, x3, x2, x1, x, epsilon):
    return CalculadoraFuncao(x5, x4, x3, x2, x1, x, epsilon)