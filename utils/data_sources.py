import logging
import os
import pathlib

import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
from dotenv import load_dotenv
from fredapi import Fred

load_dotenv()
logger = logging.getLogger(__name__)

TENORS = ["GS1m", "GS3m", "GS6m", "GS1", "GS2", "GS3", "GS5", "GS10", "GS30"]
DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
US_YIELD_CSV = DATA_DIR / "_fed_yc.csv"
UK_YIELD_CSV = DATA_DIR / "_boe_yc.csv"
BOE_MONTHLY_NOMINAL_CURVE_URL = (
	"https://www.bankofengland.co.uk/-/media/boe/files/statistics/"
	"yield-curves/glcnominalmonthedata.zip"
)


def fred_yields(start_date: str = "1990-01-01") -> dict[str, pd.DataFrame]:
	"""Fetch the available Treasury yield tenors from FRED as separate DataFrames.

	Returns a mapping from FRED series ID (for example, ``"GS10"``) to a
	DataFrame with a ``DATE`` index and a single column named for that series.
	GS7 and GS20 are intentionally omitted.
	"""
	load_dotenv()
	api_key = os.getenv("FRED_API_KEY")
	if not api_key:
		raise ValueError("FRED_API_KEY is missing; add it to your .env file.")

	fred = Fred(api_key=api_key)
	return {
		series_id: fred
		.get_series(series_id, observation_start=start_date)
		.rename(series_id)
		.to_frame()
		for series_id in TENORS
	}


def retrieve_us_yield_data() -> pd.DataFrame:
	_start = "2000-01-01"
	_tickers = [
		"GS30",
		"GS10",
		"GS5",
		"GS3",
		"GS2",
		"GS1",
		"GS6m",
		"GS3m",
		"GS1m",
	]
	df = pdr.get_data_fred(_tickers, _start)
	df.columns = [
		"30-year",
		"10-year",
		"5-year",
		"3-year",
		"2-year",
		"1-year",
		"6-month",
		"3-month",
		"1-month",
	]
	df.index = df.index + pd.offsets.MonthEnd(0)
	DATA_DIR.mkdir(parents=True, exist_ok=True)
	df.to_csv(
		US_YIELD_CSV,
		header=True,
		index=True,
		index_label="DATE",
		date_format="%Y-%m-%d",
		na_rep="NaN",
	)
	return df


def get_us_yield_data() -> pd.DataFrame:
	if not US_YIELD_CSV.exists() or US_YIELD_CSV.stat().st_size == 0:
		return retrieve_us_yield_data()
	df = pd.read_csv(US_YIELD_CSV, index_col=0)
	df.index = pd.to_datetime(df.index)

	# FRED's Treasury curve series are monthly. Refresh a cache that has not
	# received a new observation for 45 days, while keeping cached data usable
	# when FRED is temporarily unreachable.
	if pd.Timestamp.now().normalize() - df.index.max() > pd.Timedelta(days=45):
		try:
			return retrieve_us_yield_data()
		except Exception:
			logger.exception(
				"Could not refresh U.S. yield data from FRED; using cached CSV."
			)
	return df


def retrieve_uk_yield_curve_data() -> pd.DataFrame:
	"""Fetch the BoE monthly nominal government curve and save it as a CSV."""
	df = pd.read_csv(
		BOE_MONTHLY_NOMINAL_CURVE_URL,
		compression="zip",
		index_col=0,
		parse_dates=True,
	)
	df.index.name = "DATE"
	DATA_DIR.mkdir(parents=True, exist_ok=True)
	df.to_csv(
		UK_YIELD_CSV,
		header=True,
		index=True,
		index_label="DATE",
		date_format="%Y-%m-%d",
		na_rep="NaN",
	)
	return df


def get_uk_yield_curve_data() -> pd.DataFrame:
	if not UK_YIELD_CSV.exists() or UK_YIELD_CSV.stat().st_size == 0:
		retrieve_uk_yield_curve_data()
	df = pd.read_csv(UK_YIELD_CSV, index_col=0)
	df.index = pd.to_datetime(df.index)
	df.index.name = "DATE"
	return df
