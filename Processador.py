from Fila_Processador import Fila_Processador

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
            if self.tempo_execucao > (self.tarefa_atual.instante_inicio + self.tarefa_atual.intervalo):
                #O sistema não é escalonável
                return False

            if self.tarefa_atual.tempo_executado == self.tarefa_atual.tempo_execucao:
                #Verificando se existe tarefa na fila para ser executada
                if not self.fila.isEmpty():
                    self.insere_tarefa_atual(self.fila.pop())
                else: self.insere_tarefa_atual(None)

        return True