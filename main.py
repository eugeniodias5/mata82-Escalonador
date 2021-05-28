import math

from Processador import Processador
from Memoria import Memoria
from Tarefa import Tarefa
from Gantt_Plotter import Gantt_Plotter

algoritmo_escalonamento = 'EDF'
tempo_atual = 0
#Tempo máximo de execução do processador
tempo_maximo = 100

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

def analise_tempo_resposta(tarefas, tempo_maximo):
    for tarefa in reversed(tarefas):
        print(f"Calculando tempo de resposta da tarefa com prioridade {tarefa.prioridade}")

        valor_iteracao_passada = tarefa.tempo_execucao

        for iteracao in range(0, tempo_maximo):
            valor_iteracao = tarefa.tempo_execucao

            for tarefa_maior_prioridade in tarefas:
                if tarefa_maior_prioridade == tarefa:
                    break
                valor_iteracao += math.ceil(valor_iteracao_passada/tarefa_maior_prioridade.intervalo)*tarefa_maior_prioridade.tempo_execucao

            if valor_iteracao == valor_iteracao_passada:
                if valor_iteracao > tarefa.intervalo:
                    #Sistema não é escalonável
                    return valor_iteracao, tarefa
                break
            valor_iteracao_passada = valor_iteracao


if __name__ == '__main__':
    try:
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
        
        if not processador.fila.isEmpty():
            escalonavel = False

        if escalonavel:
            print("O sistema é escalonável. Gerando diagrama de Gantt...")
            gantt_plotter.salva_diagrama()
        else:
            print("O sistema não é escalonável")
            print("Calculando análise em tempo de resposta para cada tarefa...")
            tempo_resposta, tarefa = analise_tempo_resposta(tarefas, tempo_maximo)
            print(f"O sistema não é escalonável. Pois a tarefa de prioridade {tarefa.prioridade} tem deadline {tarefa.intervalo} e o tempo de resposta calculado foi {tempo_resposta}")

    except:
        print("Erro no escalonador. Tente aumentar o tempo de execução.")