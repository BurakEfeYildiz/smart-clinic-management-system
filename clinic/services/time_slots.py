from datetime import datetime, timedelta


def build_time_slots(start_time, end_time, slot_minutes):
    slots = []
    current = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)

    while current < end:
        slots.append(current.time())
        current += timedelta(minutes=slot_minutes)

    return slots
