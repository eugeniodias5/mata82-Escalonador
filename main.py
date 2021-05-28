import math

from Processador import Processador
from Memoria import Memoria
from Tarefa import Tarefa
from Gantt_Plotter import Gantt_Plotter

#Método que recebe a entrada de input.in
def recebe_entrada():
    print("Bem vindo ao escalonador!")
    print("Por quantos segundos gostaria que o processador executasse?")
    tempo_maximo = int(input())

    print("Qual algoritmo gostaria de utilizar? Digite RM ou EDF. Em caso de erro de digitação, será utilizado o algoritmo RM.")
    algoritmo_escalonamento = input()
    if algoritmo_escalonamento != 'EDF':
        algoritmo_escalonamento = 'RM'

    print("Digite o número de tarefas que deseja escalonar")
    n = int(input())
    tarefas = []
    
    for tarefa in range(0, n):
        print(f"Vamos configurar a tarefa {(tarefa + 1)}...")
        print(f"Digite o instante de liberação da tarefa {(tarefa + 1)}:")
        inst_lib = int(input())
        print(f"Digite o tempo de execução da tarefa {(tarefa + 1)}:")
        temp_exec = int(input())
        print(f"Digite o intervalo máximo de execução da tarefa {(tarefa + 1)}:")
        int_max = int(input())
        tarefas.append(Tarefa(inst_lib, temp_exec, int_max))

    print("Iniciando execução...")

    return n, tarefas, tempo_maximo, algoritmo_escalonamento

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

def lub(n, tempo_ocioso, tempo_total):
    lub = round(n*(math.pow(2, (1/n)) - 1), 3)
    utilizacao = (tempo_total - tempo_ocioso)/tempo_total
    utilizacao = round(utilizacao*100, 3)

    return lub, utilizacao

if __name__ == '__main__':
    try:
        n, tarefas, tempo_maximo, algoritmo_escalonamento = recebe_entrada()
        
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
            lub, utilizacao = lub(n, processador.tempo_ocioso, processador.tempo_execucao)
            
        else:
            print("O sistema não é escalonável")
            print("Calculando LUB...")
            lub, utilizacao = lub(n, processador.tempo_ocioso, processador.tempo_execucao)
            print(f"O LUB calculado para {n} tarefas é {lub}")
            print(f"O processador teve taxa de utilização de {utilizacao}%")

            print("Calculando análise em tempo de resposta para cada tarefa...")
            tempo_resposta, tarefa = analise_tempo_resposta(tarefas, tempo_maximo)
            print(f"O sistema não é escalonável. Pois a tarefa de prioridade {tarefa.prioridade} tem deadline {tarefa.intervalo} e o tempo de resposta calculado foi {tempo_resposta}")

    except:
        print("Erro no escalonador. Tente aumentar o tempo de execução.")