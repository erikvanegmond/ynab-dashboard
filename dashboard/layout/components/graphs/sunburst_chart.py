import plotly.express as px
import dash_core_components as dcc


def sunburst_chart(df, path, values):
    fig = px.sunburst(df, path=path, values=values)
    return dcc.Graph(figure=fig)
