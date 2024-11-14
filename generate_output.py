from parse_instance import Instance
from constants import TypeOneShopOutput, INSTANCES_FOLDER, SOLUTIONS_FOLDER
from solution_naive import solution_naive
import json


def save_solution(instance_name: str, output: dict[str, TypeOneShopOutput]) -> None:
    SOLUTIONS_FOLDER.mkdir(exist_ok=True)
    with open(SOLUTIONS_FOLDER / f"{instance_name}_naive.json", "w") as f:
        json.dump(output, f)


def generate_output():
    # iter through all the instances
    for instance_file in INSTANCES_FOLDER.iterdir():
        if instance_file.suffix == ".json":
            instance_name = instance_file.stem
            solution = solution_naive(Instance(instance_name))
            save_solution(instance_name, solution)


if __name__ == "__main__":
    generate_output()
