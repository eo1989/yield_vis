import dash
from dash_bootstrap_templates import load_figure_template
from utils import data_sources as ds
from utils.app_layout import create_layout

dash.register_page(__name__, path = "/", name = "U.S. Treasuries Yield Curve")


df = ds.get_us_yield_data()
source = "Data Source: FRED"
id_vars = "DATE"
low = '2-year'
high = '10-year'

load_figure_template("lux")
layout = create_layout(df = df, source = source, id_vars = id_vars, low = low, high = high)
