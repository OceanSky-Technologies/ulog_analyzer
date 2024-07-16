from plotly.graph_objects import Figure


def format_figure(fig: Figure):
    for i, yaxis in enumerate(fig.select_yaxes(), 1):
        legend_name = f"legend{i}"
        yaxis.exponentformat = "none"
        yaxis.separatethousands = True
        fig.update_layout(
            {legend_name: dict(y=yaxis.domain[1], yanchor="top")},
            showlegend=True,
        )
        fig.update_traces(row=i, legend=legend_name)
