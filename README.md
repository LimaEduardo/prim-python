# Prim paralelo

Esta é uma implementação do algoritmo de prim paralelizado

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Requisitos

É necessário ter instalado python3, dot, graphviz e mpi4py


## Executando os exemplos

Para a execução de um teste qualquer utilize o seguinte comando:

```
$ mpiexec -n <numero-processadores> python3 main.py <nome-arquivo-teste>
```
Como resultado dessa execução será obtido uma matriz de adjacência impressa em um arquivo de nome "saida-mat.txt"
Caso deseje a geração de uma imagem no formato png de um grafo que representa a matriz, basta descomentar a linha 230 do arquivo main.py. O arquivo png gerado terá o nome de saida.png

Para execução dos testes menores utilize o seguinte comando:

```
$ python3 testadorMenores.py
```

Caso deseje executar testes com outros arquivos, basta modificar a linha 3 do arquivo testadorMenores e substituir o diretório dos arquivos pelo dos testes a serem executados.

Para calcular a média dos testes realizados execute o seguinte comando (é necessário ter executado antes o testadorMenores.py):

```
$ python3 calculaMediaTestesMenores.py
```

Para calcular a média dos testes realizados execute o seguinte comando (é necessário ter executado antes o calculaMediaTesteMenores.py):


```
$ python3 calculaSpeedupEficienciaMediaMenores.py
```

O resultado deste último comando será um arquivo contendo (separados por tabulação):

nome do teste, número de processadores utilizados, tempo de execução, speedup, eficiência

para cada um dos testes realizados.
