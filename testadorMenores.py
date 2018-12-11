import os
import time
files = os.popen("ls ./test_instances/menores/").read().strip().splitlines()

for i in range(9, 10):
    saida = ""
    for j in range(len(files) - 1, -1, -1):
        for numProcs in [4, 2, 1]:
            comando = "mpiexec -n " + str(numProcs) + " python3 main.py ./test_instances/menores/" + files[j]
            print(comando)

            start_time = time.time()
            retorno = os.popen(comando).readlines()
            end_time = time.time()
            
            total_time = end_time - start_time
            
            saida += "./test_instances/menores/" + files[j] + "\t" + str(numProcs) + "\t" + str(total_time) + "\n"
    
    # print(saida)
    nomeArquivo = "testeMenores" + str(i+1) + ".txt"
    # print(nomeArquivo)
    with open(nomeArquivo, "w") as arquivo:
        arquivo.write(saida)