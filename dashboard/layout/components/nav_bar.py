# NAVBAR
from config_pages import config_pages
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app



def nav_bar(name, brand="Brand"):
    # PLOTLY_LOGO = "assets/"

    nav_items = [
        dbc.NavItem(
            dbc.NavLink(page['name'], href=page['link'][0])
        )
        for page_id, page in config_pages.items()
    ]

    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand(brand, className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),

                dbc.Collapse(

                    dbc.Nav(
                        nav_items, className="ml-auto", navbar=True
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]
        ),
        color="light",
        dark=False,
        sticky='top',
    )
    return navbar


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
