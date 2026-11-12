"""Input-validated recycling reward and collection utilities for Lab 7."""

from math import isfinite
from numbers import Real


MIN_KG = {"paper": 5, "plastic": 3, "metal": 2}


def _validate_weight(weight_kg):
    if isinstance(weight_kg, bool) or not isinstance(weight_kg, Real):
        raise TypeError("weight_kg must be a real number")
    if not isfinite(weight_kg):
        raise ValueError("weight_kg must be finite")
    if weight_kg < 0:
        raise ValueError("weight_kg must be non-negative")


def _validate_bool(value, name):
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool")


def reward_points(material, weight_kg, has_bonus):
    """Return points for a supported material and a non-negative finite weight."""
    if not isinstance(material, str):
        raise TypeError("material must be a string")
    if material not in MIN_KG:
        raise ValueError("unknown material")
    _validate_weight(weight_kg)
    _validate_bool(has_bonus, "has_bonus")

    minimum = MIN_KG[material]
    if has_bonus and material != "metal":
        minimum -= 1
    extra = weight_kg - minimum
    if extra <= 0:
        return 0

    rate = 12 if material == "metal" else 6
    if extra > 20:
        rate += 4
        if material == "metal":
            rate += 2
    return extra * rate


def collection_accepted(weight_kg, bags, is_hazardous):
    """Check collection limits after validating each argument."""
    _validate_weight(weight_kg)
    if isinstance(bags, bool) or not isinstance(bags, int):
        raise TypeError("bags must be an integer")
    if bags < 0:
        raise ValueError("bags must be non-negative")
    _validate_bool(is_hazardous, "is_hazardous")

    if is_hazardous:
        return weight_kg <= 5
    if weight_kg > 50:
        return False
    return bags <= 3


def slot_status(minutes_left, is_morning, is_holiday):
    """Return the pickup status for an integer minute count and boolean flags."""
    if isinstance(minutes_left, bool) or not isinstance(minutes_left, int):
        raise TypeError("minutes_left must be an integer")
    _validate_bool(is_morning, "is_morning")
    _validate_bool(is_holiday, "is_holiday")

    cutoff = 20 if is_morning else 10
    if is_holiday:
        cutoff += 15
    if minutes_left >= cutoff:
        return "open"
    if minutes_left >= cutoff - 15:
        return "late"
    return "missed"


if __name__ == "__main__":
    print("Recycling rewards processor")
    print("paper, 10 kg, no bonus:", reward_points("paper", 10, False))
    print("20 kg, 2 bags, non-hazardous:", collection_accepted(20, 2, False))
    print("20 minutes, morning, not a holiday:", slot_status(20, True, False))
