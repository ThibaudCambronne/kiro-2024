from constants import TypeSequence
from go_through_paint_shop import find_position_of_vehicle
from parse_instance import Instance


def find_partition_of_vehicle(
    partitions: dict[int, list[int]],
    vehicle: int,
):
    for partition_number, partition in partitions.items():
        if vehicle in partition:
            return partition_number


def compute_lot(
    lot_constraint,
    sequence: TypeSequence,
):
    cost = 0
    contraint_partitions = {
        i: partition for i, partition in enumerate(lot_constraint["partition"])
    }
    for i in range(len(sequence) - 1):
        current_vehicle = sequence[i]
        partition_current_vehicle = find_partition_of_vehicle(
            contraint_partitions, current_vehicle
        )
        next_vehicle = sequence[i + 1]
        partition_next_vehicle = find_partition_of_vehicle(
            contraint_partitions, next_vehicle
        )
        if partition_current_vehicle != partition_next_vehicle:
            cost += lot_constraint["cost"]

    return cost


if __name__ == "__main__":
    pass
