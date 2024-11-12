import dash

from utils import data_sources as ds


dash.register_page(__name__, path = '/', name = 'U.S. Treasuries Yield Curve')
