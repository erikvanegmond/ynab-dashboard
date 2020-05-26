import plotly.graph_objects as go
import dash_core_components as dcc


def indicator(value=0, limit=200):
    fig = go.Figure(
        go.Indicator(
            mode="number+gauge", value=value,
            domain={'x': [0.1, 1], 'y': [0, 1]},
            title={'text': "<b>Rate limit</b>"},
            gauge={
                'shape': "bullet",
                'axis': {'range': [None, limit+10]},
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 0.75,
                    'value': 200},
                'steps': [
                    {'range': [0, 150], 'color': "lightgray"},
                    {'range': [150, limit+10], 'color': "gray"}]}
        )
    )
    fig.update_layout(
        height=50,
        margin=dict(
            l=100,
            r=10,
            b=10,
            t=10
        ),
    )
    return dcc.Graph(figure=fig)
