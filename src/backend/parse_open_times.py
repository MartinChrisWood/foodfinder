import re

from datetime import datetime


DAYS = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 0
}

# In case of obvious variant in source
DAYS.update({day + "s": value for day, value in DAYS.items()})


def parse_times_line(text: str) -> list[dict]:
    """
    Given a single line of text describing
    opening hours of the formats:
    
        'Tuesday 11.00 - 13.00'
        
        'Friday 15.00-17.00'
        
        'Wednesday to Friday 11.30 - 14.30'
    
    Parse these and return a list of dicts of
    each unique open day / open time slot pair.

    Args:
        text (str): input to parse
    
    Returns:
        list of
        {'day': int, 'open': str, 'close': str, 'id': foodbank}
    """
    text = text.lower()
    text = re.sub("[^:0-9a-z .-]", "", text)
    text = re.split(r"[ -]", text)

    days = []
    times = []

    for token in text:
        day = DAYS.get(token, None)

        # Detect
        if day:
            days.append(day)
        
        if re.match(r"\d+\D\d\d", token):
            times.append(token)

    opening_hours = []
    i = days[0]

    while True:
        opening_hours.append(
            {"day": i,
             "open": times[0],
             "close": times[1]}
        )
        if i == days[-1]:
            break
        i = (i+1) % 7

    return opening_hours


if __name__ == "__main__":
    print(parse_times_line("Tuesday 11.00-13.00"))
    print(parse_times_line("Tuesday to Friday 11.00-13.00"))