from datetime import UTC, datetime
import logging
import numpy as np
from pyulog import ULog
import time

import pandas as pd

start_timestamp_us = 0
logging_start_time_us = 0


def timestamp_to_datetime(timestamp_us: int):
    return datetime.fromtimestamp(timestamp_us / 1000000, UTC).strftime("%Y-%m-%d %H:%M:%S")


def get_first_gps_timestamp(ulog: ULog):
    """This function tries to identify the first GPS timestamp."""
    global logging_start_time_us, start_timestamp_us

    gps_data = ulog.get_dataset("vehicle_gps_position")
    indices = np.nonzero(gps_data.data["time_utc_usec"])
    if len(indices[0]) > 0:
        logging_start_time_us = gps_data.data["time_utc_usec"][indices[0][0]]
        start_timestamp_us = gps_data.data["timestamp"][indices[0][0]]
        logging.info(f"First GPS timestamp found: {timestamp_to_datetime(logging_start_time_us)}")
    else:
        logging.warning("No GPS timestamp found!")


def fix_timestamps(df, timestamp_field):
    """This function adjusts timestamps so they are in the local timezone."""

    if start_timestamp_us == 0 or logging_start_time_us == 0:
        logging.warning("GPS timestamps not found, can't fix timestamp offsets.")
        return

    # used to transform everything into local timezone
    utc_offset_us = int(time.timezone * 1000000)

    # calculate difference to first gps timestamp
    timestamp_gps_diff_microseconds = int(df[timestamp_field][0] - start_timestamp_us)

    df[timestamp_field] = pd.to_datetime(
        (df[timestamp_field] - timestamp_gps_diff_microseconds + logging_start_time_us - utc_offset_us),
        unit="us",
    )
