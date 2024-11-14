from constants import INSTANCES_FOLDER
import json
import pandas as pd


def read_instance(instance_name):
    instance_path = INSTANCES_FOLDER / f"{instance_name}.json"
    with open(instance_path, "r") as f:
        instance = json.load(f)

    return instance


class Instance:
    def __init__(self, instance_name):
        self.instance = read_instance(instance_name)
        self.parse_parameters()
        self.parse_shops()
        self.parse_vehicle()
        self.parse_constraints()

    def parse_parameters(self):
        self.two_tone_delta = self.instance["parameters"]["two_tone_delta"]
        self.resequencing_cost = self.instance["parameters"]["resequencing_cost"]

    def parse_shops(self):
        self.shops = self.instance["shops"]

    def parse_vehicle(self):
        vehicles = pd.DataFrame(self.instance["vehicles"])
        self.list_vehicles = vehicles.id.to_list()
        self.two_tone_vehicles = vehicles.query("type == 'two-tone'").id.to_list()

    def parse_constraints(self):
        constraints = self.instance["constraints"]

        self.rolling_window_constraint = []
        self.batch_size_constraint = []
        self.lot_change_constraint = []

        for constraint in constraints:
            if constraint["type"] == "rolling_window":
                self.rolling_window_constraint.append(constraint)
            elif constraint["type"] == "batch_size":
                self.batch_size_constraint.append(constraint)
            elif constraint["type"] == "lot_change":
                self.lot_change_constraint.append(constraint)

        assert len(self.rolling_window_constraint) + len(
            self.batch_size_constraint
        ) + len(self.lot_change_constraint) == len(
            constraints
        ), "Some constraints have a type that isn't parsed"


if __name__ == "__main__":
    instance_ex = Instance("tiny")
