import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_vehicle_air_data_data(tmp_dirname: str, ulog_filename: str):
    message_name = "vehicle_air_data"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        rows = 3
        subplot_titles = [
            "Barometer altitude",
            "Barometer temperature",
            "Pressure",
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

        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"baro_alt_meter"],
                mode="lines",
                name=f"Barometer altitude",
            ),
        )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"baro_temp_celcius"],
                mode="lines",
                name=f"Barometer temperature",
            ),
        )

        fig.add_trace(
            col=1,
            row=3,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"baro_pressure_pa"],
                mode="lines",
                name=f"Barometer pressure",
            ),
        )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"Vehicle air data {dataset_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            xaxis3_showticklabels=True,
            yaxis={"ticksuffix": " m"},
            yaxis2={"ticksuffix": " °C"},
            yaxis3={"ticksuffix": " pa"},
        )

        figs.append(fig)

    return figs
