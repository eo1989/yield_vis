import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from utils.styles import CONTENT_INTRO, CONTENT_STYLE


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
app = dash.Dash(
    __name__,
	external_stylesheets = [dbc.themes.SPACELAB, dbc_css],
    meta_tags = [{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}],
    use_pages = True,
)

server = app.server
load_figure_template("lux")

title = html.H1(
	children = 'Yield Curves Visualization',
	className="text-center mt-4",
    stlye = { 'fontSize': 30 }
)

## =========== Modal ===========
with open('learn.md', 'r') as f:
    modal_content = f.read()

_modal_overlay = dbc.Modal(
    [
        dbc.ModalBody(html.Div([dcc.Markdown(modal_content)], id="how-to-md")),
        dbc.ModalFooter(dbc.Button("Close", id = "how-to-close", className = "how-to-bn")),
    ],
    id = "modal",
    size = "lg",
)

_button_howto = dbc.Button(
    "Learn More",
    id = "how-to-open",
    outline = True,
    color = "info",
    # disallow lowercase transformation for the class .button in the stylesheet
    style = {"textTransform": "none"},
)

_button_github = dbc.Button(
    "Github Repo",
    outline=True,
    color="primary",
    href = "https://github.com/eo1989/yield_vis",
    id = "gh-link",
    style={"text-transform": "none"},
)

# headers
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        # html.Img(id = 'logo', src = app.get_asset_url('dash-logo-new.png'), height = '30px'), md = 'auto',
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H4("Yield Curves Visualization"),
                                    html.P(dcc.Markdown("By [eo1989](https://github.com/eo1989)")),
                                ],
                                id = 'app-title',
                            )
                        ],
                        md="auto",
                        align="center",
                    ),
                ],
                align="center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.NavbarToggler(id = "navbar-toggler"),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavItem(_button_howto),
                                        dbc.NavItem(_button_github),
                                    ],
                                    navbar = True,
                                ),
                                id = "navbar-collapse",
                                navbar = True,
                            ),
                            _modal_overlay,
                        ],
                        # md = "2",
                    ),
                ],
                align="center",
            ),
        ],
        fluid=True,
    ),
    dark = False,
)

# Description
description = dbc.Col(
    [
        dbc.Card(
            id = "description-card",
            children = [
                dbc.CardHeader("Explanation"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(
                                            src = "assets/segmentation_img_example_marks.jpg",
                                            width = "200px",
                                        )
                                    ],
                                    md = "auto",
                                ),
                                dbc.Col(
                                    html.P(
                                        "This is an example of interactive machine learning for image classification. "
                                        "To train the classifier, draw some marks on the picture using different "
                                        "colors for "
                                        'different parts, like in the example image. Then enable "Show segmentation" '
                                        'to see the '
                                        "classes a Random Forest Classifier gave to regions of the image, based on the "
                                        "marks you "
                                        "used as a guide. You may add more marks to clarify parts of the image where "
                                        "the "
                                        "classifier was not successful and the classification will update."
                                    ),
                                    md = True,
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        )
    ],
    md = 12,
)

app.layout = html.Div(
    children = [
        header,
        dbc.Container(
            dbc.Row(
                [
                    html.Div(
                        id = 'yield-curve-101',
                        children = [
                            dcc.Markdown('''
                ---

                **Yield Curve 101**

                The yield curve shows how much it costs the federal
                government to borrow money
                for a given amount of time, revealing the relationship between long- and short-term
                interest rates.

                It is, inherently, a forecast for what the economy holds in the
                future — how much inflation there will be, for example, and how healthy growth will
                be over the years ahead — all embodied in the price of money today, tomorrow and
                many years from now.

                — *The New York Times (2015)*.

                ---
                        ''')
                        ],
                        className = 'text-justify mt-4', style = {'fontSize': 15}
                    )
                ]
            ),
            fluid = True,
            style = CONTENT_INTRO,
            class_name = 'dbc',
        ),
        dbc.Row(
            [
                html.Div(
                    id = 'button',
                    children = [
                        dbc.Button(
                            page["name"],
                            href = page["path"],
                            outline = True,
                            color = "dark",
                            className = "me-1",
                        )
                        for page in dash.page_registry.values()
                    ],
                    className = "text-center mt-4 mb-4", style = {'fontSize': 10}
                )
            ]
        ),
        dbc.Spinner(
            dash.page_container,
            fullscreen = True,
            show_initially = True,
            delay_hide = 600,
            type="grow",
            spinner_style={"width": "3rem", "height": "3rem"}
        ),
        html.Br(),
        dbc.Container(
            dbc.Row(
                [
                    html.Div(
                        id = "text-container1",
                        children = [
                            dcc.Markdown(
                                """
                                If you like this project, please give it a star
                                in [GitHub](https://github.com/eo1989/yield_vis) :)
                                """
                            )
                        ],
                        className='text-center mt-4', style = {'fontSize': 15}
                    )
                ]
            ),
            fluid=True,
            style=CONTENT_INTRO,
            class_name='dbc',
        ),
        # dbc.Container(
        #     dbc.Row(
        #         [
        #             html.Div(
        #                 id = "about-me",
        #             )
        #         ]
        #     )
        # )
    ]
)
# cb for modal popup
@app.callback(
    Output("modal", "is_open"),
    [Input("how-to-open", "n_clicks"), Input("how-to-close", "n_clicks")],
    [State("modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == "__main__":
    server = app.server
app.run_server(
    debug = False,
    host = '0.0.0.0',
    port = 10000
)
