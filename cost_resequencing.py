from constants import TypeSequence
from go_through_paint_shop import find_position_of_vehicle
from parse_instance import Instance


def compute_cost_resequencing_for_shop(
    output_sequence_previous_shop: TypeSequence,
    entry_sequence_current_shop: TypeSequence,
    list_of_vehicle: list[int],
    resequencing_cost: int,
    lag_next_shop_with_previous: int,
):
    cost = 0
    for i in range(len(list_of_vehicle)):
        current_vehicle = list_of_vehicle[i]
        position_when_exited_previous_shop = find_position_of_vehicle(
            output_sequence_previous_shop, current_vehicle
        )
        position_when_entered_current_shop = find_position_of_vehicle(
            entry_sequence_current_shop, current_vehicle
        )
        cost += max(
            0,
            position_when_exited_previous_shop
            - position_when_entered_current_shop
            - lag_next_shop_with_previous,
        )

    cost *= resequencing_cost

    return cost


if __name__ == "__main__":
    pass
