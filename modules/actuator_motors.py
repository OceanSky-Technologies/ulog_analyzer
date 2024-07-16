import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_actuator_motors_data(tmp_dirname: str, ulog_filename: str):
    message_name = "actuator_motors"

    actuator_motors_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {actuator_motors_count} actuator/motor data sets")

    figs = []

    for actuator_motors_num in range(actuator_motors_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, actuator_motors_num))
        fix_timestamps(df)

        actuator_control_count = 12

        rows = 1
        subplot_titles = [
            "Actuator output",
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

        for m in range(actuator_control_count):
            fig.add_trace(
                col=1,
                row=1,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"control[{m}]"] * 100,
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"Actuator/motor control {actuator_motors_num}",
            autosize=True,
            xaxis_showticklabels=True,
            yaxis={"ticksuffix": "%"},
        )

        figs.append(fig)

    return figs
