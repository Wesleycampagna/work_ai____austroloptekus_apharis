# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

class writer:
	
	def writeArchive(self, listaInt, file_path):
		
		arq = open(file_path, 'w')
		listaStr = list(map(str, listaInt))
		separator = ' '
		result = [separator.join(listaStr)]
		result = [r.replace(' ', ',') for r in result]
		arq.writelines(result)
		arq.close()
		pass