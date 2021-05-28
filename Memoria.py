from copy import deepcopy

class Memoria:
    def __init__(self, tarefas):
        self.tarefas = tarefas

    def retorna_tarefas(self, instante):
        tarefas = []
        for tarefa in self.tarefas:
            if tarefa.liberacao == instante or (float(instante - tarefa.liberacao) % float(tarefa.intervalo)) == 0:
                tarefas.append(deepcopy(tarefa))
        return tarefas
        