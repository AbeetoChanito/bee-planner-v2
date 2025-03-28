from math import pi
from typing import Dict


def cbool(value: bool) -> str:
    return str(value).lower()


def degrees_to_radians(heading: float) -> float:
    return heading / 180 * pi


def radians_to_degrees(heading: float) -> float:
    return heading / pi * 180


def build_args(arg_list: Dict[str, any]) -> str:
    ans = "{ "
    for key, value in arg_list.items():
        # edge case: handle if the value is a boolean
        if isinstance(value, bool):
            value = cbool(value)
        ans += f".{key} = {value}, "
    ans += "}"
    return ans
