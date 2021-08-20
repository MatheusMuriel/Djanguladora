from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

try:
	# Django 2
	from django.contrib.staticfiles.templatetags.staticfiles import static
except ModuleNotFoundError:
	# Django 3
	from django.templatetags.static import static

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view

from .calculadora import factor
from .gauss import factory
from .lagrange import factory_lagrange
from .newton import factory_newton

import re
import json

# ---- Metodo da Bisseção ----
@csrf_exempt
def bissecao(request):
	if request.method == 'POST':
		dados = str(request.body)
		v = spliter_request(dados)
		c = executarCalculo(v[0], v[1], v[2], v[3], v[4], v[5], v[6])
		sc = serializadorDeResposta(c)
		return HttpResponse(sc)

def spliter_request(dados):
	dados_limpos = re.sub(r"(\[|\]|\\|\'|b|\")","",dados)
	return dados_limpos.split(",")

def executarCalculo(x5, x4, x3, x2, x1, x, epsilon):
	calc = factor(x5, x4, x3, x2, x1, x, epsilon)
	return calc.calcular()

def serializadorDeResposta(lista_resposta):
	resposta = ""

	#Cada objeto
	for intervalo in lista_resposta:
		resposta += "$$$"

		a = intervalo.a
		b = intervalo.b
		resposta += ("{}::{}".format(a, b))

		d = intervalo.iteracoes
		for chave, valor in d.items():
			resposta += "#{}[".format(chave)
			for vl in valor:
				resposta += "{};".format(vl)
			resposta += "]"

		print(resposta)
	
	return(resposta)

# ---- Forma de Newton ----
# curl 'http://localhost:8000/newton/' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: http://localhost:8080/' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: http://localhost:8080' -H 'Connection: keep-alive' --data '{"X1":1,"X2":2,"X3":3,"X4":4,"X5":5,"F1":11,"F2":22,"F3":33,"F4":44,"F5":55,"X":999}'
@csrf_exempt
def newton(request):
	if request.method == 'POST':
		dados = str(request.body)
		v = spliter_request_lagrange(dados) #Usa o mesmo spliter de Lagrange
		c = executar_calculo_newton(v)
		return HttpResponse(c)

def executar_calculo_newton(dictValores):
	metodo = factory_newton(dictValores)
	return metodo.calcular()


# ---- Forma de Lagrange ----
# curl 'http://localhost:8000/lagrange/' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3' --compressed -H 'Referer: http://localhost:8080/' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: http://localhost:8080' -H 'Connection: keep-alive' --data '{"X1":1,"X2":2,"X3":3,"X4":4,"X5":5,"F1":11,"F2":22,"F3":33,"F4":44,"F5":55,"X":999}'
@csrf_exempt
def lagrange(request):
	if request.method == 'POST':
		dados = str(request.body)
		v = spliter_request_lagrange(dados)
		c = executar_calculo_lagrange(v)
		#sc = serializador_resposta_lagrange(c)
		return HttpResponse(c)

def spliter_request_lagrange(dados):
	str_limpa = dados[2:-1]
	arrDados = re.sub(r"({|}|\")","", str_limpa).split(",")
	dictValores = {}
	for item in arrDados:
		arrItem = item.split(":")
		chave = arrItem[0]
		if not "null" in arrItem[1]:
			valor = float(arrItem[1])
			dictValores[chave] = valor
	return dictValores

def executar_calculo_lagrange(dictValores):
	metodo = factory_lagrange(dictValores)
	return metodo.calcular()


# ---- Metodo da Gauss ----
# Exemplo de request curl:
# curl 'http://localhost:8000/gauss/' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: http://localhost:8080' -H 'Connection: keep-alive' -H 'Referer: http://localhost:8080/' --data '{"11":1,"12":"2","13":"3","14":"10","21":"4","22":"5","23":"6","24":"20","31":"7","32":"8","33":"9","34":"30"}'
@csrf_exempt
def gauss(request):
	if request.method == 'POST':
		dados = str(request.body)
		v = spliter_request_gauss(dados)
		c = executarCalculoGauss(v)
		sc = serializadorDeRespostaGauss(c)
		return HttpResponse(sc)

def spliter_request_gauss(dados):
	str_limpa = dados[2:-1]
	arrDados = re.sub(r"({|}|\")","", str_limpa).split(",")
	dictMaptriz = {}
	for item in arrDados:
		arrItem = item.split(":")
		chave = arrItem[0]
		valor = float(arrItem[1])
		dictMaptriz[chave] = valor

	return dictMaptriz

def executarCalculoGauss(dictMap):
	gauss = factory(dictMap)
	return gauss.calcular()

def serializadorDeRespostaGauss(dictResposta):
	passos = dictResposta['passos']
	matriz_x = str(dictResposta['matriz_X'])
	matriz_l = str(dictResposta['matriz_L'])
	matriz_u = str(dictResposta['matriz_U'])

	str_passos = ""
	for passo_i in passos:
		str_passos += str(passo_i)

	resposta = str_passos + "§§§" + matriz_x + "§§§" + matriz_l + "§§§" + matriz_u
	return(resposta)
