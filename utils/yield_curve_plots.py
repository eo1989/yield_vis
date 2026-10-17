import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_yield_surface(df: pd.DataFrame, source_text: str):
	radius = 1.65
	last_col = df.columns[-1]
	x = [last_col] * len(df.index)
	y = df.index
	z = df[last_col]

	fig = go.Figure()
	fig.add_trace(
		go.Surface(
			x=df.columns,
			y=df.index,
			z=df.values,
			contours={
				"x": {
					"show": True,
					"color": "lightblue",
					"size": 0.01,
					"project": {"x": False, "y": False, "z": False},
				},
				"y": {
					"show": True,
					"color": "lightblue",
					"size": 0.01,
					"highlight": True,
				},
				"z": {"show": False, "highlight": False},
			},
			# opacity = 0.99,
			connectgaps=False,
			colorscale="ice",
			cmin=3,
			showscale=False,
			reversescale=True,
			hovertemplate="<br>Date: %{y}"
			+ "<br>Maturity: %{x}"
			+ "<br>Yield: %{z:.2f}<extra></extra>",
		)
	)

	fig.add_trace(
		go.Scatter3d(
			x=x, y=y, z=z, mode="lines", line={"color": "black", "width": 1.5}
		)
	)

	fig.update_layout(
		title="A 3D view of a Chart Which Predicts<br> The Economy Future: "
		'The Yield Curve<br><span style = "font-size: 12px;">By EO</span>',
		title_font={"size": 20},
		title_x=0.5,
		autosize=True,
		height=900,
		hovermode="closest",
		scene={
			"aspectratio": {"x": 1, "y": 1.75, "z": 0.75},
			"camera": {
				"eye": {
					"x": 1.0 * radius,
					"y": 0.95 * radius,
					"z": 0.15 * radius,
				}
			},
			"xaxis": {"zeroline": False, "showspikes": False, "showline": True},
			"yaxis": {"zeroline": False, "showspikes": False, "showline": True},
			"zaxis": {"showspikes": False, "showline": True},
			"xaxis_title": "",
			"yaxis_title": "",
			"zaxis_title": "",
		},
		margin={"l": 0, "r": 0, "b": 10, "t": 40},
		annotations=[
			{
				"text": source_text,
				"x": 0.0,
				"y": 0.1,
				"align": "right",
				"xref": "paper",
				"yref": "paper",
				"showarrow": False,
			}
		],
	)
	fig.update_layout(showlegend=False)
	fig.update_annotations(font={"family": "Helvetica", "size": 12})
	return fig


def plot_heatmap(df: pd.DataFrame, source_text: str):
	data = df.T
	data = data.iloc[::-1]
	fig = go.Figure(
		data=[
			go.Heatmap(
				z=data.values,
				x=data.columns,
				y=data.index,
				colorscale="ice",
				zmin=-3,
				showscale=True,
				reversescale=True,
				hovertemplate="<br>Date: %{x}"
				+ "<br>Maturity: %{y}"
				+ "<br>Yield: %{z:.2f}<extra></extra>",
			)
		]
	)

	fig.update_xaxes(title=None)
	fig.update_layout(
		title="A Heatmap of the Yield Curve Evolution over Time"
		'<br><span style = "font-size: 12px;">This corresponds to the 3D surface '
		"viewed from above</span>",
		title_x=0.5,
		title_font={"size": 18},
		autosize=True,
		height=600,
		coloraxis_showscale=False,
		margin={"t": 70, "b": 90, "l": 20, "r": 20},
		annotations=[
			{
				"text": source_text,
				"x": 0,
				"y": -0.15,
				"xref": "paper",
				"yref": "paper",
				"showarrow": False,
			}
		],
	)
	return fig


# def tenor_to_years(tenor: str) -> float:
# 	tenor = tenor.strip().upper()
# 	value, unit = tenor[:-1], tenor[-1:]
# 	match unit:
# 		case "Y":
# 			return float(value)
# 		case "M":
# 			return float(value) / 12
# 		case _:
# 			raise ValueError(f"Invalid tenor format: {tenor}")


def tenor_to_years(tenor: str) -> float:
	"""
	Convert a tenor string like "40Y", "6M", "1.5Y" into a float in years.
	Supports:
		- Years: 'Y' (eg '40Y' -> 40.0)
		- Months: 'M' (eg '6M' -> 0.5)
	"""

	tenor = tenor.strip().upper()

	if tenor.endswith("Y"):
		return float(tenor[:-1])
	elif tenor.endswith("M"):
		return float(tenor[:-1]) / 12
	else:
		raise ValueError(f"Invalid tenor format: {tenor}")


# def tenor_to_years_vectorized(tenor_series: pd.Series) -> pd.Series:
# 	normalized = (
# 		tenor_series
# 		.astype("string")
# 		.str.lower()
# 		.str.replace(r"[ _]", "", regex=True)
# 	)
#
# 	components = normalized.str.extract(
# 		r"^(?P<value>\d+(?:\.\d+)?)-?(?<unit>years?|y|months?|m)$"
# 	)
#
# 	invalid = normalized.notna() & components.isna().any(axis="columns")
#
# 	if invalid.any():
# 		invalid_values = normalized[invalid].tolist()
# 		raise ValueError(f"Invalid tenor format: {invalid_values}")
#
# 	values = pd.to_numeric(components["value"])
#
# 	conversion_factors = components["unit"].map({
# 		"y": 1.0,
# 		"year": 1.0,
# 		"years": 1.0,
# 		"m": 1 / 12,
# 		"month": 1 / 12,
# 		"months": 1 / 12,
# 	})
# 	return values.mul(conversion_factors).astype(float)


