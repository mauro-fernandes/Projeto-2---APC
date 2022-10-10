"""

lista.sort(key=lambda x: x[1])

from operator import itemgetter
configuracao = sorted(configuracao, key=itemgetter(1)) 

"""

from operator import itemgetter
import copy



configuracao = []

AREA, MESAS, CADEIRAS = 0, 1, 2
restaurante = []
AREA, MESAS_OCUP, CADEIRAS_OCUP = 0, 1, 2
ocupacao = []
tempo = 0
tempo_entrada = 0
atendimento = []
log = []
T = 0
comando = 0
texto = ''


def check_tempo():
    for i in ocupacao:
        if i[4] == 0:
            i[1]=0
            i[3]=0
        for j in restaurante: 
            if i[0] == j[0]:
                if i[2] == j[2]:
                    if i[1] == 0:
                        j[4]+=1
    return


def check_time():
    for i in ocupacao:
        if i[4] >= tempo:
            i[1]=0
            i[3]=0
    return

def temporiza(ocupacao):
    """
    checa a lista de ocupação e simula a passagem do tempo pelo decréscimo do elemento i[4]. Também restabelece a disponibilidade da mesa (elemento j[4]) na lista [restaurante]  
    """
    for i in ocupacao:   
        for j in restaurante:
            if len(i)>0:
                if i[0] == j[0]:
                    if i[2] == j[2]:
                        #print(f'tempo saida grupo de {i[3]}: {i[4]}')
                        if i[4] == 0:
                            i[1]=0
                            i[3]=0
                            if j[4] < j[1]: 
                                j[4] +=1
                            
                        elif i[4] > 0:
                                i[4] = i[4] - 1





#
def relatorio_final(restaurante, ocupacao):
    """
    (comando = '-1')
    """
    restaurante = sorted(restaurante, key=itemgetter(0,2))
    s=[]
    T = 0

    print('Restaurante fechado.')
    print('Balanco final de mesas:') 

    for i in restaurante:
        if i[0] not in s:
            s.append(i[0])

    for h in s:
        print(f'{h}:')
        for i in restaurante:
            if h[:] == i[:][0]:
                print (f' {i[1]} mesas de {i[2]} cadeiras.')

    for i in restaurante:
        if len(i)>3:
            T = T - sum(i[3])

    print(f'Um total de {T} pessoas visitaram o restaurante hoje.')
    print('Bom descanso!')
    
    return


# Colocar um grupo de pessoas em uma mesa (comando = 1)
def alocar_grupo(texto, restaurante, ocupacao):
    """
    (comando = 1)
    input(string): "Quero uma mesa para X pessoas na area Y", onde 
    'X' indica quantas pessoas tem no grupo e 
    'Y' indica qual a área o grupo quer ocupar.
    output: Captura X e Y da string e gera os dados para a lista correspondente
    """
    demanda = []
    demanda = texto.split()
    X = demanda[4]
    Y = demanda[8]
    X = int(X)
    "__índices lista ocupacao:__AREA, qte_MESAS, CADEIRAS, TAM_GRUPO, TEMPO_de_permanencia = 0, 1, 2, 3, 4"
    # registro de ocupacao e permanencia
    # qte mesas ocupadas: restaurante[i][4])

    tempo_de_permanencia = ((2*X)+2)

    check_tempo()

    for i in restaurante:    
        if (i[0] == Y):
            if X <= i[2]:
                if 1 <= i[4]:       # checagem de disponibilidade 
                    print(f'Um grupo de {X} pessoas ocupou uma mesa de {i[2]} lugares na area {Y}.')
                    #print(i)                  
                    i[4] -= 1       # "bloqueio" das mesas alocadas
                    if len(i)<4:
                        i.append([-X]) 
                    else:
                        i[3].append(-X)
                    #print(i)
                    #print(ocupacao)

                    if len(ocupacao) < 1:
                        ocupacao+=[([i[0], +1, +i[2], +X, tempo_de_permanencia])]
                    else:
                        ocupacao.append([i[0], 1, i[2], X, tempo_de_permanencia])                
                    #print(ocupacao)
                    
                    return restaurante        
               
    else:
        print('Nao foi possivel levar o grupo de clientes para uma mesa.')
        #print(ocupacao)

        return restaurante

#
def adic_remov_mesas(texto, restaurante):
    """
    Adição ou remoção de mesas (comando = 4)
    input:
    "Quero remover mais 2 mesas com 2 cadeiras cada na area S    ALAO"
    "Quero adicionar mais 3 mesas com 4 cadeiras cada na area SALAO"
    Imprime na tela a mensagem de confirmação:
    Z mesas de X cadeiras OP com sucesso na area Y.
    onde OP ∈{adicionadas,removidas}, Z é a quantidade de mesas a serem adicionadas, X é a quantidade de cadeiras de cada mesa, e Y é a área em que as mesas foram adicionadas/removidas
    ***Particularidades do comando***
    Assuma que nunca serão adicionadas mesas em áreas não existentes, nem que serão removidas mesas que estão ocupadas ou que não existem!!!!!!!
    """
    s = texto.split()
    OP, Z, X, Y = s[1], s[3], s[6], s[11]
    X, Z = int(X), int(Z)

    if OP == 'adicionar':
        for i in restaurante:       
            if i[0] == Y:
                if i[2] == X:
                    i[1] += Z
                    i[4] += 1 
                    OP = 'adicionadas'
                    break
        else:
            restaurante.append([Y, Z, X, [], Z])
            OP = 'adicionadas'
            

    elif OP == 'remover':
        i[1] -= Z
        if i[4]>1:
            i[4] -= 1
        OP = 'removidas'               

    print(f'{Z} mesas de {X} cadeiras {OP} com sucesso na area {Y}.')

    return restaurante



