from pathlib import Path
from typing import TypedDict

INSTANCES_FOLDER = Path(__file__).parent / "instances"

SOLUTIONS_FOLDER = Path(__file__).parent / "solutions"

TypeSequence = list[int]


class TypeOneShopOutput(TypedDict):
    entry: TypeSequence
    exit: TypeSequence
