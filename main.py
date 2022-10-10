###########################################
#####     RESTAURANTE XANGAI          ##### #
#####         PyDiner Dash 2          #####   #
###########################################     #
#                                         #     #
#   Bem Vindo ao PyDiner Dash 2!          #     #
#                                         #     #
#   Escreva um Comando para continuar:    #     #
#   1 + atualizar mesas                   #     #
#   2 + atualizar cardapio                #     #
#   3 + atualizar estoque                 #     #
#   4 + relatorio mesas                   #     #
#   5 + relatorio cardapio                #
#   6 + relatorio estoque                 #
#   7 + fazer pedido                      #
#   8 + relatorio pedidos                 #
#   9 + fechar restaurante                #

###################################################

from operator import itemgetter

log_pedidos = []
pedidos_na = {}


def registra_pedidos(n, i):
    """
    Alimenta lista com histórico de pedidos do restaurante
    """
    log_pedidos.append([n, i])


def mesa_ocupada(n):
    """
    Atualiza a ocupação no dicionário da relacao de mesas (conf)
    """
    conf[n][1] = 'ocupada'


def atualizar_mesas(nome_arquivo):
    """
    Cada número de mesa é único no restaurante. Logo, caso seja lido algum número de mesa já existente no restaurante, deve-se atualizar esta mesa com as novas informações de área e de ocupação.
    Este comando pode:
    Inserir novas mesas no restaurante;
    Inserir novas áreas no restaurante caso seja lida alguma mesa em uma área nova;
    Atualizar informações de mesas já existentes. 
    """
    arquivo = open(nome_arquivo)

    for linha in arquivo:
        mesas = linha.strip()
        mesas = mesas.replace(', ', ',')
        mesas = mesas.split(',')
        mesas[0] = int(mesas[0])
        areas.append(mesas)

    for i in areas:
        conf[i[0]] = i[1:]

    return conf, areas


def atualizar_cardapio(nome_arquivo):
    """
    Caso seja lido um item que não exista no cardápio atual, deve-se adicioná-lo ao cardápio junto com seus respectivos ingredientes.

    Caso seja lido um item que já exista no cardápio, deve-se atualizar este item com as novas informações de ingredientes, sobrescrevendo as antigas.
    """
    arquivo = open(nome_arquivo)

    ingredientes = []
    for linha in arquivo:
        item = linha.strip()
        item = item.replace(', ', ',')
        item = item.split(',')
        ingredientes.append(item)

    for k in ingredientes:
        cardapio[k[0]] = k[1:]

    return cardapio


def atualizar_estoque(nome_arquivo):
    """
    Caso seja lido algum ingrediente que não exista no estoque, deve-se adicioná-lo ao estoque com sua respectiva quantidade.

    Caso seja lido algum ingrediente que já exista no estoque, deve-se adicioná-lo ao estoque somando sua respectiva quantidade com a quantidade já armazenada no estoque.
    """
    arquivo = open(nome_arquivo)

    dispensa = []
    for linha in arquivo:
        item = linha.strip()
        item = item.replace(', ', ',')
        item = item.split(',')
        item[1] = int(item[1])
        dispensa.append(item)

    for elem in dispensa:
        if elem[0] in estoque:
            estoque[elem[0]] += elem[1]
        else:
            estoque[elem[0]] = elem[1]

    return estoque


def relat_mesas():
    """
    Imprime a configuração de mesas do restaurante em ordem alfabética do nome da área e em ordem crescente de mesa, no seguinte formato:
    area: ai
    - mesa: m1, status: s1
    .
    - mesa: mj, status: sj
    Onde
    ax corresponde às áreas existentes no restaurante, com x ∈{1,2,...,i} , sendo i o número total de áreas;
    my corresponde às mesas existentes em cada área, com y ∈{1,2,...,j} , sendo j o número total de mesas;
    sy corresponde ao status da mesa my, ou seja, sy ∈{ocupada,livre}
    Caso alguma área esteja sem mesas, imprima a seguinte mensagem nesta área:
    area: ai
    - area sem mesas
    Caso o restaurante não tenha mesas em nenhuma área, apenas imprima a seguinte mensagem:
    - restaurante sem mesas
    """
    if conf == {}:
        print('- restaurante sem mesas')

    areas2 = sorted(areas, key=itemgetter(1))  # areas por ordem alfabetica
    lista_areas = []  # lista com nomes das áreas, somente (para iteração)
    ordenado_mesa = []  # para relatório, também
    ordenado_mesa = sorted(conf.items(), key=lambda item: item[0])

    areas_ocupadas = []

    for k in conf.values():
        areas_ocupadas.append(k[0])

    for i in areas2:  # Cria a Listagem de AREAS
        area = i[1]
        if area not in lista_areas:
            lista_areas.append(i[1])

    for l in lista_areas:
        if l not in areas_ocupadas:
            areas_vazias.append(l)
    areas_vazias.sort()

    for j in lista_areas:
        print(f'area: {j}')
        for k in ordenado_mesa:
            if j == k[1][0]:
                print(f'- mesa: {k[0]}, status: {k[1][1]}')
        if j not in areas_ocupadas:
            print('- area sem mesas')

    for v in conf.values():
        if v[0] not in lista_areas:
            print('erro >> area invalida (ADM >> verificar)')

    return lista_areas, areas_vazias, areas_ocupadas


