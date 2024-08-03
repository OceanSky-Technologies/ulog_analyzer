import logging
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from modules.csv_reader import get_csv_file, get_multi_id_num
from modules.figure_formatter import format_figure
from modules.timestamp_helper import fix_timestamps


def read_esc_data(tmp_dirname: str, ulog_filename: str):
    message_name = "esc_status"

    dataset_count = get_multi_id_num(tmp_dirname, message_name)
    logging.info(f"Found {dataset_count} {message_name} data sets")

    timestamp_field = "timestamp"

    figs = []

    for dataset_num in range(dataset_count):
        # read in csv
        df = pd.read_csv(get_csv_file(tmp_dirname, ulog_filename, message_name, dataset_num))
        fix_timestamps(df, timestamp_field)

        motor_count = 4

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

        for x in range(motor_count):
            fig.add_trace(
                col=1,
                row=1,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].esc_errorcount"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        for x in range(motor_count):
            fig.add_trace(
                col=1,
                row=2,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].esc_rpm"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        fig.add_trace(
            col=1,
            row=2,
            trace=go.Scatter(
                x=df[timestamp_field],
                y=sum([df[f"esc[{x}].esc_rpm"] for x in range(motor_count)]),
                mode="lines",
                name=f"Total motor RPM",
                visible="legendonly",
            ),
        )

        for x in range(motor_count):
            # ESC reports negative temperature when it's not armed
            df[f"esc[{x}].esc_temperature"] = df[f"esc[{x}].esc_temperature"].abs()

            fig.add_trace(
                col=1,
                row=3,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].esc_temperature"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        for x in range(motor_count):
            fig.add_trace(
                col=1,
                row=4,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].esc_voltage"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        for x in range(motor_count):
            fig.add_trace(
                col=1,
                row=5,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].esc_current"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        for x in range(motor_count):
            fig.add_trace(
                col=1,
                row=6,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].failures"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        for x in range(motor_count):
            fig.add_trace(
                col=1,
                row=7,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].esc_state"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        for x in range(motor_count):
            fig.add_trace(
                col=1,
                row=8,
                trace=go.Scatter(
                    x=df[timestamp_field],
                    y=df[f"esc[{x}].esc_power"],
                    mode="lines",
                    name=f"Motor {x+1}",
                ),
            )

        format_figure(fig)

        # show x axis labels in every subplot
        fig.update_layout(
            title_text=f"ESC {dataset_num}",
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
