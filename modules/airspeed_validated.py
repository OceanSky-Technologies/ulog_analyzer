import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_airspeed_validated_data(tmp_dirname: str, ulog_filename: str):
    message_name = "airspeed_validated"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        rows = 4
        subplot_titles = [
            "Airspeed",
            "Ground minus wind",
            "Airspeed sensor measurement valid",
            "Selected airspeed index",
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

        # Airspeed
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"indicated_airspeed_m_s"],
                mode="lines",
                name=f"Indicated airspeed",
            ),
        )

        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"calibrated_airspeed_m_s"],
                mode="lines",
                name=f"Calibrated airspeed",
            ),
        )

        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"true_airspeed_m_s"],
                mode="lines",
                name=f"True airspeed",
            ),
        )

        # Ground minus wind
        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"calibrated_ground_minus_wind_m_s"],
                mode="lines",
                name=f"Calibrated ground minus wind",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"true_ground_minus_wind_m_s"],
                mode="lines",
                name=f"True ground minus wind",
            ),
        )

        # airspeed sensor measurement valid
        fig.add_trace(
            col=1,
            row=3,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"airspeed_sensor_measurement_valid"],
                mode="lines",
                name=f"Airspeed sensor measurement valid",
            ),
        )

        # Selected airspeed sensor index
        fig.add_trace(
            col=1,
            row=4,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"selected_airspeed_index"],
                mode="lines",
                name=f"Selected airspeed sensor index",
            ),
        )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"Airspeed (validated) {dataset_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            xaxis3_showticklabels=True,
            xaxis4_showticklabels=True,
            yaxis={"ticksuffix": " m/s"},
            yaxis2={"ticksuffix": " m/s"},
        )

        figs.append(fig)

    return figs
