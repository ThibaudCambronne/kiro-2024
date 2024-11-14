import random
import pygad
import numpy as np
from cost_resequencing import compute_cost_resequencing_for_shop
from cost_lot import compute_lot
from parse_instance import Instance


def get_lot_constraint(shop_name, instance):
    for lot_change_constraint in instance.lot_change_constraint:
        if lot_change_constraint["shop"] == shop_name:
            return lot_change_constraint
    return None


def get_best_entry_sequence(
    instance, output_sequence_previous_shop, last_shop_name, next_shop_name
):
    # Assume instance and output_sequence_previous_shop are provided as in the original code
    output_sequence_previous_shop = instance.list_vehicles

    # Update the fitness function to accept three parameters as required by PyGAD 2.20.0
    def fitness_function(ga_instance, solution, solution_idx):
        # Compute the cost using the provided function
        cost = compute_cost_resequencing_for_shop(
            output_sequence_previous_shop,
            solution,
            instance.list_vehicles,
            0 if last_shop_name == "first_shop" else instance.resequencing_cost,
            0
            if last_shop_name == "first_shop"
            else instance.get_shop(last_shop_name)["resequencing_lag"],
        )

        lot_constraint = get_lot_constraint(next_shop_name, instance)
        if lot_constraint is not None:
            cost += compute_lot(
                lot_constraint,
                solution,
            )

        # PyGAD maximizes by default, so return the negative cost for minimization
        return -cost

    # Genetic Algorithm parameters
    population_size = 50
    num_generations = 20
    crossover_probability = 0.7
    mutation_probability = 0.2

    # Define the initial population
    # Convert the instance list to indices for initialization purposes
    num_genes = len(output_sequence_previous_shop)
    initial_population = [
        random.sample(output_sequence_previous_shop, num_genes)
        for _ in range(population_size)
    ]

    # Define the custom crossover function using Order Crossover (OX)
    def custom_crossover_func(parents, offspring_size, ga_instance):
        # Ensure parents is a list to avoid TypeError
        parents = list(
            parents
        )  # Convert to a list to ensure compatibility with random.sample

        offspring = []
        for k in range(offspring_size[0]):
            # Select two random parents for crossover
            parent1, parent2 = random.sample(parents, 2)

            # Select two random crossover points
            cut1, cut2 = sorted(random.sample(range(len(parent1)), 2))

            # Create the child and copy the segment from the first parent
            child = [None] * len(parent1)
            child[cut1:cut2] = parent1[cut1:cut2]

            # Fill the remaining positions from the second parent in order, skipping duplicates
            p2_idx = 0
            for i in range(len(child)):
                if child[i] is None:
                    while parent2[p2_idx] in child:
                        p2_idx += 1
                    child[i] = parent2[p2_idx]

            offspring.append(child)

        return np.array(offspring)

    # Define the mutation function for shuffle index mutation
    def mutation_func(offspring, ga_instance):
        # Swap two indices in each offspring to maintain unique integers
        for i in range(len(offspring)):
            if random.random() < mutation_probability:
                swap_idx1, swap_idx2 = random.sample(range(len(offspring[i])), 2)
                assert swap_idx1 != swap_idx2, "Indices to swap are the same"
                # Swap two elements in the offspring
                offspring[i][swap_idx1], offspring[i][swap_idx2] = (
                    offspring[i][swap_idx2],
                    offspring[i][swap_idx1],
                )
        return offspring

    # Set up the PyGAD GA
    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=int(population_size * crossover_probability),
        fitness_func=fitness_function,
        sol_per_pop=population_size,
        num_genes=num_genes,
        gene_type=int,
        initial_population=np.array(initial_population),
        parent_selection_type="tournament",
        keep_parents=1,
        crossover_type=custom_crossover_func,
        mutation_type=mutation_func,
        mutation_percent_genes=int(mutation_probability * 100),
    )

    # Run the genetic algorithm
    ga_instance.run()

    # Get the best solution after all generations
    best_solution, best_solution_fitness, _ = ga_instance.best_solution()

    # Print the results
    print("Best sequence:", best_solution)
    print("Best cost:", -best_solution_fitness)
    return [int(x) for x in best_solution]
