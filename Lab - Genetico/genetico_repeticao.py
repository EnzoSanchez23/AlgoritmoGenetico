from pyeasyga import pyeasyga
import random
import matplotlib.pyplot as plt

# Dados dos itens
data = [{'name': 'green', 'value': 4, 'weight': 12},
        {'name': 'gray', 'value': 2, 'weight': 1},
        {'name': 'yellow', 'value': 10, 'weight': 4},
        {'name': 'orange', 'value': 1, 'weight': 1},
        {'name': 'blue', 'value': 2, 'weight': 2}]

tamanho_populacao = 10
capacidade_mochila = 15  # Capacidade da mochila

# Configuração do algoritmo genético
ga = pyeasyga.GeneticAlgorithm(data, population_size=tamanho_populacao,
                               generations=50,
                               crossover_probability=0.9,
                               mutation_probability=0.1,
                               elitism=False,
                               maximise_fitness=True)

# Contador para controle das aptidões por geração
cont = 0
aptidoes_por_geracao = []
melhor_por_geracao = []

# Função de aptidão
def aptidao(individual, data):
    global cont
    cont += 1
    
    valor_total, peso_total = 0, 0
    for quantidade, item in zip(individual, data):
        valor_total += quantidade * item['value']
        peso_total += quantidade * item['weight']
    
    # Penalizar se o peso exceder a capacidade da mochila
    if peso_total > capacidade_mochila:
        valor_total = 0
    
    # Guardar aptidão da geração
    aptidoes_por_geracao.append(valor_total)
    if cont >= tamanho_populacao:
        melhor_por_geracao.append(max(aptidoes_por_geracao))
        aptidoes_por_geracao.clear()
        cont = 0
    
    return valor_total

# Definir a função create_individual para gerar indivíduos válidos
def create_individual(seed_data=None):
    return [random.randint(0, 10) for _ in range(len(data))]  # Permitir até 10 repetições por item

# Atribuir a função de criação de indivíduos e função de aptidão
ga.create_individual = create_individual
ga.fitness_function = aptidao

# Executar o algoritmo genético
ga.run()

# Resultados
melhor_individuo = ga.best_individual()
melhor_aptidao = ga.fitness_function(melhor_individuo[1], data)  # Recalcular aptidão para o melhor indivíduo encontrado

print("Melhor indivíduo encontrado:", melhor_individuo)
print("Melhor valor:", melhor_aptidao)

# Plotar o gráfico de melhores valores por geração
plt.plot(melhor_por_geracao)
plt.title('Melhor Valor por Geração')
plt.xlabel('Geração')
plt.ylabel('Valor')
plt.savefig('graphComRep.jpg')
