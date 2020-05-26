import plotly.express as px
import dash_core_components as dcc


def area_chart(df, x="", y="", color=""):
    fig = px.area(df, x=x, y=y, color=color,
                  line_group=color)
    return dcc.Graph(figure=fig)
