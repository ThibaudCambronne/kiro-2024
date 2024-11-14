from parse_instance import Instance
from constants import TypeOneShopOutput
from go_through_paint_shop import go_through_paint_shop
import pandas as pd


def naive_initial_vehicles_list(instance: Instance) -> list[int]:
    return sorted(instance.list_vehicles)


def get_number_of_two_tone_vehicles_in_partition(
    partition: list[int], two_tone_vehicles: list[int]
) -> int:
    return len([vehicle for vehicle in partition if vehicle in two_tone_vehicles])


assert get_number_of_two_tone_vehicles_in_partition([1, 2, 3, 4, 5], [3, 4, 5]) == 3


def best_lot_initial_vehicles_list(instance: Instance) -> list[int]:
    # select the lot change constraint with the highest cost
    max_cost = 0
    best_lot_change_constraint = instance.lot_change_constraint[0]
    for lot_change_constraint in instance.lot_change_constraint:
        if lot_change_constraint["cost"] > max_cost:
            max_cost = lot_change_constraint["cost"]
            best_lot_change_constraint = lot_change_constraint

    partitions = {
        i: partition
        for i, partition in enumerate(best_lot_change_constraint["partition"])
    }
    df_partitions = pd.DataFrame(data={"partition_number": list(partitions.keys())})

    # reorder the partitions to get the one with the least
    # two-tone vehicles first
    df_partitions["two_tone_vehicles"] = df_partitions.apply(
        lambda x: get_number_of_two_tone_vehicles_in_partition(
            partitions[x["partition_number"]], instance.two_tone_vehicles
        ),
        axis=1,
    )
    df_partitions = df_partitions.sort_values(by="two_tone_vehicles")

    # concat the partitions
    best_lot_initial_vehicles_list = []
    for partition_number in df_partitions["partition_number"]:
        best_lot_initial_vehicles_list += partitions[partition_number]

    assert len(best_lot_initial_vehicles_list) == len(
        instance.list_vehicles
    ), "the partitions are not complete (some vehicles aren' t in them)"

    return best_lot_initial_vehicles_list


def solution_naive(
    instance: Instance, initial_vehicles_list: list[int] | None = None
) -> dict[str, TypeOneShopOutput]:
    output = {}
    if initial_vehicles_list is None:
        initial_vehicles_list = naive_initial_vehicles_list(instance)

    entry_shop_sequence = initial_vehicles_list

    for shop in instance.shops:
        shop_name = shop["name"]
        output[shop_name] = {}
        output[shop_name]["entry"] = entry_shop_sequence

        if shop_name == "paint":
            # then we need to apply the two_tone_delta
            output_shop_sequence = go_through_paint_shop(
                entry_shop_sequence, instance.two_tone_vehicles, instance.two_tone_delta
            )
        else:
            output_shop_sequence = entry_shop_sequence

        output[shop_name]["exit"] = output_shop_sequence
        entry_shop_sequence = output_shop_sequence

    return output


if __name__ == "__main__":
    instance = Instance("large_1")
    print(solution_naive(instance, best_lot_initial_vehicles_list(instance)))
