import plotly.express as px
import dash_core_components as dcc
import plotly.graph_objects as go


def networth_chart(balances, group=None, frequency="M"):
    fig = px.bar(balances, x="date", y="running_balance", color=group)
    networth = balances.resample(frequency, on="date")["running_balance"].sum()
    fig.add_trace(
        go.Scatter(x=networth.index,
                   y=networth.values,
                   line={'color': '#86c7f0'},
                   mode="markers+lines",
                   name="Networth")
    )
    return dcc.Graph(figure=fig)
