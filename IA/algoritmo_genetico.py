import random
import matplotlib.pyplot as plt

# população inicial do problema
itens_disponiveis = [ 
    { 'peso': 3, 'valor': 1},
    { 'peso': 8, 'valor': 3},
    { 'peso': 12, 'valor': 1},
    { 'peso': 2, 'valor': 8},
    { 'peso': 8, 'valor': 9},
    { 'peso': 4, 'valor': 3},
    { 'peso': 4, 'valor': 2},
    { 'peso': 5, 'valor': 8},
    { 'peso': 1, 'valor': 5},
    { 'peso': 1, 'valor': 1},
    { 'peso': 8, 'valor': 1},
    { 'peso': 6, 'valor': 6},
    { 'peso': 4, 'valor': 3},
    { 'peso': 3, 'valor': 2},
    { 'peso': 3, 'valor': 5},
    { 'peso': 5, 'valor': 2},
    { 'peso': 7, 'valor': 3},
    { 'peso': 3, 'valor': 8},
    { 'peso': 5, 'valor': 9},
    { 'peso': 7, 'valor': 3},
    { 'peso': 4, 'valor': 2},
    { 'peso': 3, 'valor': 4},
    { 'peso': 7, 'valor': 5},
    { 'peso': 2, 'valor': 4},
    { 'peso': 3, 'valor': 3},
    { 'peso': 5, 'valor': 1},
    { 'peso': 4, 'valor': 3},
    { 'peso': 3, 'valor': 2},
    { 'peso': 7, 'valor': 14},
    { 'peso': 19, 'valor': 32},
    { 'peso': 20, 'valor': 20},
    { 'peso': 21, 'valor': 19},
    { 'peso': 11, 'valor': 15},
    { 'peso': 24, 'valor': 37},
    { 'peso': 13, 'valor': 18},
    { 'peso': 17, 'valor': 13},
    { 'peso': 18, 'valor': 19},
    { 'peso': 6, 'valor': 10},
    { 'peso': 15, 'valor': 15},
    { 'peso': 25, 'valor': 40},
    { 'peso': 12, 'valor': 17},
    { 'peso': 19, 'valor': 39},
]

def gerar_populacao_inicial(itens_disponiveis, tamanho_populacao):
    num_max_itens = len(itens_disponiveis)
    
    return [ [random.choice([0,1]) for i in range(num_max_itens)] for j in range(tamanho_populacao)] 


def print_geracao(geracao):
    for g in geracao:
        print('\n')
        for gene in g:
            print('%s ' %(gene), end='', flush=True)
    
# recupera os indices dos valores selecionados para serem inseridos na mochila
def get_index_populacao(populacao):
    return [[index for (index, item) in enumerate(itens_disponiveis) if p[index]] for p in populacao]

# recupera os itens selecionados da população
def get_itens_populacao(populacao):
    return [[item for (index, item) in enumerate(itens_disponiveis) if p[index]] for p in populacao]

# recupera os itens de um unico individuo da população
def get_itens_individuo(individuo):
    return [item for (index, item) in enumerate(itens_disponiveis) if individuo[index]]

# Função fitness para uma população
# Retorna a soma dos pesos e valores de cada item da mochila
def calcular_fitness(populacao):
    itens_populacao = get_itens_populacao(populacao)
    
    fitness_values = []
    for index, itens_individuo in enumerate(itens_populacao):
        individuo = populacao[index]
        fitness_values.append( sum_itens(itens_individuo) )
        
    return fitness_values

# Função fitness para um unico indivíduo da população
def fitness_individuo(individuo):
    itens_individuo = get_itens_individuo(individuo)
    
    return sum_itens(itens_individuo)

def fitness_normalizada(populacao):
    fitness_values = calcular_fitness(populacao)
    fitness_total = sum_fitness(fitness_values)
    normalizado = []
    
    for individuo in populacao:
        f = fitness_individuo(individuo)
        f_normalizado = {
            'peso': f['peso'] / fitness_total['peso'], 
            'valor': f['valor'] / fitness_total['valor']
        }
        
        normalizado.append(f_normalizado)
        
    return normalizado
    
# Retorna a soma do peso dos indivíduos
def get_peso_individuo(individuo):
    peso = 0
    for item in get_itens_individuo(individuo):
        peso += item['peso']
    return peso

# Soma todos os valores da função fitness apresentados
def sum_fitness(fitness_values):
    return sum_itens(fitness_values)

# soma os pesos e valores dos itens apresentados
def sum_itens(itens):
    soma_peso = 0
    soma_valor = 0
    for item in itens:
        soma_peso += item['peso']
        soma_valor += item['valor']
    
    return {'peso': soma_peso, 'valor': soma_valor}
   
def selecao_roleta(populacao):
    p = fitness_normalizada(populacao)
    
    selecionados = []
    for individuo in populacao:
        p_selecao = random.uniform(0, 1)
        
        index_individuo_selecionado = 0
        soma = p[index_individuo_selecionado]['valor']
        while soma < p_selecao:
            index_individuo_selecionado += 1
            soma += p[index_individuo_selecionado]['valor']
        
        selecionados.append(populacao[index_individuo_selecionado])
    
    return selecionados


