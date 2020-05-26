import plotly.express as px
import dash_core_components as dcc


def line_chart(df, x="", y="", color=""):
    fig = px.line(df, x=x, y=y, line_shape="spline")
    return dcc.Graph(figure=fig)
