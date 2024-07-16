import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_system_power_data(tmp_dirname: str, ulog_filename: str):
    message_name = "system_power"

    system_power_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {system_power_count} system power data sets")

    figs = []

    for system_power_num in range(system_power_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, system_power_num))
        fix_timestamps(df)

        count_3v3_sensors = 4

        rows = 8
        subplot_titles = [
            "Voltage 5V",
            "Voltage 3.3V",
            "Sensors 3.3V valid",
            "Brick valid",
            "Servo valid",
            "5V overcurrent",
            "5V to companion valid",
            "CAN1/GPS1 5V valid",
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

        # Voltage 5V
        fig.add_trace(
            col=1,
            row=1,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["voltage5v_v"],
                mode="lines",
                name="Voltage 5V",
            ),
        )

        # Voltage 3.3V
        for m in range(count_3v3_sensors):
            fig.add_trace(
                col=1,
                row=2,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"sensors3v3[{m}]"],
                    mode="lines",
                    name=f"Voltage 3.3V [{m}]",
                ),
            )

        # Sensors 3.3V valid
        fig.add_trace(
            col=1,
            row=3,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["sensors3v3_valid"],
                mode="lines",
                name="Sensors 3.3V valid",
            ),
        )

        # Brick valid
        fig.add_trace(
            col=1,
            row=4,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["brick_valid"],
                mode="lines",
                name="Brick valid",
            ),
        )

        # Servo valid
        fig.add_trace(
            col=1,
            row=5,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["servo_valid"],
                mode="lines",
                name="Servo valid",
            ),
        )

        # 5V overcurrent
        fig.add_trace(
            col=1,
            row=6,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["periph_5v_oc"],
                mode="lines",
                name="Peripheral 5V overcurrent",
            ),
        )

        fig.add_trace(
            col=1,
            row=6,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["hipower_5v_oc"],
                mode="lines",
                name="High power peripheral 5V overcurrent",
            ),
        )

        # 5V to companion valid
        fig.add_trace(
            col=1,
            row=7,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["comp_5v_valid"],
                mode="lines",
                name="5V to companion valid",
            ),
        )

        # CAN1/GPS1 5V valid
        fig.add_trace(
            col=1,
            row=8,
            trace=go.Scatter(
                x=df["timestamp"],
                y=df["can1_gps1_5v_valid"],
                mode="lines",
                name="CAN1/GPS1 5V valid",
            ),
        )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"System power {system_power_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            xaxis3_showticklabels=True,
            xaxis4_showticklabels=True,
            xaxis5_showticklabels=True,
            xaxis6_showticklabels=True,
            xaxis7_showticklabels=True,
            xaxis8_showticklabels=True,
            yaxis={"ticksuffix": "V"},
            yaxis2={"ticksuffix": "V"},
        )

        figs.append(fig)

    return figs
