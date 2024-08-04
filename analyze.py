#!/usr/bin/env python3

"""
Visualize ulog files.
"""

import argparse
import os
import subprocess
import tempfile
import logging
from pyulog import ULog
from dash import Dash, html, dcc, Output, Input, callback
from plotly.graph_objects import Figure

from CustomFormatter import CustomFormatter
from modules.actuator_motors import read_actuator_motors_data
from modules.airspeed import read_airspeed_data
from modules.airspeed_validated import read_airspeed_validated_data
from modules.battery_status import read_battery_data
from modules.esc_status import read_esc_data
from modules.manual_control_setpoint import read_manual_control_setpoint_data
from modules.system_power import read_system_power_data
from modules.sensor_gps import read_sensor_gps_data
from modules.timestamp_helper import get_first_gps_timestamp
from modules.vehicle_air_data import read_vehicle_air_data_data
from modules.vehicle_gps_position import read_vehicle_gps_position_data
from modules.vehicle_local_position_setpoint import read_vehicle_local_position_setpoint_data
from modules.vehicle_thrust_setpoint import read_vehicle_thrust_setpoint_data

tmp_dirname = None
ulog_filename = None

subplot_height = 600

tab_figures = {}


def sanitize_fig_title(title: str):
    return title.text.lower().replace(" ", "-")


def add_figs_to_dash(figs: list[Figure], main_layout: html.Div):
    # unify subplot sizes
    for fig in figs:
        fig.update_layout(height=len(fig._get_subplot_rows_columns()[0]) * subplot_height)

    # make sure there is a tabs container
    tabs = [child for child in main_layout.children if isinstance(child, dcc.Tabs)]
    if len(tabs) != 1:
        raise Exception("There must be exactly one tab in the main div!")
    main_div_tabs = tabs[0].children

    # add separate tab for each figure
    for fig in figs:
        main_div_tabs.append(
            dcc.Tab(
                label=fig.layout.title.text,
                value=sanitize_fig_title(fig.layout.title),
            )
        )

        # save this figure in the tab_figures dictionary: {sanitized_fig_title: fig}
        tab_figures[sanitize_fig_title(fig.layout.title)] = fig

        # remove figure title because the tab name already contains it
        fig.layout.title.text = ""

    # by default select the first tab
    if len(tabs[0].children) > 0:
        tabs[0].value = tabs[0].children[0].value


@callback(Output("tabs-content-graph", "children"), Input("tabs-graph", "value"))
def render_content(tab):
    if tab in tab_figures.keys():
        return html.Div([dcc.Graph(figure=tab_figures[tab])])
    else:
        logging.error(f"Tab name {tab} not found in tab_figures!")


def main():
    """Command line interface"""
    global ulog_filename, tmp_dirname

    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    parser = argparse.ArgumentParser(description="Plot ulog data")
    parser.add_argument("filename", metavar="file.ulg", help="ULog input file")
    parser.add_argument("--keep-csv", "-k", action="store_true", help="Don't delete the temporary csv files.")
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f'File "{args.filename}" doesn\'t exist.')
        exit(1)
    elif not str(args.filename).endswith(".ulg"):
        print(f'File "{args.filename}" must be an *.ulg file.')
        exit(1)
    else:
        ulog_filename = args.filename

    ulog = ULog(args.filename, None, True)
    get_first_gps_timestamp(ulog)

    with tempfile.TemporaryDirectory(delete=not args.keep_csv) as tmp_dirname:
        if args.keep_csv:
            logging.info(f"CSV files: {tmp_dirname}")

        # convert ulog file to csvs
        cmd = f"ulog2csv -o {tmp_dirname} {args.filename}"
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            universal_newlines=True,
        )
        std_out, _ = proc.communicate()

        if proc.returncode:
            print("Couldn't convert ulog file to csv. Error:")
            print(std_out)
            exit(1)

        external_stylesheets = ["style.css"]
        app = Dash(name="ulog analyzer", external_stylesheets=external_stylesheets)

        app.layout = html.Div(
            id="main_div",
            children=[
                html.H1("ulog analyzer"),
                dcc.Tabs(
                    id="tabs-graph",
                    value="tabs-graph",
                    children=[],
                ),
                html.Div(id="tabs-content-graph"),
            ],
        )

        add_figs_to_dash(read_battery_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout)

        add_figs_to_dash(read_system_power_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout)

        add_figs_to_dash(read_esc_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout)

        add_figs_to_dash(read_actuator_motors_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout)

        add_figs_to_dash(
            read_manual_control_setpoint_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout
        )

        add_figs_to_dash(read_airspeed_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout)

        add_figs_to_dash(
            read_airspeed_validated_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout
        )

        # Data included in vehicle_gps_position (with even better accuracy)
        # add_figs_to_dash(read_sensor_gps_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout)

        add_figs_to_dash(
            read_vehicle_gps_position_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout
        )

        add_figs_to_dash(read_vehicle_air_data_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout)

        add_figs_to_dash(
            read_vehicle_local_position_setpoint_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout
        )

        add_figs_to_dash(
            read_vehicle_thrust_setpoint_data(tmp_dirname=tmp_dirname, ulog_filename=ulog_filename), app.layout
        )

        app.run(debug=True)


if __name__ == "__main__":
    main()
