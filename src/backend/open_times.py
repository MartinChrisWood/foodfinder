import re
from datetime import datetime
import numpy as np
import pandas as pd


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


def week_day_num(day):
    return str(weekdays.index(day) % 7 + 1)


def parse_open_times(df, col_in="Opening", col_id="Name"):
    df_out = df.apply(
        lambda x: pd.DataFrame(parse_opening_str(x[col_in], x[col_id])), axis=1
    ).to_list()

    df_out["day_start"] = pd.to_datetime(
        df_out["day"].apply(week_day_num) + "-" + df_out["start"],
        format="%d-%H.%M",
    )
    df_out["day_end"] = pd.to_datetime(
        df_out["day"].apply(week_day_num) + "-" + df_out["end"],
        format="%d-%H.%M",
    )

    return pd.concat(df_out)


def sort_by_time_to_open(df_out, time_now=datetime.now()):
    time_weird = pd.to_datetime(
        str(time_now.weekday() + 1) + "-" + datetime.now().strftime("%H.%M"),
        format="%d-%H.%M",
    )
    now_msk = (df_out["day_start"] <= time_weird) & (df_out["day_end"] >= time_weird)
    df_out["time_to_open"] = (df_out["day_start"] - time_weird) % np.timedelta64(7, "D")
    df_out.loc[now_msk, "time_to_open"] = np.timedelta64(0, "D")
    return df_out.sort_values("time_to_open")