def relat_cardapio():
    """
    mprime configuração dos itens do cardápio em ordem alfabética de nome e em ordem alfabética de ingredientes, no seguinte formato:

    item: ij 
    - ing1: q1
    .
    .
    - ingk: qk

    Onde 
    ix corresponde a um item do cardápio, com x ∈{1,2,...,j} , sendo j o número total de itens;
    ingy corresponde aos ingredientes de cada item, com y ∈{1,2,...,k} , sendo k o número total de ingredientes;
    qy corresponde a quantidade do ingrediente ingy necessária para produzir o item.
    Caso o cardápio esteja vazio, imprima a seguinte mensagem:
    - cardapio vazio
    """
    if cardapio == {}:
        print(f'- cardapio vazio')

    for item in sorted(cardapio):
        print(f'item: {item}')
        relacao = relaciona_qte_ingredientes(item)
        #chaves_na_ordem = sorted(relacao)
        chaves_na_ordem2 = sorted(relacao.items(), key=itemgetter(0))
        for elem in chaves_na_ordem2:
            print(f'- {elem[0]}: {elem[1]}')


def relat_estoque():
    """
    Imprime a relação de ingredientes do estoque em ordem alfabética, junto de suas respectivas quantidades, no seguinte formato:

ing1: qt1
.
.
.
ingk: qtk

    Onde 
    ingx correspondem aos ingredientes do estoque, com x ∈{1,2,...,k} , sendo k o número total de itens;
    qtx corresponde a quantidade do item ingx no estoque.
    """
    if estoque == {}:
        print(f'- estoque vazio')

    for ing in sorted(estoque):
        print(f'{ing}: {estoque[ing]}')


def relaciona_qte_ingredientes(item_cardapio):
    """
    Relaciona os ingredientes necessários para o preparo do item do cardápio (em forma dicionário).
    """
    ingredientes = cardapio[item_cardapio]

    relacao = {}
    for i in ingredientes:
        relacao[i] = relacao.get(i, 0) + relacao.get(i, 1)

    return relacao


def falta_ingredientes(i):
    """
    Retorna True se a qtde. ingredientes necessários para o preparo do item for insuficiente
    """
    ingr_necessarios = relaciona_qte_ingredientes(i)

    for i in ingr_necessarios:
        if i not in estoque:
            return True
        if estoque[i] - ingr_necessarios[i] < 0:
            return True
    return False


def refresh_estoque(i):
    """
    Atualiza o dicionário do estoque quando o pedido é feito com sucesso.
    ***ATENÇÃO***
    Ao realizar um pedido com sucesso, caso este pedido esgote algum ingrediente do estoque, deve-se deletar este ingrediente do estoque ao invés de deixá-lo zerado.
    
    """
    usados = relaciona_qte_ingredientes(i)
    for ingred in usados:
        if estoque[ingred] == usados[ingred]:
            del (estoque[ingred])
        else:
            estoque[ingred] -= usados[ingred]


def fazer_pedido(n, i):
    """
    n, i Onde:
    n é um número inteiro, que indica o número da mesa que fez o pedido; 
    i  é uma string, que indica o item do cardápio que foi pedido.
    Faça as verificações de erro nesta ordem:
    1 - Mesa inexistente
    Caso a mesa não exista no restaurante, imprima a seguinte mensagem de erro:
    erro >> mesa n inexistente
    Onde n é o número da mesa escrito no pedido.
    2 - Mesa desocupada
    Caso a mesa não esteja ocupada, imprima a seguinte mensagem de erro:
    erro >> mesa n desocupada
    Onde n é o número da mesa escrito no pedido.
    3 - Item inexistente
    Caso o item não exista no cardápio, imprima a seguinte mensagem de erro:
    erro >> item i nao existe no cardapio
    Onde i é o item do cardápio escrito no pedido.
    4 - Ingredientes insuficientes
    Caso falte ingredientes para produzir item, imprima a seguinte  mensagem de erro:
    erro >> ingredientes insuficientes para produzir o item i
    Onde i é o item do cardápio escrito no pedido.
    Deve ser impressa no máximo uma mensagem de erro.
    Caso passe em todas as validações, imprima a seguinte mensagem de  sucesso:
    sucesso >> pedido realizado: item i para mesa n
    Onde n indica o número da mesa que fez o pedido e i indica o item do cardápio que foi pedido.
    ***PARTICULARIDADES DO COMANDO***
    Ao realizar um pedido válido deve-se também executar as seguintes  ações:
    Atualizar o registro de pedidos dessa mesa
    -Atualizar o histórico de pedidos do restaurante
    Remover do estoque os ingredientes e suas respectivas quantidades que foram utilizados no preparo do pedido
    """
    if n not in conf:
        erro('mesa ', n, ' inexistente')

    elif conf[n][1] == 'livre':
        erro('mesa ', n, ' desocupada')

    elif i not in cardapio:
        erro('item ', i, ' nao existe no cardapio')

    elif falta_ingredientes(i):
        erro('ingredientes insuficientes para produzir o item ', i, '')

    else:
        print(f'sucesso >> pedido realizado: item {i} para mesa {n}')
        registra_pedidos(n, i)
        mesa_ocupada(n)
        refresh_estoque(i)


