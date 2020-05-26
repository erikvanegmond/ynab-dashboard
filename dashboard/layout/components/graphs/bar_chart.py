import plotly.express as px
import dash_core_components as dcc


def bar_chart(df, x="", y="", color=None):
    fig = px.bar(df, x=x, y=y, color=color)
    return dcc.Graph(figure=fig)
