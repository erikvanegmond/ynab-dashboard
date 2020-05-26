import dash_table


def table(df):
    return dash_table.DataTable(
        sort_action="native",
        sort_mode="multi",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native'
    )