def relatorio_pedidos():
    """
    O seu programa também deve gerar relatório de pedidos de cada mesa do restaurante.
    Imprime os pedidos feitos pelo restaurante em ordem crescente de número de mesa e em ordem alfabética do nome dos itens pedidos, no seguinte formato:

mesa: mj
- i1
.
.
- ik
    Onde:
    mx corresponde ao número das mesas existentes, com x ∈{1,2,...,j} , sendo j o número total de mesas
    iy corresponde aos itens pedidos por cada mesa, com y ∈{1,2,...,k} , sendo k o número total de pedidos feitos por uma mesa

    Caso nenhum pedido tenha sido feito, apenas imprima a seguinte mensagem:
    - nenhum pedido foi realizado
    """
    pedidos_na = {}

    if log_pedidos == []:
        print('- nenhum pedido foi realizado')
    else:

        for p in sorted(log_pedidos, key=lambda item: item[0]):
            mesa = p[0]
            item = p[1]
            if mesa in pedidos_na:
                pedidos_na[mesa].append(item)
            else:
                pedidos_na[mesa] = [item]

        for c, v in pedidos_na.items():
            print(f'mesa: {c}')
            for i in v:
                print(f'- {i}')
        '''for mesa in sorted(conf):
            for elem in sorted(log_pedidos, key = lambda item: item[1]):
                if elem[0] == mesa:
                    print(f'- {elem[1]}')'''

    return pedidos_na


def fechar():
    """
    Imprima o histórico de pedidos do restaurante em ordem cronológica, ou seja, na ordem em que foram pedidos, no seguinte formato:

1. mesa m1 pediu i1
2. mesa m2 pediu i2
.
.
.
n. mesa mj pediu ik
Onde m são as mesas, e p são os pedidos que cada mesa fez.


Caso não tenha sido feito nenhum pedido no restaurante, imprima a seguinte mensagem:
- historico vazio
    """
    if log_pedidos == []:
        print('- historico vazio')

    for i in range(len(log_pedidos)):
        print(f'{i+1}. mesa {log_pedidos[i][0]} pediu {log_pedidos[i][1]}')

    print('=> restaurante fechado')
    exit = True

    return exit


def erro(s1, s2, s3):
    """
    Imprime a mensagem como erro
    """
    print(f'erro >> {s1}{s2}{s3}')


####  %%%%%%%%%%%%%%%%%%%%  ####
####   INICIO DO PROGRAMA   ####
####  %%%%%%%%%%%%%%%%%%%%  ####
# 1   + atualizar mesas        #
# 2   + atualizar cardapio     #
# 3   + atualizar estoque      #
# 4   + relatorio mesas        #
# 5   + relatorio cardapio     #
# 6   + relatorio estoque      #
# 7   + fazer pedido           #
# 8   + relatorio pedidos      #
# 9   + fechar restaurante     #
################################

print('=> restaurante aberto')

exit = False
conf = {}
estoque = {}
cardapio = {}
areas = []
a_ocup = []
areas_vazias = []

while True:

    if exit == True:
        break
    else:
        comando = input().strip()

    while True:

        if comando == '+ atualizar mesas':
            nome_arquivo = input()
            conf, areas = atualizar_mesas(nome_arquivo)
            break

        elif comando == '+ atualizar cardapio':
            nome_arquivo = input()
            cardapio = atualizar_cardapio(nome_arquivo)
            break

        elif comando == '+ atualizar estoque':
            nome_arquivo = input()
            estoque = atualizar_estoque(nome_arquivo)
            break

        elif comando == '+ relatorio mesas':
            lista_areas, areas_vazias, a_ocup = relat_mesas()
            break

        elif comando == '+ relatorio cardapio':
            relat_cardapio()
            break

        elif comando == '+ relatorio estoque':
            relat_estoque()
            break

        elif comando == '+ fazer pedido':
            n, i = input().split(', ')  # num mesa; item cardapio
            n = int(n)
            fazer_pedido(n, i)
            break

        elif comando == '+ relatorio pedidos':
            rel = relatorio_pedidos()
            break

        elif comando == '+ fechar restaurante':
            exit = fechar()
            break

        else:
            erro('comando inexistente', '', '')
            break
