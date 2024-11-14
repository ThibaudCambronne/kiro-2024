from parse_instance import Instance
from constants import TypeOneShopOutput
from go_through_paint_shop import go_through_paint_shop


def naive_initial_vehicles_list(instance: Instance) -> list[int]:
    return sorted(instance.list_vehicles)


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
    instance = Instance("tiny")
    print(solution_naive(instance))