def crossover(populacao, probabilidade):
    
    populacao_crossover = list(populacao) #copia a população inicial para não deletar
    tamanho_populacao = len(populacao_crossover)
    
    num_individuos_crossover = 0 #numero de individuos que passaram por crossover
    crossovered = [] #população após crossover
    
    while num_individuos_crossover < tamanho_populacao:
        num_individuos_crossover += 2
        
        individuo_1 = select_and_remove(populacao_crossover)
        individuo_2 = select_and_remove(populacao_crossover)
        
        # probabilidade de crossover menor que o limiar
        p_not_crossover = random.uniform(0, 1)
        if probabilidade < p_not_crossover:
            # caso não tenha ocorrido o crossover
            crossovered.append(individuo_1)
            crossovered.append(individuo_2)
            continue
        
        ponto_corte  = random.randrange(len(individuo_1))
        
        filho_1 = list(individuo_1[: ponto_corte ]) + list(individuo_2[ponto_corte : ])
        filho_2 = list(individuo_2[: ponto_corte ]) + list(individuo_1[ponto_corte : ])
        
        crossovered.append(filho_1)
        crossovered.append(filho_2)
    
    return crossovered
        
def select_and_remove(populacao):
    #index_individuo = random.randrange(len(populacao))
    index_individuo = 0 # seleciona sempre os primeiro
    individuo = populacao[index_individuo]
    
    del populacao[index_individuo]
    
    return individuo

def mutar(populacao, probabilidade):
    
    for (index, individuo) in enumerate(populacao):
        populacao[index] = mutar_individuo(individuo, probabilidade)
    
    return populacao


def mutar_individuo(individuo, probabilidade):
    for (index, gene) in enumerate(individuo):
        p_not_mutar = random.uniform(0, 1)
        #não muta
        if(probabilidade < p_not_mutar):
            continue
        
        individuo[index] = inverter_gene(individuo[index])
    
    return individuo

def inverter_gene(gene):
    if gene == 1:
        return 0
    return 1


def fitness_ajustado(populacao, limite_peso):
    fitness_minimo = 0
    fitness_penalizada = []
    for index, individuo in enumerate(populacao):
        
        f_individuo = dict(fitness_individuo(individuo))
        f_individuo['individuo'] = individuo
        
        peso = f_individuo['peso']
        
        #peso permitido
        if peso <= limite_peso:
            fitness_penalizada.append(f_individuo)
            continue
    
        #transforma o fitenss em negativo
        f_individuo['valor'] = f_individuo['valor'] * -1
        #f_individuo['valor'] = f_individuo['valor'] - 5000
        #f_individuo['valor'] = 0 
        
        fitness_penalizada.append(f_individuo)
        
        if f_individuo['valor'] < fitness_minimo:
            fitness_minimo = f_individuo['valor']
    
    #return fitness_penalizada
    return shift_fitness_list(fitness_penalizada, -1 * fitness_minimo)
    #return shift_fitness_list(fitness_penalizada, -5000)

# Desloca os valores fitness pelo valor informado
def shift_fitness_list(fitness_list, shift):
    for f_individuo in fitness_list:
        f_individuo['valor'] += shift

    return fitness_list
            

# Seleciona os melhores indivídus sobreviventes para a próxima geração
def selecionar_nova_populacao(populacao, fitness_ajustado, tamanho_geracao):
    fitness_populacao = sorted(list(fitness_ajustado), key=lambda k: -k['valor']) 
   
    nova_geracao = []
    i = 0
    while i < tamanho_geracao:
        #indice_selecionado = fitness_populacao[i]['index']
        #nova_geracao.append(populacao[indice_selecionado])
        nova_geracao.append(list(fitness_populacao[i]['individuo']))
        
        i += 1
        
    return (nova_geracao, fitness_populacao[:tamanho_geracao])


def media_fitness(fitness_list):
    total = sum_itens(fitness_list)
    size = len(fitness_list)
    return {'valor' : total['valor']/size, 'peso': total['peso']/size } 



def plot(melhores, media, piores):
    melhores_valores = [item['valor'] for item in melhores]
    valores_medios = [item['valor'] for item in media]
    piores_valores = [item['valor'] for item in piores]
    
    geracoes = [i for i in range(len(melhores_valores))]
    
    plt.plot(
        geracoes, melhores_valores, 'r--', 
        geracoes, valores_medios, 'b--',
        geracoes, piores_valores, 'g--',
    )
    plt.show()



limite_peso = 120 #C
tamanho_populacao = 60 #Np
probabilidade_mutacao = 0.05 # Pm
probabilidade_crossover = 0.9 #Pc
maximo_geracoes = 500
 
populacao_inicial = gerar_populacao_inicial(itens_disponiveis, tamanho_populacao)
# fitness_inicial = fitness_ajustado(populacao_inicial, limite_peso)
fitness_inicial = calcular_fitness(populacao_inicial)
                                   
melhores_individuos = []
melhores_fitness = []
piores_fitness = []
fitness_medio = []

geracao = 0

while geracao < maximo_geracoes:
    
    pares = selecao_roleta(populacao_inicial)
    populacao = crossover(pares, probabilidade_crossover)
    populacao = mutar(populacao, probabilidade_mutacao)
    
    
    fitness_geracao_atual = fitness_ajustado(populacao, limite_peso)
    
    populacao_inicial, fitness_selecionados = selecionar_nova_populacao(
            populacao, 
            list(fitness_inicial + fitness_geracao_atual),
            tamanho_populacao
    )
    
    #fitness_inicial = list(fitness_geracao_atual)
    fitness_inicial = calcular_fitness(fitness_geracao_atual)
    
    melhores_individuos.append(populacao_inicial[0])
   
    itens = get_itens_individuo(populacao_inicial[0])
    soma = sum_itens(itens)
    if soma['peso'] > limite_peso:
        soma['valor'] = 0
        
    melhores_fitness.append(soma)
    #melhores_fitness.append(fitness_selecionados[0])
    
    piores_fitness.append(fitness_selecionados[-1])
    fitness_medio.append(media_fitness(fitness_selecionados))
    
    geracao += 1


plot(melhores_fitness, fitness_medio, piores_fitness)

print('fim')