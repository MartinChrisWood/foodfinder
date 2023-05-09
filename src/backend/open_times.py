import pandas as pd
import re


Days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
Days = Days + [x + "s" for x in Days]
DAYS = [x.upper() for x in Days]
days = [x.lower() for x in Days]
weekdays = Days + DAYS + days


def parse_opening_str(text, id_name):
    row_list = []
    result = re.search(
        f"({'|'.join(weekdays)})"
        + r" *([0-9\.:]+) *[-–]? *([0-9\.:]+)\n?(.*)",  # noqa:W605
        text,
    )
    if result:
        if len(result.groups()) > 3:
            row_list = parse_opening_str(result.groups()[3], id_name)
        row_list.append(
            {
                "id": id_name,
                "day": result.groups()[0],
                "start": result.groups()[1],
                "end": result.groups()[2],
            }
        )
    return row_list


def parse_open_times(df, col_in="Opening", col_id="Name"):
    df_out = df.apply(
        lambda x: pd.DataFrame(parse_opening_str(x[col_in], x[col_id])), axis=1
    ).to_list()
    # next step: convert times

    return pd.concat(df_out)
