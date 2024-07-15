#!/usr/bin/env python3

"""
Visualize ulog files.
"""

import argparse
from datetime import UTC, datetime
import os
import time
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import subprocess
import tempfile
import logging
import pyulog
from plotly.subplots import make_subplots

from CustomFormatter import CustomFormatter

tmp_dirname = None
ulog_filename = None
start_timestamp_us = 0
logging_start_time_us = 0


def get_csv_file(message_name: str, multi_id: 0):
    output_file_prefix = ulog_filename
    # strip '.ulg'
    if output_file_prefix.lower().endswith(".ulg"):
        output_file_prefix = output_file_prefix[:-4]

    base_name = os.path.basename(output_file_prefix)
    output_file_prefix = os.path.join(tmp_dirname, base_name)

    fmt = "{0}_{1}_{2}.csv"
    return fmt.format(output_file_prefix, message_name, str(multi_id))


def timestamp_to_datetime(timestamp_us: int):
    return datetime.fromtimestamp(timestamp_us / 1000000, UTC).strftime("%Y-%m-%d %H:%M:%S")


def get_first_gps_timestamp(ulog: pyulog.ULog):
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


def fix_timestamps(df):
    """This function adjusts timestamps so they are in the local timezone."""

    # used to transform everything into local timezone
    utc_offset_us = int(time.timezone * 1000000)

    # calculate difference to first gps timestamp
    timestamp_gps_diff_microseconds = int(df["timestamp"][0] - start_timestamp_us)

    df["timestamp"] = pd.to_datetime(
        (df["timestamp"] - timestamp_gps_diff_microseconds + logging_start_time_us - utc_offset_us),
        unit="us",
    )


def read_esc_data():
    esc_num = 0
    message_name = "esc_status"

    # read in csvs
    df = pd.read_csv(get_csv_file(message_name, esc_num))
    fix_timestamps(df)

    motor_count = 4

    # esc[0].esc_errorcount,
    # esc[0].esc_rpm,
    # esc[0].esc_voltage,
    # esc[0].esc_current,
    # esc[0].esc_temperature,
    # esc[0].failures,
    # esc[0].esc_address,
    # esc[0].esc_cmdcount,
    # esc[0].esc_state,
    # esc[0].actuator_function,
    # esc[0].esc_power,

    fig = make_subplots(
        rows=8,
        cols=1,
        vertical_spacing=0.02,
        shared_xaxes=True,
        subplot_titles=[
            "ESC errorcount",
            "ESC RPM",
            "ESC temperature",
            "ESC voltage",
            "ESC current",
            "ESC failures",
            "ESC state",
            "ESC power",
        ],
    )

    for m in range(motor_count):
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].esc_errorcount"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    for m in range(motor_count):
        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].esc_rpm"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    for m in range(motor_count):
        # ESC reports negative temperature when it's not armed
        df[f"esc[{m}].esc_temperature"] = df[f"esc[{m}].esc_temperature"].abs()

        fig.add_trace(
            col=1,
            row=3,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].esc_temperature"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    for m in range(motor_count):
        fig.add_trace(
            col=1,
            row=4,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].esc_voltage"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    for m in range(motor_count):
        fig.add_trace(
            col=1,
            row=5,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].esc_current"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    for m in range(motor_count):
        fig.add_trace(
            col=1,
            row=6,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].failures"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    for m in range(motor_count):
        fig.add_trace(
            col=1,
            row=7,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].esc_state"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    for m in range(motor_count):
        fig.add_trace(
            col=1,
            row=8,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df[f"esc[{m}].esc_power"],
                mode="lines",
                name=f"Motor {m}",
            ),
        )

    fig.update_layout(title="ESC", height=4000)

    for i, yaxis in enumerate(fig.select_yaxes(), 1):
        legend_name = f"legend{i}"
        yaxis.exponentformat = "none"
        yaxis.separatethousands = True
        fig.update_layout(
            {legend_name: dict(y=yaxis.domain[1], yanchor="top")},
            showlegend=True,
        )
        fig.update_traces(row=i, legend=legend_name)

    # show x axis labels in every subplot
    fig.update_layout(
        xaxis_showticklabels=True,
        xaxis2_showticklabels=True,
        xaxis3_showticklabels=True,
        xaxis4_showticklabels=True,
        xaxis5_showticklabels=True,
        xaxis6_showticklabels=True,
        xaxis7_showticklabels=True,
        xaxis8_showticklabels=True,
    )

    return fig


def main():
    """Command line interface"""
    global ulog_filename, tmp_dirname

    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    parser = argparse.ArgumentParser(description="Plot ulog data")
    parser.add_argument("filename", metavar="file.ulg", help="ULog input file")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f'File "{args.filename}" doesn\'t exist.')
        exit(1)
    else:
        ulog_filename = args.filename

    ulog = pyulog.ULog(args.filename, None, True)
    get_first_gps_timestamp(ulog)

    delete_tmp_file_after_usage = True
    with tempfile.TemporaryDirectory(delete=delete_tmp_file_after_usage) as tmp_dirname:
        if not delete_tmp_file_after_usage:
            logging.info(f"CSV files: {tmp_dirname}")

        # convert ulog file to csvs
        cmd = f"ulog2csv -o {tmp_dirname} {args.filename}"
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            universal_newlines=True,
        )
        std_out, _ = proc.communicate()

        if proc.returncode:
            print("Couldn't convert ulog file to csv. Error:")
            print(std_out)
            exit(1)

        esc_fig = read_esc_data()
        esc_fig.show()


if __name__ == "__main__":
    main()
