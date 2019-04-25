import re as regex

texto = '19 2 3\n 4 5 6\n 7 8 9'  # trocar para arquivo

textoarray = texto.split("\n")
matriz = []

for texto in textoarray:
  lista = regex.findall('(\d+)', texto)
  for i in range(len(lista)):
    lista[i] = int(lista[i])
  matriz.append(lista)

print(matriz)

class reader:
	arq = open('inputpath', 'r')
	texto = arq.read()
	
	caracter = texto[0]
	i = 0
	matriz = []

	while (texto[i] < len(caracter))
		while (texto[i] != '\n')
		texto = 'l e ga\n l'
		i = 0
		while (i < len(texto)):
  		print(texto[i])
  		i = i + 1