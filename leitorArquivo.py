class LeitorArquivo:

    def __init__(self, nomeArquivo):

        self.nomeArquivo = nomeArquivo
    
    def leArquivo(self):
        with open(self.nomeArquivo, "r") as arquivo:
            linhas = arquivo.read().splitlines()
            quantidadeVertices = int(linhas[0])
            matriz = [[None] * quantidadeVertices for i in range(quantidadeVertices)]

            vs = []
            arestas = []

            for i in range(1, quantidadeVertices + 1):
                linhaVertice = linhas[i].strip().split(' ')
                vertice = int(linhaVertice[0])
                coordenadaX = float(linhaVertice[1])
                coordenadaY = float(linhaVertice[2])
                vs.append((vertice, coordenadaX, coordenadaY))
            
            quantidadeAresta = int(linhas[quantidadeVertices + 1])

            for i in range(quantidadeVertices + 2, quantidadeVertices + quantidadeAresta + 2):
                linhasAresta = linhas[i].strip().split(' ')
                v1 = vs[int(linhasAresta[0])]
                v2 = vs[int(linhasAresta[1])]
                distancia = self.calculaDistanciaEuclidiana(v1[1], v1[2], v2[1], v2[2])
                matriz[v1[0]][v2[0]] = distancia
                matriz[v2[0]][v1[0]] = distancia

            vertices = []
            for v in vs:
                vertices.append(v[0])
            
            return {'matriz': matriz, 'vertices': vertices}

    def calculaDistanciaEuclidiana(self, coordenadaX1, coordenadaY1, coordenadaX2, coordenadaY2):
        x = coordenadaX1 - coordenadaX2
        y = coordenadaY1 - coordenadaY2
        return (x*x + y*y)**(1/2)