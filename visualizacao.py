matriz = [[0,0,3,4,4,1], [3,3,0,0,1,2], [4,0,0,1,0,1
], [2,2,2,3,2,2]]
lista = []
linha = len(matriz)
coluna = len(matriz[0])

for i in range(coluna - 1):
  MaiorAfinidade = -1
  for j in range(linha):
    if(matriz[j][i] > MaiorAfinidade):
      MaiorAfinidade = matriz[j][i]
  lista.append(MaiorAfinidade)
print(lista)