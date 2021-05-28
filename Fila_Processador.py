class Fila_Processador:
    def __init__(self):
        self.tarefas = []

    def isEmpty(self):
        if len(self.tarefas) == 0:
            return True
        
        return False

    def pop(self):
        tarefa = self.tarefas[0]

        if len(self.tarefas) == 1:
            tarefa = self.tarefas[0]
            self.tarefas = []
            return tarefa

        self.tarefas = self.tarefas[1:]
        return tarefa

    def insert(self, tarefa):
        self.tarefas.append(tarefa)
        self.tarefas.sort(key=lambda tarefa : tarefa.prioridade)
        return True