#   Consulta de mesas (comando = 2)

def consulta_mesas(restaurante, ocupacao):
    """
    Consulta de mesas (comando = 2)
    Imprime como saída uma lista com cada área, em ordem alfabética, com o respectivo número de mesas ocupadas de um total de mesas, no seguinte formato:
    onde A é a área existente, M é a quantidade de mesas ocupadas na área e T é a quantidade de mesas totais da área.
    """
    restaurante = sorted(restaurante, key=itemgetter(0))
    s=[]
        
    for i in restaurante:
        if i[0] not in s:
            s.append(i[0])
    
    Mesas_ocupadas = 0
    for h in s:
        print(f'{h}: ', end = '')
        
        Total_mesas = 0
        for i in restaurante:
            if i[0] == h:
                Total_mesas += i[:][1]
        
            Mesas_ocupadas = 0
            for j in ocupacao:
                if h == j[0]:                    
                    Mesas_ocupadas += j[1]
            
        print (f'({Mesas_ocupadas} de {Total_mesas} mesas)')
    
    return
    




# Consulta de lotação (comando = 3)
def consulta_lotacao(restaurante, ocupacao):
    """
    Imprime como saída uma lista com cada área, em ordem alfabética, com a respectiva lotação atual e capacidade total, no seguinte formato:
    A1: (C1 de T1 pessoas)
    A2: (C2 de T2 pessoas)
    A3: (C3 de T3 pessoas)
    .
    .
    .
    An: (Cn de Tn pessoas)
    onde A é a área existente, C é a quantidade de cadeiras ocupadas na área e T é a quantidade de cadeiras totais da área.

    """
    restaurante = sorted(restaurante, key=itemgetter(0))
    s=[]
        
    for i in restaurante:
        if i[0] not in s:
            s.append(i[0])

    

    y = 0
    x = 0
    
    cadeiras_ocupadas = 0
    
    for h in s:
        print(f'{h}: ', end = '')
        
        y = []
        for i in restaurante:
            if h[:] == i[:][0]:
                x = i[1]*i[2]
                y.append(x)
        
        
        cadeiras_ocupadas = 0
        for j in ocupacao:
            if h[:] == j[:][0]:                    
                cadeiras_ocupadas += j[3]
            
        print (f'({cadeiras_ocupadas} de {sum(y)} pessoas)')

    return






#########################
## Início do Programa: ##
#########################


entrada = input()

if entrada == ('--CONFIGURACAO'):
    

    while True:

        entrada = input()
        
        '''
        if entrada == '-1':
            restaurante = configuracao
            relatorio_final(restaurante, atendimento)
            break
        '''
        if entrada != ('--ATENDIMENTO'):  # Cria a lista com a configuração das areas, mesas e cadeiras
            #config_rest()

            a, m, c = entrada.split()
            m, c = int(m), int(c)
            d = m
            configuracao.append([a, m, c, [], d])
            restaurante = copy.deepcopy(configuracao)

                        

        elif entrada == ('--ATENDIMENTO'):

            tempo = 0

            while True:

                entrada_atend = input()
                
                
                tempo += 1

                if entrada_atend == ('1'):  # alocar grupo
                    texto = input()
                    atendimento.append([1, texto])
                    alocar_grupo(texto, restaurante, ocupacao)
                    temporiza(ocupacao)                    
                
                if entrada_atend == ('4'): # adic ou remoção de mesas
                    temporiza(ocupacao)
                    texto = input()
                    atendimento.append([4, texto])
                    adic_remov_mesas(texto, restaurante)
                    

                if entrada_atend == ('2'):
                    temporiza(ocupacao)
                    consulta_mesas(restaurante, ocupacao)
                    atendimento.append([entrada_atend])

                    
                if entrada_atend == ('3'):
                    temporiza(ocupacao)
                    atendimento.append([entrada_atend])
                    consulta_lotacao(restaurante, ocupacao)
                                        

                if entrada_atend == '-1':  # Relatório Final
                    atendimento.append([entrada_atend])
                    relatorio_final(restaurante, ocupacao)
                    break        
                
            break

        else:
            print('saida inesperada')
            break



#print('Config', configuracao)
#print('Atend', atendimento)
#print('Rest', restaurante)


'''
--CONFIGURACAO
SALAO 1 3
SALAO 2 4
SALAO 1 8
VARANDA 2 2
VARANDA 1 4
--ATENDIMENTO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
-1



--CONFIGURACAO
SALAO 4 4
--ATENDIMENTO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 4 pessoas na area SALAO
2
2
2
2
2
2
2
2
2
2
2
2
-1


--CONFIGURACAO
SALAO 1 2
SALAO 2 3
SALAO 3 4
SALAO 4 5
SALAO 1 10
VARANDA 1 9
VARANDA 9 1
EVENTOS 10 10
NAO-FUMANTES 1 1
--ATENDIMENTO
1
Quero uma mesa para 2 pessoas na area SALAO
1
Quero uma mesa para 2 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 3 pessoas na area SALAO
1
Quero uma mesa para 13 pessoas na area SALAO
2
3
4
Quero adicionar mais 1 mesas com 15 cadeiras cada na area SALAO
1
Quero uma mesa para 13 pessoas na area SALAO
2
3
-1
'''