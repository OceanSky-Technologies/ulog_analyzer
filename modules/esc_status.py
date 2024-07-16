import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_esc_data(tmp_dirname: str, ulog_filename: str):
    message_name = "esc_status"

    esc_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {esc_count} ESC data sets")

    figs = []

    for esc_num in range(esc_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, esc_num))
        fix_timestamps(df)

        motor_count = 4

        # esc[0].esc_errorcount,
        # esc[0].esc_rpm,
        # esc[0].esc_voltage,
        # esc[0].esc_current,
        # esc[0].esc_temperature,
        # esc[0].failures,
        # esc[0].esc_address,
        # esc[0].esc_cmdcount,
        # esc[0].esc_state,
        # esc[0].actuator_function,
        # esc[0].esc_power,

        rows = 8
        subplot_titles = [
            "Error count",
            "RPM",
            "Temperature",
            "Voltage",
            "Current",
            "Failures",
            "State",
            "Power",
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

        for m in range(motor_count):
            fig.add_trace(
                col=1,
                row=1,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].esc_errorcount"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        for m in range(motor_count):
            fig.add_trace(
                col=1,
                row=2,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].esc_rpm"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df["timestamp"],
                y=sum([df[f"esc[{m}].esc_rpm"] for m in range(motor_count)]),
                mode="lines",
                name=f"Total motor RPM",
            ),
        )

        for m in range(motor_count):
            # ESC reports negative temperature when it's not armed
            df[f"esc[{m}].esc_temperature"] = df[f"esc[{m}].esc_temperature"].abs()

            fig.add_trace(
                col=1,
                row=3,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].esc_temperature"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        for m in range(motor_count):
            fig.add_trace(
                col=1,
                row=4,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].esc_voltage"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        for m in range(motor_count):
            fig.add_trace(
                col=1,
                row=5,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].esc_current"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        for m in range(motor_count):
            fig.add_trace(
                col=1,
                row=6,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].failures"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        for m in range(motor_count):
            fig.add_trace(
                col=1,
                row=7,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].esc_state"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        for m in range(motor_count):
            fig.add_trace(
                col=1,
                row=8,
                trace=go.Scatter(
                    x=df["timestamp"],
                    y=df[f"esc[{m}].esc_power"],
                    mode="lines",
                    name=f"Motor {m}",
                ),
            )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"ESC {esc_num}",
            autosize=True,
            xaxis_showticklabels=True,
            xaxis2_showticklabels=True,
            xaxis3_showticklabels=True,
            xaxis4_showticklabels=True,
            xaxis5_showticklabels=True,
            xaxis6_showticklabels=True,
            xaxis7_showticklabels=True,
            xaxis8_showticklabels=True,
            yaxis2={"ticksuffix": " RPM"},
            yaxis3={"ticksuffix": "°C"},
            yaxis4={"ticksuffix": "V"},
            yaxis5={"ticksuffix": "A"},
            yaxis7={"ticksuffix": "V"},
            yaxis8={"ticksuffix": "%"},
        )

        figs.append(fig)

    return figs
