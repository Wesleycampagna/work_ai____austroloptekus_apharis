class writer:
	def writeArchive(listaInt):
		
		arq = open('saida-genetico.txt', 'w')
		listaStr = list(map(str, listaInt))
		separator = ' '
		result = [separator.join(listaStr)]
		result = [r.replace(' ', ',') for r in result]
		arq.writelines(result)
		arq.close()
	
	texto = []
	texto.append(1)
	texto.append(2)
	texto.append(3)
	writeArchive(texto)