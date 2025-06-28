from datetime import datetime, timedelta

def suggest_interview_slots(num_candidates, as_rfc3339=False):
    base_date = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    slots = []
    for i in range(num_candidates):
        day_offset = i % 5  # Weekdays only
        slot_time = base_date + timedelta(days=day_offset, hours=(i // 5))
        if as_rfc3339:
            start = slot_time.isoformat() + 'Z'
            end = (slot_time + timedelta(minutes=30)).isoformat() + 'Z'
            slots.append({"start": start, "end": end, "display": slot_time.strftime("%A, %Y-%m-%d at %I:%M %p")})
        else:
            slots.append(slot_time.strftime("%A, %Y-%m-%d at %I:%M %p"))
    return slots
