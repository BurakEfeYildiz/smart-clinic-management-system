from datetime import time

from clinic.services.time_slots import build_time_slots


def test_build_time_slots_creates_expected_intervals():
    slots = build_time_slots(time(9, 0), time(10, 0), 30)

    assert slots == [time(9, 0), time(9, 30)]
