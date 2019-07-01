Obs: Possui alguns erros gramaticais/(de sentença) no texto abaixo. Ainda não houve a a oportunidade de arruma-los.

## Algoritmo genético para alocação de revisores de artigos

#### Trabalho realizado por:

- William Felipe Tsubota 
- Wesley Souza Campagna 
- Alberto Benites 
- Gabriel Chiba Miyahira 

### Considerações iniciais

- O nome do repositório `work_ai____austroloptekus_apharis` foi para não permitir a busca do mesmo por outros alunos da classe que viessem a agir de modo errado.

- O trabalho possuía duas etapas. A primeira era uma busca A* para o problema do `Resta Um`, onde havia a necessidade de construir uma heurística que pudesse chegar na conclusão o mais breve possível, além da validação de uma função de avaliação e de custo. A segunda é este trabalho. Todos os membros do grupo definiram em reuniões quais seriam as heurísticas e as funções para cada uma das etapas. Porém o desenvolvimento foi dividido em duas duplas: para a primeira etapa desenvolveram Gabriel Chiba e Alberto Benites e para a segunda Wesley Campagna e William Tsubota - razão de existir apenas commits  destes dois alunos. Vale ressaltar que todos participaram das duas etapas de planejamento.  

### Objetivo

O objetivo de criação deste trabalho foi de resolver e desenvolver um problema elaborado  pelo professor dos alunos, Professor Doutor Bruno Nogueira, quando destes, estudantes da matéria de inteligência artificial pela FACOM (Faculdade de Computação) - UFMS (Universidade Federal de Mato Grosso do Sul).
O algoritmo desenvolvido serviu para o aprimoramento do entendimento de algoritmos genéticos, uma parte importante dentro da Inteligência Artificial. Havia como objetivo o desenvolvimento do algoritmo baseado em roleta respeitando os processos de `seleção`, `crossover` e `mutação`, da criação de gráficos utilizando da biblioteca [matplot](https://matplotlib.org/) e do desáfio de criação de uma função de avaliação, uma heurística válida e um método de convergência para parada do algoritmo. Para tal foi exigida a codificação respeitando algumas configurações para atingir a meta que era a **alocação de revisores de artigos respeitando sua disponibilidade com a busca de melhor parâmetro de configuração**.

### O problema

A ideia vem do problema de alocação de artigos para revisores. Existe muitos tipos de artigos que são publicados, como também, muitos revisores com conhecimentos em torno da área de sua pesquisa/estudo.
Cada revisor então declara qual sua aptidão com cada artigo disponivel para correção e a sua disponibilidade de correção (limite máximo de artigos que deseja corrigir). Vale ressaltar que esta parte o algoritmo não faz e pode inclusive ser base para outro projeto. O algoritmo então tenta solucionar o problema, que é um problema clássico de alocação, buscando uma configuração de saída válida e que tente maximizar a satisfação de artigo entregue para o revisor que tenha a melhor aptidão e respeitando a disponibilidade dita por este.

### O Algoritmo

O algoritmo já recebe pronta uma matriz `n x m + 1` representando _revisor x artigo_, respectivamente,  e _1_ como uma coluna que representa a disponibilidade de correção do revisor. Essa matriz deve ser gerada por outro algoritmo ou a mão, não existe representado aqui como dito anteriormente e passado seu caminho como parâmetro de entrada desse algoritmo.

Existe já [aqui](https://github.com/Wesleycampagna/work_ai____austroloptekus_apharis/blob/master/inputpath) um arquivo que demostra essa matriz. Note que o nome do arquivo é _'inputpath'_, foi usado dessa forma para que qndo executado pela primeira vez observe-se que um parametro descrito como `inputpath` em [AlocacaoArigos](https://github.com/Wesleycampagna/work_ai____austroloptekus_apharis/blob/master/alocacaoArtigos.py) designa o arquivo padrão de entrada mas deve receber o `caminho + nome do arquivo`.

Sabendo dos parâmetros é gerado a _heurística_ que melhora a solução do algoritmo, esta também é usada para análise da convergência de tal. A _heurística_ nada mais é que a soma das melhores aptidões para cada artigo sem considerar efetivamente a disponibilidade do revisor.

A população é gerada randomicamente com um total de 6 indivíduos - quantidade de indivíduos foi escolhida sem uma definição - esses valores são convertidos em bits respeitando um _tetolog_ que preenche a quantidade de bits para representar um número inteiro. se 8 = log2 de 8 = 3 → tetolog = 3. se 7 pega-se o teto (8) e calcula-se o log → _tetolog = 3_.

A função de avaliação acontece por cálculo do `fitness` obtido, para cada indivíduo dentro de uma população dada uma geração calcula-se por meio de soma a afinidade relacionada ao revisor alocado em cada posição desse indivíduo, essa posição é relacionada diretamente ao artigo de interesse. Por punição/penalidade onde em cada geração analisada de indivíduos da população verifica-se se algum dos revisores alocados da maneira que foi gerado fere a sua disponibilidade relacionada.

A função de convergência do algoritmo, e por si só o critério de parada, é verificar o melhor indivíduo de 10 gerações atuais em relação ao melhor indivíduo das 10 gerações anteriores, caso esses dois indivíduos tenham valores próximos e um deles for próximo do valor heurístico, afirma-se para exemplificação que ele está convergindo.

Existe então o algoritmo genético que utiliza de 10 baterias de testes e a idéia de **elitismo** - um indivíduo obtido na primeira bateria/etapa/geração é o melhor até que outro prove ser melhor. Logo, procura-se o melhor indivíduo nas 10 baterias/repetições para ser gravado no arquivo de saída. Cada bateria é a execução única do algoritmo genético.

Além do processo acima existe a busca em cada uma das repetições pelo melhor indivíduo que aparecerá conforme convergência ou o melhor no limiar de **maxgen** gerações.

Com isso gera-se os gráficos descritos em _Dados gerados_ e a resposta anteriormente descrita.

### Como executar

para ver como o mesmo funciona, certifique-se de possuir [python 3.x ou maior](https://www.python.org/downloads/) e algumas de suas bibliotecas: [matplotlib](https://matplotlib.org/users/installing.html) e [numpy](https://www.numpy.org/). Então clone o projeto para alguma pasta de interesse com o comando:

```Terminal
   git clone https://github.com/Wesleycampagna/work_ai____austroloptekus_apharis.git
```

Basta navegar até a pasta `work_ai____austroloptekus_apharis` e executar:

```Terminal
   python3 run.py
```

Os parâmetros de melhor configuração para o problema poderão ser encontrados após dentro do local atual com o nome de **`saida-genetico.txt`**.

Existe ainda a possibilidade de usar argumentos na execução do programa:

```Terminal
   python3 run.py arg1 arg2 arg3 arg4
```
Que correspondem à:

- **arg1** &#8594; `crossoverrate` float [0~1] : taxa de crossover _ou_ **inputpath** string[<path_folder_and_file_name>]: caminho para o arquivo de entrada;

A partir daqui _arg1_ é _crossoverrate_.

- **arg2** &#8594; `mutationrate` float [0~1] : taxa de mutation;
- **arg3** &#8594; `maxgen` int [1~3000(aconselhável)]: quantas gerações serão geradas;
- **arg4** &#8594;  **inputpath** string[<path_folder_and_file_name>]: caminho para o arquivo de entrada;

### Dados gerados

São ao final da execução gerados alguns itens:
- gráficos gerados na pasta `geneticFiles';
   - gráfico da média da média da população da geração nas 10 repetições do algoritmo x média do melhor indivíduo da população nas 10 repetições;
   - 10 gráficos representando cada repetição contendo a média da população da geração x valor do fitness do melhor indivíduo da população;
   - média das convergências ocorridas x convergência mais rápida.
- arquivo de saida `saida-genetico.txt` contendo a melhor configuração para o problema.

### Algumas análises finais

A função de convergência caso ela seja modificada para um limiar menor, fixo em `20%` - procurar linha **34** em [genetic](https://github.com/Wesleycampagna/work_ai____austroloptekus_apharis/blob/master/genetic.py) onde `self.__converg = (self._Genetic__heuristic_sum *`**`0.20`**`)` - , ocasiona em uma melhor análise dos dados que, consequentemente, entrega uma configuração de resposta melhor. Porém o efeito disto é que a convergência do algoritmo é mais lenta e em vezes não ocorre, ao menos para o limite de gerações do parâmetro/argumento de entrada. 

O algoritmo consegue em um tempo muito bom obter a resposta para o problema. Em uma matriz de 5 x 4 + 1 usando um computador de processamento _core i3 2.4Gz_ uma média de 2s para resolução. Não foram testados exemplos grandiosos para o caso.

Uso de divisão por números flutuantes para penalizar o fitness e consequentemente validar apenas o valor _inteiro_ obtido do fitness do indivíduo para possível resposta para o problema se mostrou eficaz e simplificou qualquer outra resolução que viria a ser complexa. Isto ocorre na  linha **35** em [genetic](https://github.com/Wesleycampagna/work_ai____austroloptekus_apharis/blob/master/genetic.py) onde 5.1 em  `self.__penalty = self._Genetic__heuristic_sum /`**`5.1`** é a penalidade flutuante, e na  linha **189** do [genetic](https://github.com/Wesleycampagna/work_ai____austroloptekus_apharis/blob/master/genetic.py) onde a verdade da comparação `if sum_individual == math.ceil(sum_individual):` é a validação para o valor _inteiro_.

Algoritmo genético por usar roleta e seleção realmente obtém melhoras graduais ao longo das gerações.

Uma mutação alta não permite melhora das populações ao decorrer das gerações, por incrível que pareça, valores acima de 0.08 (equivalentes a 8% de chance de mutação) começam a fazer o sistema de roleta perder validade, podendo não haver melhora ao longo das gerações.

