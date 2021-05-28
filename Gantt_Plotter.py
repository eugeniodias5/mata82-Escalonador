import matplotlib.pyplot as plt
import random

#Classe que irá plotar o diagrama de Gantt caso o sistema seja escalonável
class Gantt_Plotter:
    def __init__(self, n, tempo_maximo, tarefas):
        cores = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange', 'tab:cyan', 'tab:gray', 'tab:brown', 'yellow', 'lime']
        self.n = n
        self.tempo_maximo = tempo_maximo
        self.tarefa_cor = {}

        yticks = []
        ytickslabels = []
        for index, tarefa in enumerate(tarefas):
            self.tarefa_cor[tarefa.prioridade] = random.choice(cores)
            yticks.append(((index + 1)*10) - 5)
            ytickslabels.append(str(index))

        #Definindo configurações iniciais do diagrama
        fig, self.gnt = plt.subplots()
        self.gnt.set_ylim(0, (10*n))  
        self.gnt.set_xlim(0, tempo_maximo)

        self.gnt.set_xlabel('Tempo')
        self.gnt.set_ylabel('Tarefa')
        
        self.gnt.set_yticks(yticks)
        self.gnt.set_yticklabels(ytickslabels)
        
        self.gnt.grid(True)

    def desenha_tarefa(self, tarefa, instante):
        self.gnt.broken_barh([(instante, 1)], (10*tarefa.prioridade, 9), facecolors = (self.tarefa_cor[tarefa.prioridade]))

    def salva_diagrama(self):
        plt.savefig("Gantt_Diagram.png")