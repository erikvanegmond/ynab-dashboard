import plotly.express as px
import dash_core_components as dcc


def pie_chart(df, values, names):
    fig = px.pie(df, names=names, values=values)
    return dcc.Graph(figure=fig)