def tenor_to_years_vectorized(tenor_series: pd.Series) -> pd.Series:
	"""
	Vectorized conversion of a pandas Series of tenor strings to float years.
	Supports:
		- '50Y', '39.5Y', '6M'
		- '30-year', '6-month'
	"""

	s = tenor_series.str.lower().str.replace(r"[ _]", "", regex=True)

	result = pd.Series(np.nan, index=s.index, dtype=float)

	# yera formats
	mask_year = s.str.contains("year") | s.str.endswith("y")
	result[mask_year] = (
		s[mask_year]
		.str.replace(r"-?year?$", "", regex=True)
		.str.replace("y", "", regex=False)
		.astype(float)
	)

	# month formats
	mask_month = s.str.contains("month") | s.str.endswith("m")
	result[mask_month] = (
		s[mask_month]
		.str.replace(r"-?month?$", "", regex=True)
		.str.replace("m", "", regex=False)
		.astype(float)
		/ 12
	)

	return result


def prep_data_historical_yc(df, id_vars="DATE"):

	df_rev = df.iloc[:, ::-1]

	tabular_df = pd.melt(
		df_rev.reset_index(),
		id_vars=id_vars,
		value_vars=df_rev.columns,
		var_name="Maturity",
		value_name="Yield",
	)

	tabular_df["Color"] = ["blue"] * len(tabular_df)

	tabular_df["Maturity"] = tenor_to_years_vectorized(tabular_df["Maturity"])

	tabular_df[id_vars] = tabular_df[id_vars].dt.strftime("%b-%Y")
	return tabular_df


def plot_historical_yield_curve(df, source_text, id_vars="DATE"):

	tabular_df = prep_data_historical_yc(df, id_vars)

	first_date = tabular_df[id_vars].iloc[0]
	last_date = tabular_df[id_vars].iloc[-1]

	max_yield = tabular_df.Yield.max()
	min_yield = tabular_df.Yield.min()

	fig = px.line(
		tabular_df,
		x="Maturity",
		y="Yield",
		labels={"Color": "", "Maturity": "Maturity", "Yield": "Yield"},
		color=id_vars,
		color_discrete_sequence=["cornflowerblue"],
		animation_frame=id_vars,
		animation_group="Maturity",
		range_y=[int(min_yield), int(max_yield) + 2],
		markers="*",
		hover_data={
			"Maturity": True,
			"Yield": True,
			id_vars: True,
			"Color": False,
		},
	)

	latest_curve = tabular_df[tabular_df[id_vars] == last_date]

	fig.add_trace(
		go.Scatter(
			x=latest_curve.Maturity, y=latest_curve.Yield, name=f"{last_date}"
		)
	)

	fig.update_layout(
		title="An Animation of the Yield Curve Over Time <br> "
		f'<span style = "font-size: 12px;">{first_date} to {last_date}</span>',
		title_font={"size": 18},
		title_x=0.5,
		# autosize=True,
		height=700,
		margin={"t": 70, "b": 90, "l": 50, "r": 50},
		legend_title="",
		legend={"yanchor": "top", "y": 0.99, "xanchor": "right", "x": 0.99},
		annotations=[
			{
				"text": source_text,
				"x": 0,
				"y": -0.15,
				"xref": "paper",
				"yref": "paper",
				"showarrow": False,
			}
		],
	)

	for step in fig.layout.sliders[0].steps:
		step["args"][1]["frame"]["redraw"] = True

	for button in fig.layout.updatemenus[0].buttons:
		button["args"][1]["frame"]["redraw"] = True
		button["args"][1]["frame"]["duration"] = 200

	return fig


def plot_line_spread(df, idx, low, high, source_text):
	data = df.copy()
	data["Spread"] = df[high] - df[low]
	# data['Inverted'] = np.where(data['Spread'] < 0, 1, 0)
	mask = data["Spread"] <= 0
	data["Spread_above"] = np.where(mask, data["Spread"], 0)
	data["Spread_below"] = np.where(mask, 0, data["Spread"])
	fig = px.area(
		data.reset_index(), x=idx, y="Spread", hover_data={"Spread": True}
	)
	fig.add_trace(
		go.Scatter(
			x=data.index,
			y=data["Spread_above"],
			fill="tozeroy",
			mode="none",
			name="Inverted",
		)
	)
	fig.add_trace(
		go.Scatter(
			x=data.index,
			y=data["Spread_below"],
			fill="tozeroy",
			mode="none",
			name="Normal",
		)
	)
	fig.update_xaxes(title=None)

	fig.update_layout(
		title=f'A Visualisation of the Yield Spread<br><span style="font-size: 12px;"> '
		f"Difference (%) between the {high} and the {low} Yields<span>",
		title_font={"size": 18},
		title_x=0.5,
		autosize=True,
		height=550,
		margin={"t": 60, "b": 90, "l": 20, "r": 20},
		annotations=[
			{
				"text": source_text,
				"x": 0,
				"y": -0.15,
				"xref": "paper",
				"yref": "paper",
				"showarrow": False,
			}
		],
	)

	fig.update_layout(showlegend=False)
	return fig
