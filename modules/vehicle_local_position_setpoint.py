import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_vehicle_local_position_setpoint_data(tmp_dirname: str, ulog_filename: str):
    message_name = "vehicle_local_position_setpoint"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        rows = 5
        subplot_titles = [
            "Position",
            "Acceleration",
            "Thrust",
            "Yaw",
            "Yawspeed",
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

        # Position
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"y"],
                mode="lines",
                name=f"Y",
            ),
        )

        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"y"],
                mode="lines",
                name=f"Y",
            ),
        )

        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"z"],
                mode="lines",
                name=f"Z",
            ),
        )

        # Acceleration
        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"acceleration[0]"],
                mode="lines",
                name=f"Acceleration (X)",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"acceleration[1]"],
                mode="lines",
                name=f"Acceleration (Y)",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"acceleration[2]"],
                mode="lines",
                name=f"Acceleration (Z)",
            ),
        )

        # Thrust
        fig.add_trace(
            col=1,
            row=3,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"thrust[0]"] * 100,
                mode="lines",
                name=f"Thrust (up)",
            ),
        )

        if "thrust[1]" in df.keys():
            fig.add_trace(
                col=1,
                row=3,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"thrust[1]"] * 100,
                    mode="lines",
                    name=f"Thrust (forward)",
                ),
            )

        # Yaw
        fig.add_trace(
            col=1,
            row=4,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"yaw"],
                mode="lines",
                name=f"Yaw",
            ),
        )

        # Yawspeed
        fig.add_trace(
            col=1,
            row=5,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"yawspeed"],
                mode="lines",
                name=f"Yawspeed",
            ),
        )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"Vehicle local position setpoint {dataset_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            xaxis3_showticklabels=True,
            xaxis4_showticklabels=True,
            xaxis5_showticklabels=True,
            yaxis={"ticksuffix": " m"},
            yaxis2={"ticksuffix": " m/s"},
            yaxis3={"ticksuffix": " %"},
            yaxis4={"ticksuffix": " °"},
            yaxis5={"ticksuffix": " m/s"},
        )

        figs.append(fig)

    return figs
