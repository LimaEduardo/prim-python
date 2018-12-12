nomeArquivo = "testeMenoresMedia.txt"
with open(nomeArquivo, "r") as arquivo:
    linhas = arquivo.read().strip().splitlines()


dict_dados = {}
for linha in linhas:
    dados = linha.split()
    dados[1] = int(dados[1])
    dados[2] = float(dados[2])
    try:
        dict_dados[dados[0]]
    except KeyError:
        dict_dados[dados[0]] = {}
    
    dict_dados[dados[0]][dados[1]] = dados[2]

saida = ""
for nome, dict_processadores in dict_dados.items():
    for num_processadores, valor in dict_processadores.items():
        saida += nome + "\t"
        saida += str(num_processadores) + "\t"
        saida += str(valor) + "\t"
        speedup = dict_processadores[1] / valor
        saida += str(speedup) + "\t"
        eficiencia = speedup / num_processadores
        saida += str(eficiencia) + "\n"

with open("testeMenoresMetricas.txt", "w") as arquivo:
    arquivo.write(saida)