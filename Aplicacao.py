
import random

cargas = [5, 10, 15, 3, 10, 5, 2, 16, 9, 7]
tamPopulacao = 100
maxGeracoes = 1000
taxaMutacao = 0.01

# Gera um individuo com 10 genes aleatorios (0 ou 1)
def gerarIndividuo():
    individuo = []

    for i in range(len(cargas)):
        gene = random.randint(0, 1)
        individuo.append(gene)

    return individuo


# Gera a populacao inicial com 100 individuos
def gerarPopulacao():
    populacao = []

    for i in range(tamPopulacao):
        individuo = gerarIndividuo()
        populacao.append(individuo)

    return populacao


# Calcula a carga horaria de cada pessoa
def calcularCargas(individuo):
    cargaA = 0
    cargaB = 0

    for i in range(len(individuo)):
        if individuo[i] == 0:
            cargaA += cargas[i]
        else:
            cargaB += cargas[i]

    return cargaA, cargaB


# Calcula a aptidao - menor a diferenca, melhor
def calcularAptidao(individuo):
    cargaA, cargaB = calcularCargas(individuo)
    diferenca = abs(cargaA - cargaB)
    aptidao = 1 / (1 + diferenca)

    return aptidao


# Encontra o melhor individuo da populacao (elitismo)
def melhorIndividuo(populacao):
    melhor = populacao[0]

    for individuo in populacao:
        if calcularAptidao(individuo) > calcularAptidao(melhor):
            melhor = individuo

    return melhor


# Sorteia dois individuos e escolhe o de maior aptidao
def selecaoTorneio(populacao):
    competidores = random.sample(populacao, 2)
    vencedor = competidores[0]

    if calcularAptidao(competidores[1]) > calcularAptidao(vencedor):
        vencedor = competidores[1]

    return vencedor


# Combina os genes dos pais usando um ponto de corte
def crossoverUniponto(pai1, pai2):
    pontoCorte = random.randint(1, len(pai1) - 1)

    filho1 = pai1[:pontoCorte] + pai2[pontoCorte:]
    filho2 = pai2[:pontoCorte] + pai1[pontoCorte:]

    return filho1, filho2


# Inverte genes aleatoriamente conforme a taxa de mutacao
def mutacao(individuo):
    for i in range(len(individuo)):
        if random.random() < taxaMutacao:
            individuo[i] = 1 - individuo[i]

    return individuo


# Verifica se pelo menos 98% dos individuos sao iguais
def convergiu(populacao):
    individuoReferencia = populacao[0]
    quantidadeIguais = 0

    for individuo in populacao:
        if individuo == individuoReferencia:
            quantidadeIguais += 1

    proporcao = quantidadeIguais / len(populacao)

    return proporcao >= 0.98


populacao = gerarPopulacao()
geracao = 0
motivoParada = ""

while True:
    melhor = melhorIndividuo(populacao)
    aptidao = calcularAptidao(melhor)

    if geracao % 50 == 0:
        print(f"Geracao: {geracao} | Aptidao: {aptidao:.4f}")

    # Criterio de parada 1 - solucao otima
    if aptidao == 1.0:
        motivoParada = "Aptidao otima encontrada"
        break

    # Criterio de parada 2 - atingiu o maximo de geracoes
    if geracao >= maxGeracoes:
        motivoParada = "Limite maximo de geracoes atingido"
        break

    # Criterio de parada 3 - populacao convergiu
    if convergiu(populacao):
        motivoParada = "Populacao convergiu"
        break

    # Elitismo: preserva o melhor individuo
    elite = melhor.copy()
    novaPopulacao = [elite]

    # Cria filhos ate completar a nova populacao
    while len(novaPopulacao) < tamPopulacao:

        # Seleciona os pais por torneio
        pai1 = selecaoTorneio(populacao)
        pai2 = selecaoTorneio(populacao)

        # Realiza o crossover uniponto
        filho1, filho2 = crossoverUniponto(pai1, pai2)

        # Aplica mutacao nos filhos
        mutacao(filho1)
        mutacao(filho2)

        # Adiciona os filhos sem ultrapassar 100 individuos
        novaPopulacao.append(filho1)

        if len(novaPopulacao) < tamPopulacao:
            novaPopulacao.append(filho2)

    # Atualiza a populacao para a proxima geracao
    populacao = novaPopulacao
    geracao += 1


melhor = melhorIndividuo(populacao)
cargaA, cargaB = calcularCargas(melhor)

print("Motivo da parada:", motivoParada)
print("Geracoes executadas:", geracao)
print("Melhor cromossomo:", melhor)
print("Aptidao:", calcularAptidao(melhor))

print("\nDistribuicao das tarefas:")

for i in range(len(melhor)):
    pessoa = "A" if melhor[i] == 0 else "B"

    print(
        f"Tarefa {i + 1}: "
        f"{cargas[i]} horas -> Pessoa {pessoa}"
    )

print("\nCarga total da pessoa A:", cargaA, "horas")
print("Carga total da pessoa B:", cargaB, "horas")
print("Diferenca de horas:", abs(cargaA - cargaB))
