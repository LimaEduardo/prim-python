import sys
import os

from leitorArquivo import LeitorArquivo
from mpi4py import MPI
from graphviz import Graph

def achaMenorLista(lista, verticesDivisao, verticesAGM):
    menor = None
    posicao = None
    for i in range(len(lista)):
        try:
            verticesAGM[verticesDivisao[i]]
        except KeyError:
            if(menor == None):
                menor = lista[i]
                posicao = i
            elif(lista[i] != None and menor != None and lista[i] < menor):
                menor = lista[i]
                posicao = i
        
        

    return (menor, posicao)


def achaMenorMatriz(subGrafo, verticesDivisao, verticesAGM):
    menor = None
    menorI = None
    menorJ = None

    for i in verticesAGM:
        linha = subGrafo[i]
        m, posicao = achaMenorLista(linha, verticesDivisao, verticesAGM)
        if(menor == None):
            menor = m
            menorI = i
            menorJ = posicao
        elif(m != None and m < menor):
            menor = m
            menorI = i
            menorJ = posicao

    return (menor, menorI, menorJ)


def divideGrafo(vertices, matrizAdjacencia):
    print("Divide")
    divisaoMatrizes = {}

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    restoChunks = int(len(vertices) % size)
    
    tamanho = len(vertices)
    posicaoInicial = 0
    posicaoFinal = 0
    posicaoVerticeInicial = 0
    posicaoVerticeFinal = 0
    for i in range(size):
        print("Processador: " + str(i))
        numeroColunas = int(len(vertices)/size)

        if (i < restoChunks):
            numeroColunas += 1

        divisao = []
        
        posicaoFinal += numeroColunas

        arestasDivisao = []
        for j in range(tamanho):
            # print("Cria divisao nula: " + str(j))
            divisao.append([])
            for k in range(posicaoInicial, posicaoFinal):
                # print("Append coluna: " + str(k))
                divisao[j].append(matrizAdjacencia[j][k])
        
        posicaoInicial = posicaoFinal

        posicaoVerticeFinal += numeroColunas
        divisaoMatrizes[i] = {'matriz' : divisao, 'vertices' : vertices[posicaoVerticeInicial:posicaoVerticeFinal]}
        posicaoVerticeInicial = posicaoVerticeFinal

        print("Termina processador: " + str(i))

    
    return divisaoMatrizes


def gerarArvoreInicial(vertices):
    matriz = []
    for i in range(len(vertices)):
        matriz.append([])
        for j in range(len(vertices)):
            matriz[i].append(None)
    conjuntoVertices = {}
    conjuntoVertices[0] = 0

    agm = {'matriz' : matriz, 'vertices' : conjuntoVertices}

    return agm

def achaMenorGlobal(menores):
    menorPeso , posI, posJ = None,None, None
    for menor in menores:
        if menorPeso == None:
            menorPeso, posI, posJ = menor[0], menor[1], menor[2]
        if menor[0] != None:
            if menor[0] < menorPeso:
                menorPeso, posI, posJ = menor[0], menor[1], menor[2]
    return (menorPeso, posI, posJ)


def escreveMatrizArquivo(prefixoArquivoSaida, vertices, matriz):
    saida = "\t"
    for i in range(len(matriz)):
        saida += str(i) + "\t"
    saida += '\n'
    for i in range(len(matriz)):
        saida += str(i) + "\t"
        for j in range(len(matriz)):
            if(agm['matriz'][i][j] == None):
                saida += "-"
            else:
                saida += "{0:.2f}".format(agm['matriz'][i][j])
            saida += "\t"
        saida += "\n"
    
    with open(prefixoArquivoSaida + "-mat.txt", "w") as arquivo:
        arquivo.write(saida)

    print(saida)
    

def exportaGraphviz(agm):
    dot = Graph()
    vertices = agm['vertices']
    matriz = agm['matriz']

    for i in range(len(matriz)):
        dot.node(str(i))

    for i in range(len(vertices)):
        for j in range(i):
            if(matriz[i][j] != None):
                dot.edge(str(i), str(j), "{0:.2f}".format(matriz[i][j]))

    with open("saida.dot", "w") as arquivo:
        arquivo.write(dot.source)
    print(dot.source)

    os.system("dot -Tpng saida.dot > saida.png")

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        nomeArquivoEntrada = sys.argv[1]
        if nomeArquivoEntrada == "":
            print("Informa o nome do arquivo")
            sys.exit()

        infos = LeitorArquivo(nomeArquivoEntrada).leArquivo()
        vertices = infos['vertices']
        
        matriz = infos['matriz']

        divisoes = divideGrafo(vertices, matriz)
        print("terminou divisões")
        
        for i in range(1, size):
            print("Enviando para o processador " + str(i))
            comm.send(divisoes[i], dest=i, tag=0)
            print("Terminou envio para o processador " + str(i))
        
        divisao = divisoes[0]
        print("Terminou envios")
    else:
        divisao = comm.recv(source=0, tag=0)

    print("Recebeu: " + str(rank))
    tamanho = 1
    
    if rank == 0:
        agm = gerarArvoreInicial(vertices)
    else:
        agm = {}
        agm['vertices'] = None

    sai = False
    while (not sai):
        # print("Paralelo")
        verticesAGM = comm.bcast(agm['vertices'], root=0)

        
        menor, posI, posJ = achaMenorMatriz(divisao['matriz'], divisao['vertices'], verticesAGM)
        pos = None

        if (posJ != None):
            pos = divisao['vertices'][posJ]

        recvbuf = comm.gather([menor, posI, pos], root=0)

        if (rank == 0):
            menorGlobal = achaMenorGlobal(recvbuf)
            agm['matriz'][menorGlobal[1]][menorGlobal[2]] = menorGlobal[0]
            agm['matriz'][menorGlobal[2]][menorGlobal[1]] = menorGlobal[0]
            agm['vertices'][menorGlobal[1]] = menorGlobal[1]
            agm['vertices'][menorGlobal[2]] = menorGlobal[2]
            print("INSERINDO", len(agm['vertices']))
            
            if len(agm['vertices']) >= len(vertices):
                sai = True
        
        sai = comm.bcast(sai, root=0)  

    if rank == 0:
        prefixoArquivoSaida = "saida"
        escreveMatrizArquivo(prefixoArquivoSaida, agm['vertices'], agm['matriz'])
        exportaGraphviz(agm)

    MPI.Finalize()
        

        
