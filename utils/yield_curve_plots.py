import plotly.express as px    
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def plot_yield_surface(df: pd.DataFrame, source_text: str):
    radius = 1.65
    last_col = df.columns[-1]
    x = [last_col] * len(df.index)
    y = df.index
    z = df[last_col]

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x = df.columns,
            y = df.index,
            z = df.values,
            contours = {"x": {"show": True, "color": "lightblue", "size": 0.01,
                              "project": {"x": False, "y": False, "z": False}
                            },
                        "y": {"show": True, "color": "lightblue", "size": 0.01, "highlight": True},
                        "z": {"show": False, "highlight": False}
                    },
            # opacity = 0.99,
            connectgaps=False,
            colorscale='ice',
            cmin = 3,
            showscale = False,
            reversescale=True,
            hovertemplate='<br>Date: %{y}' + '<br>Maturity: %{x}' + '<br>Yield: %{z:.2f}<extra></extra>',
        )
    )
    
    fig.add_trace(
        go.Scatter3d(
            x = x,
            y = y,
            z = z,
            mode = 'lines',
            line = dict(
                color = 'black',
                width = 1.5,
            ),
        )
    )
    
    fig.update_layout(
        title = 'A 3D view of a Chart Which Predicts<br> The Economy Future: '
                'The Yield Curve<br><span style="font-size: 12px;">By EO</span>',     
        title_font = dict(size = 20),
        title_x = 0.5,
        autosize = True,
        height = 900,
        hovermode = 'closest',
        scene = {
            'aspectratio': {"x": 1, "y": 1.75, "z": 0.75},
            'camera': {
                'eye': {'x': 1.0 * radius, 'y': 0.95 * radius, 'z': 0.15 * radius},
            },
            'xaxis': {'zeroline': False, "showspikes": False, "showLine": True},
            'yaxis': {'zeroline': False, "showspikes": False, "showLine": True},
            'zaxis': {"showspikes": False, "showLine": True},
            'xaxis_title': '',
            'yaxis_title': '',
            'zaxis_title': ''
        },
        margin = dict(l = 0, r = 0, b = 10, t = 40),
        annotations = [
            dict(
                text = source_text,
                x = 0.0,
                y = 0.1,
                align = 'right',
                xref = 'paper',
                yref = 'paper',
                showarrow = False,
            )
        ]
    )
    fig.update_layout(showlegend = False)
    fig.update_annotations(font = dict(family = 'Helvetica', size = 12))
    return fig


def plot_heatmap(df: pd.DataFrame, source_text: str):
    data = df.T
    data = data.iloc[::-1]