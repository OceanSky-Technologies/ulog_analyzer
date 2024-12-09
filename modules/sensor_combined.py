import logging
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_sensor_combined_data(tmp_dirname: str, ulog_filename: str):
    message_name = "sensor_combined"

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
            "Raw acceleration",
            "Frequency Analysis (X)",
            "Frequency Analysis (Y)",
            "Frequency Analysis (Z)",
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

        # Raw acceleration
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"accelerometer_m_s2[0]"],
                mode="lines",
                name=f"Raw acceleration X (m/s^2)",
            ),
        )
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"accelerometer_m_s2[1]"],
                mode="lines",
                name=f"Raw acceleration Y (m/s^2)",
            ),
        )
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=df[f"accelerometer_m_s2[2]"],
                mode="lines",
                name=f"Raw acceleration Z (m/s^2)",
            ),
        )

        # Perform FFTs
        df["time_seconds"] = (df[timestamp_field] - df[timestamp_field].iloc[0]).dt.total_seconds()
        sample_rate = 1 / np.mean(np.diff(df["time_seconds"]))  # Calculate sampling rate

        x_acceleration = df[f"accelerometer_m_s2[0]"].values
        y_acceleration = df[f"accelerometer_m_s2[1]"].values
        z_acceleration = df[f"accelerometer_m_s2[2]"].values
        fft_result_x = np.fft.fft(x_acceleration)
        fft_result_y = np.fft.fft(y_acceleration)
        fft_result_z = np.fft.fft(z_acceleration)
        frequencies_x = np.fft.fftfreq(len(fft_result_x), d=1 / sample_rate)
        frequencies_y = np.fft.fftfreq(len(fft_result_y), d=1 / sample_rate)
        frequencies_z = np.fft.fftfreq(len(fft_result_z), d=1 / sample_rate)

        # Consider only positive frequencies
        positive_frequencies_x = frequencies_x[: len(frequencies_x) // 2]
        positive_frequencies_y = frequencies_y[: len(frequencies_y) // 2]
        positive_frequencies_z = frequencies_z[: len(frequencies_z) // 2]
        fft_magnitude_x = np.abs(fft_result_x[: len(frequencies_x) // 2])
        fft_magnitude_y = np.abs(fft_result_y[: len(frequencies_y) // 2])
        fft_magnitude_z = np.abs(fft_result_z[: len(frequencies_z) // 2])

        # Add frequency analysis data
        fig.add_trace(
            go.Scatter(
                x=positive_frequencies_x,
                y=fft_magnitude_x,
                mode="lines",
                name="Frequency Analysis (X)",
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=positive_frequencies_y,
                y=fft_magnitude_y,
                mode="lines",
                name="Frequency Analysis (Y)",
            ),
            row=3,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=positive_frequencies_z,
                y=fft_magnitude_z,
                mode="lines",
                name="Frequency Analysis (Z)",
            ),
            row=4,
            col=1,
        )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"IMU raw {dataset_num}",
            xaxis2_title="Frequency (Hz)",
            yaxis2_title="Amplitude",
            xaxis3_title="Frequency (Hz)",
            yaxis3_title="Amplitude",
            xaxis4_title="Frequency (Hz)",
            yaxis4_title="Amplitude",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            xaxis3_showticklabels=True,
            xaxis4_showticklabels=True,
            yaxis={"ticksuffix": " deg/s"},
            yaxis2={"ticksuffix": " deg/s"},
            yaxis3={"ticksuffix": " deg/s"},
            yaxis4={"ticksuffix": " deg/s"},
        )

        figs.append(fig)

    return figs
