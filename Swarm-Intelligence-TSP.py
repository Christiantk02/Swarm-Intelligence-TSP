import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic

cities = np.array([
    [59.9139, 10.7522],  # Oslo
    [60.3913, 5.3221],   # Bergen
    [58.9701, 5.7333],   # Stavanger
    [63.4305, 10.3951],  # Trondheim
    [58.1467, 7.9956],   # Kristiansand
    [62.4722, 6.1549],   # Ålesund
    [69.6496, 18.9560],  # Tromsø
    [67.2804, 14.4049],  # Bodø
    [68.4385, 17.4274],  # Narvik
    [61.1153, 10.4662]   # Lillehammer
])

def calculate_distance_matrix(cities):
    n = len(cities)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i, j] = geodesic(cities[i], cities[j]).kilometers  
    return dist_matrix

def generate_random_route(cities):
    n = len[cities]
    return np.random.permutation(n) 

def calculate_route_distance(route, dist_matrix):
    n = len(route)
    total_distance = 0
    for i in range(n - 1):
        total_distance += dist_matrix[route[i], route[i + 1]]
    total_distance += dist_matrix[route[n - 1], route[0]]
    return total_distance

def plot_route(route, cities):
    x = cities[route, 1] 
    y = cities[route, 0] 
    plt.plot(x, y, marker='o', linestyle='-', color='blue', label="Optimal rute")
    plt.plot([x[-1], x[0]], [y[-1], y[0]], 'b-')  
    plt.xlabel("Lengdegrad")
    plt.ylabel("Breddegrad")
    plt.title("Optimal rute for DHL-levering")
    plt.legend()
    plt.show()

def abc_tsp(cities, num_bees=30, num_iterations=50, limit=2): #Inspired by ChatGPT (Feb 2025)
    num_cities = len(cities)
    dist_matrix = calculate_distance_matrix(cities)  
    
    bees = [np.random.permutation(num_cities) for _ in range(num_bees)]
    fitness = np.array([1 / calculate_route_distance(route, dist_matrix) for route in bees])
    
    best_route = bees[np.argmax(fitness)]
    best_distance = 1 / max(fitness)
    trial = np.zeros(num_bees) 

    for _ in range(num_iterations):
        for i in range(num_bees):
            new_route = bees[i].copy()
            a, b = np.random.choice(num_cities, size=2, replace=False)
            new_route[a], new_route[b] = new_route[b], new_route[a] 

            new_distance = calculate_route_distance(new_route, dist_matrix)
            new_fitness = 1 / new_distance

            if new_fitness > fitness[i]:  
                bees[i] = new_route
                fitness[i] = new_fitness
                trial[i] = 0  
            else:
                trial[i] += 1  

        probabilities = fitness / np.sum(fitness)
        selected_indices = np.random.choice(range(num_bees), size=num_bees, p=probabilities)

        for i in selected_indices:
            new_route = bees[i].copy()
            a, b = np.random.choice(num_cities, size=2, replace=False)
            new_route[a], new_route[b] = new_route[b], new_route[a]

            new_distance = calculate_route_distance(new_route, dist_matrix)
            new_fitness = 1 / new_distance

            if new_fitness > fitness[i]:
                bees[i] = new_route
                fitness[i] = new_fitness
                trial[i] = 0
            else:
                trial[i] += 1

        for i in range(num_bees):
            if trial[i] > limit:
                bees[i] = np.random.permutation(num_cities) 
                fitness[i] = 1 / calculate_route_distance(bees[i], dist_matrix)
                trial[i] = 0  

        best_index = np.argmax(fitness)
        if fitness[best_index] > 1 / best_distance:
            best_route = bees[best_index]
            best_distance = 1 / fitness[best_index]

    return best_route, best_distance

best_route, best_distance = abc_tsp(cities)

print("Beste rute funnet:", best_route)
print("Korteste avstand:", round(best_distance, 2), "km")

plot_route(best_route, cities)