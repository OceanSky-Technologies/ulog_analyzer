import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_sensor_gps_data(tmp_dirname: str, ulog_filename: str):
    message_name = "sensor_gps"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp_sample"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        rows = 2
        subplot_titles = [
            "Altitude",
            "Velocity",
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

        # Altitude
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"altitude_msl_m"],
                mode="lines",
                name=f"Altitude",
            ),
        )

        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"altitude_ellipsoid_m"],
                mode="lines",
                name=f"Altitude ellipsoid",
            ),
        )

        # Velocity
        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"vel_m_s"],
                mode="lines",
                name=f"Velocity",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"vel_n_m_s"],
                mode="lines",
                name=f"Velocity N",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"vel_e_m_s"],
                mode="lines",
                name=f"Velocity E",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"vel_d_m_s"],
                mode="lines",
                name=f"Velocity D",
            ),
        )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"GPS sensor {dataset_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            yaxis={"ticksuffix": " m"},
            yaxis2={"ticksuffix": " m/s"},
        )

        figs.append(fig)

    return figs
