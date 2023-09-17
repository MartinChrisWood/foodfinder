import re

from datetime import datetime as dt


DAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
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

    # Only need to detect days of week and times within a line
    for token in text:
        day = DAYS.get(token, None)

        if day:
            days.append(day)
        
        elif re.match(r"\d+\D\d\d", token):
            times.append(token)

    # Expand range of days to entry for each day
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
        i = (i+1) % 7    # Use modulo to iterate forward over week

    return opening_hours


def parse_times_entry(text: str) -> list[dict]:
    """
    Wrapper, really just splits lines and validates
    that something was read.
    """
    entries = []
    for line in text.split("\n"):
        entries = entries + parse_times_line(line)
    
    if len(entries) == 0:
        raise ValueError(f"Failing to read opening times from {text}")

    return entries


def sort_soonest(current: dt, times: list[dict]) -> list[dict]:
    """
    Sort the list of opening time dicts by soonest open.

    Args:
        current (dt): A datetime object from which to calculate
        times (list[dict]): list of opening time dicts, of
            form {'day': 1, 'open': '%H.%M', 'close': '%H.%M'}
    
    Returns:
        ordered list of dicts with original fields plus timedelta
            values 'oD' and 'cD', in seconds
    """
    # Create copy, avoid altering source
    opening_times = times.copy()

    for time in opening_times:
        # Get differences in seconds, modulo to positive-only
        day_delta = ( (time['day'] - current.weekday()) % 7 ) * 60 * 60 * 24
        open_delta = (day_delta + (dt.strptime(time['open'], "%H.%M") - dt.strptime(f"{current.hour}.{current.second}", "%H.%M")).total_seconds()) % (7*24*60*60)
        close_delta = (day_delta + (dt.strptime(time['close'], "%H.%M") - dt.strptime(f"{current.hour}.{current.second}", "%H.%M")).total_seconds()) % (7*24*60*60)
        time.update({"oD": open_delta, "cD": close_delta})

    # sort key is nearest closing time, then nearest opening time
    return sorted(opening_times, key = lambda x: min([x['oD'], x['cD']]))
