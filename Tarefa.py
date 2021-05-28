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
