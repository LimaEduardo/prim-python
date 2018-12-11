import os
import time
files = os.popen("ls ./test_instances/menores/").read().strip().splitlines()

saida = ""
for i in range(len(files) - 1, 0, -1):

    comando = "mpiexec -n 4 python3 main.py ./test_instances/menores/" + files[i]
    print(comando)

    start_time = time.time()
    retorno = os.popen(comando).readlines()
    end_time = time.time()
    
    total_time = end_time - start_time
    
    saida += "./test_instances/menores/" + files[i] + "\t" + str(total_time) + "\n"

with open("testeMenores.txt", "w") as arquivo:
    arquivo.write(saida)