import sys

if __name__ == "__main__":
  nomeArquivo = sys.argv[1]

  with open(nomeArquivo, "r") as arquivo:
    linhas = arquivo.read().splitlines()
    testes = {}
    tabelaLatex = ""
    for linha in linhas:
      linhaLimpa = linha.split('\t')
      nomeInstancia = linhaLimpa[0].replace('./test_instances/menores/','').replace('.input','')
      try:
        testes[nomeInstancia] += [linhaLimpa[1], linhaLimpa[2]]
      except KeyError:
        testes[nomeInstancia] = [linhaLimpa[1], linhaLimpa[2]]
    for chave, valor in testes.items():
      tabelaLatex += chave + " & " + "%.3f" % float(valor[1]) + " & " + "%.3f" % float(valor[3]) + " & " + "%.3f" % float(valor[5]) + "\\\ \n"
    
    with open("saidaLatex", "w") as saida:
      saida.write(tabelaLatex)