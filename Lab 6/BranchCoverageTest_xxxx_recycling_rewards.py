import pytest

from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status,
)


@pytest.mark.parametrize(
    "material, weight, bonus, expected",
    [
        ("paper", 3, False, 0),
        ("paper", 6, True, 12),
        ("metal", 23, False, 378),
    ],
)
def test_reward_points(material, weight, bonus, expected):
    assert reward_points(material, weight, bonus) == expected


def test_unknown_material():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 5, False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


@pytest.mark.parametrize(
    "weight, bags, hazardous, expected",
    [
        (4, 1, True, True),
        (51, 1, False, False),
        (20, 2, False, True),
    ],
)
def test_collection_accepted(weight, bags, hazardous, expected):
    assert collection_accepted(weight, bags, hazardous) is expected


@pytest.mark.parametrize(
    "minutes, morning, holiday, expected",
    [
        (35, True, True, "open"),
        (0, False, False, "late"),
        (-6, False, False, "missed"),
    ],
)
def test_slot_status(minutes, morning, holiday, expected):
    assert slot_status(minutes, morning, holiday) == expected

@pytest.mark.parametrize(
    "material, weight, bonus, expected",
    [
        ("plastic", 24, False, 210),
        ("metal", 3, True, 12),
        ("paper", 5, False, 0),
        ("plastic", 3, False, 0),
        ("paper", 25, False, 120),
    ],
)
def test_reward_additional_cases(material, weight, bonus, expected):
    assert reward_points(material, weight, bonus) == expected


@pytest.mark.parametrize(
    "weight, bags, hazardous, expected",
    [
        (5, 1, True, True),
        (6, 1, True, False),
        (50, 3, False, True),
        (50, 4, False, False),
    ],
)
def test_collection_boundaries(weight, bags, hazardous, expected):
    assert collection_accepted(weight, bags, hazardous) is expected


@pytest.mark.parametrize(
    "minutes, morning, holiday, expected",
    [
        (20, True, False, "open"),
        (19, True, False, "late"),
        (5, True, False, "late"),
        (4, True, False, "missed"),
        (25, False, True, "open"),
        (24, False, True, "late"),
        (10, False, True, "late"),
        (9, False, True, "missed"),
    ],
)
def test_slot_boundaries(minutes, morning, holiday, expected):
    assert slot_status(minutes, morning, holiday) == expected