import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_vehicle_thrust_setpoint_data(tmp_dirname: str, ulog_filename: str):
    message_name = "vehicle_thrust_setpoint"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp_sample"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        rows = 1
        subplot_titles = [
            "Thrust",
        ]
        if len(subplot_titles) != rows:
            raise Exception("Number of subplots is wrong")

        fig = make_subplots(
            rows=rows,
            cols=1,
            vertical_spacing=0.075,
            shared_xaxes=True,
            subplot_titles=subplot_titles,
        )

        # xyz
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=abs(df[f"xyz[0]"] * 100),
                mode="lines",
                name=f"Thrust (forward)",
            ),
        )

        if "xyz[1]" in df.keys():
            fig.add_trace(
                col=1,
                row=1,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=abs(df[f"xyz[1]"] * 100),
                    mode="lines",
                    name=f"Thrust (right)",
                ),
            )

        if "xyz[2]" in df.keys():
            fig.add_trace(
                col=1,
                row=1,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=abs(df[f"xyz[2]"] * 100),
                    mode="lines",
                    name=f"Thrust (up)",
                ),
            )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"Vehicle thrust setpoint {dataset_num}",
            autosize=True,
            xaxis_showticklabels=True,
            yaxis={"ticksuffix": " %"},
        )

        figs.append(fig)

    return figs
