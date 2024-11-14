from parse_instance import Instance
from constants import TypeOneShopOutput, INSTANCES_FOLDER, SOLUTIONS_FOLDER
from solution_naive import solution_naive, best_lot_initial_vehicles_list
from solution_genetic_algorithm import solution_genetic_algorithm
import json
from pathlib import Path
from tqdm import tqdm


def save_solution(
    instance_name: str, output: dict[str, TypeOneShopOutput], output_folder_name: str
) -> None:
    output_folder = SOLUTIONS_FOLDER / output_folder_name
    output_folder.mkdir(exist_ok=True)
    with open(output_folder / f"{instance_name}_naive.json", "w") as f:
        json.dump(output, f)


def generate_output(output_folder_name: str) -> None:
    # iter through all the instances
    for instance_file in tqdm(INSTANCES_FOLDER.iterdir(), desc="Generating outputs"):
        if instance_file.suffix == ".json":
            instance_name = instance_file.stem
            instance = Instance(instance_name)
            solution = solution_genetic_algorithm(instance)
            save_solution(instance_name, solution, output_folder_name)


if __name__ == "__main__":
    generate_output("ga3")
