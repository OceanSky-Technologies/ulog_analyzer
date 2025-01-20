import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_vehicle_gps_position_data(tmp_dirname: str, ulog_filename: str):
    message_name = "vehicle_gps_position"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        rows = 3
        subplot_titles = ["Altitude", "Velocity", "Raw data"]
        if len(subplot_titles) != rows:
            raise Exception("Number of subplots is wrong")

        fig = make_subplots(
            rows=rows,
            cols=1,
            vertical_spacing=0.075,
            shared_xaxes=True,
            subplot_titles=subplot_titles,
            specs=[[{}], [{}], [{"type": "table"}]],  # Specify table type for the last row
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

        # TODO: add more fields

        # Data Table
        columns = [
            "timestamp",
            "latitude_deg",
            "longitude_deg",
            "altitude_msl_m",
            "altitude_ellipsoid_m",
            "time_utc_usec",
            "eph",
            "epv",
            "hdop",
            "vdop",
            "noise_per_ms",
            "jamming_indicator",
            "vel_m_s",
            "heading",
            "heading_accuracy",
            "fix_type",
            "jamming_state",
            "satellites_used",
        ]
        fig.add_trace(
            go.Table(
                header=dict(
                    values=list(columns), fill_color="lightgrey", align="center", font=dict(size=12, color="black")
                ),
                cells=dict(
                    values=[df[col] for col in columns],
                    fill_color="white",
                    align="center",
                    font=dict(size=10, color="black"),
                ),
            ),
            row=3,
            col=1,
        )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"Vehicle GPS position {dataset_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            yaxis={"ticksuffix": " m"},
            yaxis2={"ticksuffix": " m/s"},
        )

        figs.append(fig)

    return figs
