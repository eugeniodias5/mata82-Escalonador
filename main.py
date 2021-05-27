from copy import deepcopy
import matplotlib.pyplot as plt
import random

algoritmo_escalonamento = 'EDF'
tempo_atual = 0
#Tempo máximo de execução do processador
tempo_maximo = 500

class Processador:
    def __init__(self):
        self.fila = Fila_Processador()
        self.tarefa_atual = None
        self.tempo_execucao = 0

    def insere_tarefa_atual(self, tarefa):            
        self.tarefa_atual = tarefa

    def insere_tarefa(self, tarefa):
        if tarefa.instante_inicio == 0:
            #Se a tarefa ainda não foi iniciada, setamos o instante de início
            tarefa.instante_inicio = self.tempo_execucao

        if self.tarefa_atual is not None:
            #Se a tarefa que chegou é menos prioritária, irá para a fila do processador
            if tarefa.prioridade >= self.tarefa_atual.prioridade:
                self.fila.insert(tarefa)
            else:
                self.fila.insert(self.tarefa_atual)
                self.insere_tarefa_atual(tarefa) 
            return

        if not self.fila.isEmpty():
            #Se a tarefa que chegou é menos prioritáriaque a tarefa aguardando na fila do processador, irá para a fila
            if tarefa.prioridade > self.fila.tarefas[0].prioridade:
                self.insere_tarefa_atual(self.fila.pop()) 
                self.fila.insert(tarefa)
                return
        
        self.insere_tarefa_atual(tarefa) 

    def executa(self):
        self.tempo_execucao += 1
        if self.tarefa_atual != None:
            self.tarefa_atual.incrementa_tempo_executado()
            print(self.tempo_execucao, self.tarefa_atual.instante_inicio, self.tarefa_atual.intervalo)
            if self.tempo_execucao > (self.tarefa_atual.instante_inicio + self.tarefa_atual.intervalo):
                #O sistema não é escalonável
                return False

            if self.tarefa_atual.tempo_executado == self.tarefa_atual.tempo_execucao:
                #Verificando se existe tarefa na fila para ser executada
                if not self.fila.isEmpty():
                    self.insere_tarefa_atual(self.fila.pop())
                else: self.insere_tarefa_atual(None)

        return True

class Fila_Processador:
    def __init__(self):
        self.tarefas = []

    def isEmpty(self):
        if len(self.tarefas) == 0:
            return True
        
        return False

    def pop(self):
        tarefa = self.tarefas[0]
        self.tarefas = self.tarefas[1:(len(self.tarefas) - 1)]
        return tarefa

    def insert(self, tarefa):
        self.tarefas.append(tarefa)
        self.tarefas.sort(key=lambda tarefa : tarefa.prioridade)
        return True

class Tarefa:
    def __init__(self, liberacao, tempo_execucao, intervalo):
        self.liberacao = liberacao
        self.tempo_execucao = tempo_execucao
        self.intervalo = intervalo
        self.prioridade = None
        self.tempo_executado = 0
        #Instante que o processador começou a executar a tarefa atual
        self.instante_inicio = 0
    
    def set_prioridade(self, prioridade):
        self.prioridade = prioridade

    def incrementa_tempo_executado(self):
        self.tempo_executado += 1

class Memoria:
    def __init__(self, tarefas):
        self.tarefas = tarefas

    def retorna_tarefas(self, instante):
        tarefas = []
        for tarefa in self.tarefas:
            if tarefa.liberacao == instante or (float(instante - tarefa.liberacao) % float(tarefa.intervalo)) == 0:
                tarefas.append(deepcopy(tarefa))
        return tarefas

#Classe que irá plotar o diagrama de Gantt caso o sistema seja escalonável
class Gantt_Plotter:
    def __init__(self, n, tempo_maximo, tarefas):
        cores = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange']
        self.n = n
        self.tempo_maximo = tempo_maximo
        self.tarefa_cor = {}
        for tarefa in tarefas:
            self.tarefa_cor[tarefa.prioridade] = random.choice(cores)

        #Definindo configurações iniciais do diagrama
        fig, self.gnt = plt.subplots()
        self.gnt.set_ylim(0, (10*n))  
        self.gnt.set_xlim(0, tempo_maximo)
        
        self.gnt.set_xlabel('Tempo')
        self.gnt.set_ylabel('Tarefa')

        self.gnt.grid(True)

    def desenha_tarefa(self, tarefa, instante):
        self.gnt.broken_barh([(instante, 1)], (10*tarefa.prioridade, 10), facecolors = (self.tarefa_cor[tarefa.prioridade]))

    def salva_diagrama(self):
        plt.savefig("Gantt_Diagram.png")

#Método que recebe a entrada de input.in
def recebe_entrada():
    n = int(input())
    tarefas = []
    tarefa = ''
    parentese_aberto = False
    #Pegando dados do arquivo input.in
    for letra in input():
        if letra == '(':
            parentese_aberto = True
        elif letra == ')':
            parentese_aberto = False
            tarefa = tarefa.split(',')
            tarefas.append(Tarefa(int(tarefa[0]), int(tarefa[1]), int(tarefa[2])))
            tarefa = ''
        else:
            if parentese_aberto:
                tarefa += letra
    return n, tarefas

def ordenar_rm(tarefas):
    tarefas.sort(key=lambda tarefa: tarefa.intervalo)
    for index, tarefa in enumerate(tarefas): tarefa.set_prioridade(index)
    return tarefas

def ordenar_edf(tarefas):
    tarefas.sort(key=lambda tarefa: (tarefa.liberacao + tarefa.intervalo))
    for index, tarefa in enumerate(tarefas): tarefa.set_prioridade(index)
    return tarefas



if __name__ == '__main__':
    print('Recebendo tarefas de entrada...')
    n, tarefas = recebe_entrada()
    
    if algoritmo_escalonamento == 'RM':
        tarefas = ordenar_rm(tarefas)
    else:
        tarefas = ordenar_edf(tarefas)

    processador = Processador()
    memoria = Memoria(tarefas)
    #Diagrama de Gantt será plotado caso as tarefas sejam escalonáveis
    gantt_plotter = Gantt_Plotter(n, tempo_maximo, tarefas)
    escalonavel = True

    for tarefa in tarefas:
        print(tarefa.instante_inicio)

    for instante in range(0, tempo_maximo):
        print(f"Instante {instante}: Buscando tarefas na memória.")
        tarefas_atuais = []
        tarefas_atuais = memoria.retorna_tarefas(instante)
        
        for tarefa in tarefas_atuais:
            print(f"Encontrada Tarefa com prioridade {tarefa.prioridade}")
            processador.insere_tarefa(tarefa)

        if processador.tarefa_atual is not None:
            print(f"Processador executando tarefa com prioridade {processador.tarefa_atual.prioridade}")
            gantt_plotter.desenha_tarefa(processador.tarefa_atual, instante)
        else:
            print(f"Processador está ocioso... Sem tarefas para executar")

        if not processador.executa():
            escalonavel = False
            break

    if escalonavel:
        print("O sistema é escalonável. Gerando diagrama de Gantt...")
        gantt_plotter.salva_diagrama()
    else:
        print("O sistema não é escalonável")
