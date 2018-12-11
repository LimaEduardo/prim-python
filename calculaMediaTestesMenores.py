dict_media = {}
for i in range(1, 10):
    nomeArquivo = "testeMenores" + str(i+1) + ".txt"
    with open(nomeArquivo, "r") as arquivo:
        linhas = arquivo.read().strip().splitlines()

    for linha in linhas:
        dados = linha.split()
        dados[1] = int(dados[1])
        dados[2] = float(dados[2])
        try:
            dict_media[dados[0]]
        except KeyError:
            dict_media[dados[0]] = {}
        try:
            dict_media[dados[0]][dados[1]] += dados[2]
        except KeyError:
            dict_media[dados[0]][dados[1]] = dados[2]
        

saida = ""
for nome, dict_processos in dict_media.items():
    for chave, valor in dict_processos.items():
        dict_processos[chave] = valor / 10
        saida += nome + "\t"
        saida += str(chave) + "\t"
        saida += str(dict_processos[chave]) + "\n"

nomeArquivo = "testeMenoresMedia.txt"
with open(nomeArquivo, "w") as arquivo:
    arquivo.write(saida)



