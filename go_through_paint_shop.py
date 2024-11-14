from constants import TypeSequence
import pandas as pd


def find_position_of_vehicle(entry_sequence: TypeSequence, vehicle: int) -> int:
    for i in range(len(entry_sequence)):
        if entry_sequence[i] == vehicle:
            return i + 1
    raise ValueError(f"Vehicle {vehicle} not found in sequence {entry_sequence}")


def apply_permutation(
    entry_sequence: TypeSequence, permutation: list[int]
) -> TypeSequence:
    start_index_of_permutation = permutation[0] - 1
    elements_before_permutation = entry_sequence[:start_index_of_permutation]
    # print(elements_before_permutation)

    end_index_of_permutation = len(permutation) + start_index_of_permutation
    elements_after_permutation = entry_sequence[end_index_of_permutation:]
    # print(elements_after_permutation)

    permuted_elements = []
    # go through permutation starting from the end
    for i in range(len(permutation)):
        permutation_element = permutation[-(i + 1)]
        permuted_elements.append(entry_sequence[permutation_element - 1])

    output_sequence = (
        elements_before_permutation + permuted_elements + elements_after_permutation
    )
    return output_sequence


def go_through_paint_shop(
    entry_sequence: TypeSequence, two_tone_vehicles: list[int], two_tone_delta: int
) -> TypeSequence:
    n = len(entry_sequence)

    # First, we need to get an increasing list of the position of the two-tone vehicles
    # in the entry sequence
    df_vehicles_position = pd.DataFrame(
        {
            "vehicle": two_tone_vehicles,
            "initial_position": [
                find_position_of_vehicle(entry_sequence, vehicle)
                for vehicle in two_tone_vehicles
            ],
        }
    )
    df_vehicles_position = df_vehicles_position.sort_values(by="initial_position")
    ordered_two_tone_vehicles = df_vehicles_position["vehicle"].tolist()
    sequence_after_permutation_of_t_uk_1 = entry_sequence
    for uk in ordered_two_tone_vehicles:
        new_t_uk = find_position_of_vehicle(sequence_after_permutation_of_t_uk_1, uk)
        delta = min(two_tone_delta, n - new_t_uk)
        permutation = [new_t_uk] + [new_t_uk + delta - i for i in range(delta)]
        sequence_after_permutation_of_t_uk_1 = apply_permutation(
            sequence_after_permutation_of_t_uk_1, permutation
        )

    return sequence_after_permutation_of_t_uk_1


if __name__ == "__main__":
    # test 1
    entry_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    two_tone_vehicles = [1]
    two_tone_delta = 3
    assert go_through_paint_shop(entry_sequence, two_tone_vehicles, two_tone_delta) == [
        2,
        3,
        4,
        1,
        5,
        6,
        7,
        8,
        9,
        10,
    ]

    # test 2
    entry_sequence = [5, 4, 3, 2, 1]
    two_tone_vehicles = [3]
    two_tone_delta = 2
    assert go_through_paint_shop(entry_sequence, two_tone_vehicles, two_tone_delta) == [
        5,
        4,
        2,
        1,
        3,
    ]

    # test 3
    entry_sequence = [5, 3, 4, 2, 1]
    two_tone_vehicles = [2, 3, 4]
    two_tone_delta = 2

    assert go_through_paint_shop(entry_sequence, two_tone_vehicles, two_tone_delta) == [
        5,
        3,
        4,
        2,
        1,
    ]

    # test 4
    entry_sequence = [6, 3, 4, 2, 1, 5]
    two_tone_vehicles = [5, 4, 2]
    two_tone_delta = 4
    assert go_through_paint_shop(entry_sequence, two_tone_vehicles, two_tone_delta) == [
        6,
        3,
        1,
        4,
        2,
        5,
    ]

    # test final
    entry_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    two_tone_vehicles = [1, 3, 8, 9]
    two_tone_delta = 3
    assert go_through_paint_shop(entry_sequence, two_tone_vehicles, two_tone_delta) == [
        2,
        4,
        1,
        5,
        3,
        6,
        7,
        10,
        8,
        9,
    ]
    print("All tests passed!")
