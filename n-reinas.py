import random
"""
Los Algotirmos Geneticos  tienen varios pasos para procesar la informacion

1. Generar una poblacion inicial
2. Evaluar la poblacion(fitness)
3. Desendencia
    3.1. Seleccionar los padres
    3.2. Cruzar los padres
    3.3. Mutar los hijos
    3.4. Aceptar los hijos
4. Reemplazar la poblacion
5. Test de terminacion
6. Loop repetir desde el paso 2
"""
## 1. Generar una poblacion inicial
def generar_poblacion(tamano_poblacion, n):
    poblacion = []
    for _ in range(tamano_poblacion):
        individuo = list(range(1, n + 1))
        random.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion

## 2. Evaluar la poblacion(fitness)
def evaluar_fitness(individuo):
    # Calcular la cantidad de conflictos (amenazas entre reinas)
    conflictos = 0
    next = 1
    for i in range(len(individuo)):
        for j in range(i + next, len(individuo)):
            if (i!=j):
                if (individuo[i] == individuo[j]):
                    conflictos += 1
                if (abs(i - individuo[i]) == abs(j - individuo[j]) or abs(i + individuo[i]) == abs(j + individuo[j])):
                    conflictos += 1
    return conflictos

## 3. Desendencia
# 3.1. Seleccionar los padres
def seleccionar_padres(poblacion, tamano_torneo):
    padres = []
    for _ in range(len(poblacion)//2):  # Tomar la mitad de la población como padres
        torneo = random.sample(poblacion, min(tamano_torneo, len(poblacion)))
        mejor_padre = min(torneo, key=lambda x: evaluar_fitness(x))
        padres.append(mejor_padre)
    return padres

# 3.2. Cruzar los padres
def cruzar(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + [gen for gen in padre2 if gen not in padre1[:punto_cruce]]
    hijo2 = padre2[:punto_cruce] + [gen for gen in padre1 if gen not in padre2[:punto_cruce]]
    return hijo1, hijo2

# 3.3. Mutar los hijos
def mutar(individuo, probabilidad_mutacion):
    if random.uniform(0, 1) < probabilidad_mutacion:
        pos1, pos2 = random.sample(range(len(individuo)), 2)
        individuo[pos1], individuo[pos2] = individuo[pos2], individuo[pos1]
    return individuo

def algoritmo_genetico(n, tamano_poblacion, num_generaciones, tamano_torneo, probabilidad_mutacion):
    poblacion = generar_poblacion(tamano_poblacion, n)

    #6. Loop repetir desde el paso 2
    for generacion in range(num_generaciones):
        poblacion = sorted(poblacion, key=lambda x: evaluar_fitness(x))
        mejores_individuos = poblacion[:tamano_torneo]

        if evaluar_fitness(mejores_individuos[0]) == 0:
            print(f'Solución encontrada en la generación {generacion}:\n{mejores_individuos[0]}')
            return mejores_individuos[0]

        padres = seleccionar_padres(poblacion, tamano_torneo)

        hijos = []

        #3.4. Aceptar los hijos
        for i in range(0, len(padres), 2):
            if i + 1 < len(padres):  # Asegurar que hay dos padres para cruzar
                hijo1, hijo2 = cruzar(padres[i], padres[i + 1])
                hijo1 = mutar(hijo1, probabilidad_mutacion)
                hijo2 = mutar(hijo2, probabilidad_mutacion)
                hijos.extend([hijo1, hijo2])


        # 4. Reemplazar la población
        poblacion = mejores_individuos + hijos


    mejor_solucion = min(poblacion, key=lambda x: evaluar_fitness(x))
    print(f'Mejor solución encontrada después de {num_generaciones} generaciones:\n{mejor_solucion}')
    return mejor_solucion

# Parámetros
n = int(input("Ingrese el número de reinas (N): "))
tamano_poblacion = int(input("Ingrese el tamaño de la población: "))
num_generaciones = int(input("Ingrese el número de generaciones: "))
tamano_torneo = min(5, tamano_poblacion)  # Tamaño del torneo para la selección de padres
probabilidad_mutacion = float(input("Ingrese la probabilidad de mutación (0-1): "))

# Ejecutar el algoritmo genético
algoritmo_genetico(n, tamano_poblacion, num_generaciones, tamano_torneo, probabilidad_mutacion)

#Ejemoplo de tamaño 8

algoritmo_genetico(8, 100, 100, 5, 0.1)
