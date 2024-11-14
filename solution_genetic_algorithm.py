from go_through_paint_shop import go_through_paint_shop
from solution_naive import naive_initial_vehicles_list, naive_initial_vehicles_list
from parse_instance import Instance
from constants import TypeOneShopOutput
from get_best_entry_sequence import get_best_entry_sequence

from tqdm import tqdm


def solution_genetic_algorithm(instance: Instance) -> dict[str, TypeOneShopOutput]:
    output = {}
    initial_vehicles_list = naive_initial_vehicles_list(instance)

    for i, shop in tqdm(enumerate(instance.shops)):
        if i == 0:
            entry_shop_sequence = initial_vehicles_list
        else:
            entry_shop_sequence = get_best_entry_sequence(
                instance, output_shop_sequence, "first_shop", shop["name"]
            )
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

    return output


if __name__ == "__main__":
    instance = Instance("large_1")
    print(solution_genetic_algorithm(instance))
