import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_battery_data(tmp_dirname: str, ulog_filename: str):
    message_name = "battery_status"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        cell_count = 6

        rows = 7
        subplot_titles = [
            "Voltage",
            "Current",
            "Discharged",
            "Remaining",
            "Time remaining",
            "Temperature",
            "Cell voltage",
        ]
        if len(subplot_titles) != rows:
            raise Exception("Number of subplots is wrong")

        fig = make_subplots(
            rows=rows,
            cols=1,
            vertical_spacing=0.02,
            shared_xaxes=True,
            subplot_titles=subplot_titles,
        )

        # Voltage
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["voltage_v"],
                mode="lines",
                name="Voltage",
            ),
        )

        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["voltage_filtered_v"],
                mode="lines",
                name="Voltage (filtered)",
            ),
        )

        # Current
        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["current_a"],
                mode="lines",
                name="Current",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["current_filtered_a"],
                mode="lines",
                name="Current (filtered)",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["current_average_a"],
                mode="lines",
                name="Current (average)",
            ),
        )

        # Discharged mAh
        fig.add_trace(
            col=1,
            row=3,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["discharged_mah"],
                mode="lines",
                name="Discharged",
            ),
        )

        # Remaining
        fig.add_trace(
            col=1,
            row=4,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["remaining"] * 100,
                mode="lines",
                name="Remaining",
            ),
        )

        # Remaining*power scaling factor
        fig.add_trace(
            col=1,
            row=4,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["remaining"] * df["scale"] * 100,
                mode="lines",
                name="Remaining (incl. power scaling factor)",
            ),
        )

        # Time remaining
        fig.add_trace(
            col=1,
            row=5,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["time_remaining_s"],
                mode="lines",
                name="Time remaining",
            ),
        )

        # Temperature
        fig.add_trace(
            col=1,
            row=6,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df["temperature"],
                mode="lines",
                name="Temperature",
            ),
        )

        # cell voltages are not reported ...
        for x in range(cell_count):
            fig.add_trace(
                col=1,
                row=7,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"voltage_cell_v[{x}]"],
                    mode="lines",
                    name=f"Cell {x+1}",
                ),
            )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"Battery/power module {dataset_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            xaxis3_showticklabels=True,
            xaxis4_showticklabels=True,
            xaxis5_showticklabels=True,
            xaxis6_showticklabels=True,
            xaxis7_showticklabels=True,
            yaxis={"ticksuffix": "V"},
            yaxis2={"ticksuffix": "A"},
            yaxis3={"ticksuffix": "mAh"},
            yaxis4={"ticksuffix": "%"},
            yaxis5={"ticksuffix": "s"},
            yaxis6={"ticksuffix": "°C"},
            yaxis7={"ticksuffix": "V"},
        )

        figs.append(fig)

    return figs
