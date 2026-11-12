"""Property-based validation tests for processor.py (Hypothesis + pytest)."""

import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import collection_accepted, reward_points, slot_status


@settings(max_examples=150, deadline=None)
@given(
    material=st.sampled_from(["paper", "plastic", "metal"]),
    weight=st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False),
    bonus=st.booleans(),
)
def test_reward_points_are_non_negative_for_valid_inputs(material, weight, bonus):
    assert reward_points(material, weight, bonus) >= 0


@settings(max_examples=100, deadline=None)
@given(
    material=st.sampled_from(["paper", "plastic"]),
    weight=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_bonus_never_reduces_reward(material, weight):
    assert reward_points(material, weight, True) >= reward_points(material, weight, False)


@pytest.mark.parametrize("bad_weight", [None, "5", [], True, False])
def test_reward_rejects_non_numeric_or_boolean_weights(bad_weight):
    with pytest.raises(TypeError):
        reward_points("paper", bad_weight, False)


@pytest.mark.parametrize("bad_weight", [-1, math.inf, -math.inf, math.nan])
def test_reward_rejects_negative_or_non_finite_weights(bad_weight):
    with pytest.raises(ValueError):
        reward_points("paper", bad_weight, False)


@settings(max_examples=120, deadline=None)
@given(weight=st.one_of(st.none(), st.booleans(), st.floats(allow_nan=True, allow_infinity=True)))
def test_fuzz_reward_weight_contract(weight):
    if isinstance(weight, bool) or weight is None:
        with pytest.raises(TypeError):
            reward_points("paper", weight, False)
    elif not math.isfinite(weight) or weight < 0:
        with pytest.raises(ValueError):
            reward_points("paper", weight, False)
    else:
        assert reward_points("paper", weight, False) >= 0


@settings(max_examples=120, deadline=None)
@given(
    weight=st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False),
    bags=st.integers(min_value=0, max_value=10),
    hazardous=st.booleans(),
)
def test_collection_result_is_boolean(weight, bags, hazardous):
    assert isinstance(collection_accepted(weight, bags, hazardous), bool)


@pytest.mark.parametrize("bad_bags", [None, "2", 2.0, True, False, []])
def test_collection_rejects_invalid_bag_counts(bad_bags):
    with pytest.raises(TypeError):
        collection_accepted(4, bad_bags, False)


def test_collection_rejects_negative_bag_count():
    with pytest.raises(ValueError):
        collection_accepted(4, -1, False)


@settings(max_examples=120, deadline=None)
@given(bags=st.one_of(st.none(), st.booleans(), st.integers()))
def test_fuzz_collection_bag_contract(bags):
    if isinstance(bags, bool) or bags is None:
        with pytest.raises(TypeError):
            collection_accepted(4, bags, False)
    elif bags < 0:
        with pytest.raises(ValueError):
            collection_accepted(4, bags, False)
    else:
        assert isinstance(collection_accepted(4, bags, False), bool)


@settings(max_examples=120, deadline=None)
@given(
    minutes=st.integers(min_value=-10000, max_value=10000),
    morning=st.booleans(),
    holiday=st.booleans(),
)
def test_slot_status_is_one_of_the_documented_results(minutes, morning, holiday):
    assert slot_status(minutes, morning, holiday) in {"open", "late", "missed"}


@settings(max_examples=120, deadline=None)
@given(minutes=st.one_of(st.none(), st.booleans(), st.integers()))
def test_fuzz_slot_minute_contract(minutes):
    if isinstance(minutes, bool) or minutes is None:
        with pytest.raises(TypeError):
            slot_status(minutes, True, False)
    else:
        assert slot_status(minutes, True, False) in {"open", "late", "missed"}


@pytest.mark.parametrize("bad_minutes", [None, "20", 20.0, True, False, []])
def test_slot_rejects_non_integer_or_boolean_minutes(bad_minutes):
    with pytest.raises(TypeError):
        slot_status(bad_minutes, True, False)


@pytest.mark.parametrize(
    "function,args",
    [
        (lambda value: reward_points("paper", 5, value), (1,)),
        (lambda value: collection_accepted(4, 1, value), ("yes",)),
        (lambda value: slot_status(20, value, False), (1,)),
    ],
)
def test_boolean_flags_are_validated(function, args):
    with pytest.raises(TypeError):
        function(*args)


def test_known_reward_and_boundary_examples():
    assert reward_points("paper", 5, False) == 0
    assert reward_points("paper", 6, True) == 12
    assert reward_points("metal", 23, False) == 378


def test_collection_boundaries():
    assert collection_accepted(5, 99, True) is True
    assert collection_accepted(5.01, 1, True) is False
    assert collection_accepted(50, 3, False) is True
    assert collection_accepted(50, 4, False) is False


def test_slot_boundaries():
    assert slot_status(20, True, False) == "open"
    assert slot_status(19, True, False) == "late"
    assert slot_status(4, True, False) == "missed"
