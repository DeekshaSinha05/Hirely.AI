from datetime import datetime, timedelta

def suggest_interview_slots(num_candidates):
    base_date = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    slots = []
    for i in range(num_candidates):
        day_offset = i % 5  # Weekdays only
        slot_time = base_date + timedelta(days=day_offset, hours=(i // 5))
        slots.append(slot_time.strftime("%A, %Y-%m-%d at %I:%M %p"))
    return slots
