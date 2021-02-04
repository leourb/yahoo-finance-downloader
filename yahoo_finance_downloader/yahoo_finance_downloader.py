"""Module to download data from Yahoo! Finance"""

import dateparser
import requests

from datetime import datetime
from io import BytesIO

import pandas as pd

from .datashelf import DataShelf


class YahooFinanceDownloader:
    """Download data from Yahoo! Finance from the start_date to the end_date"""

    def __init__(self, ticker, start_date, end_date=None, interval="d", event="h", adj_close=True):
        """
        Initialize the class with the given input
        :param str ticker: single ticker or list of tickers to use to download the data from Yahoo! Finance
        :param str start_date: start date of the query period in a string format YYYY-MM-DD (or similar)
        :param str interval: frequency for the time-series. Default: daily
        :param str event: series to download. Default: history
        :param bool adj_close: True if you want the adjusted series, False otherwise
        :param str end_date: end date of the query period in a string format YYYY-MM-DD (or similar)
        """
        self.__datashelf = DataShelf()
        self.__ticker = ticker
        self.__start_date = start_date
        self.__end_date = end_date
        self.__interval = interval
        self.__event = event
        self.__adj_close = adj_close
        self.__validate_inputs()
        self.__url = self.__build_url()
        self.__raw_query_results = self.__download_file()
        self.__parsed_results = self.__parse_results()

    def __validate_inputs(self):
        """
        Validates start_date and end_date and checks their congruence
        :return: all formatted inputs
        :rtype: None
        """
        self.__validate_start_and_end_date()
        self.__validate_interval()
        self.__validate_series()

    def __validate_start_and_end_date(self):
        """
        Validate start_date and end_date parameters
        :return: validated time input
        :rtype: None
        """
        self.__start_date = dateparser.parse(self.__start_date).timestamp()
        self.__end_date = dateparser.parse(self.__end_date).timestamp() if self.__end_date \
            else datetime.today().timestamp()

    def __validate_interval(self):
        """
        Validate the interval parameter
        :return: validated interval input
        :rtype: None
        """
        interval = self.__interval.lower()
        if interval not in ["daily", "weekly", "monthly"]:
            if interval[0] not in ["d", "w", "m"]:
                interval = "d"
        self.__interval = interval if len(interval) == 1 else interval[0]

    def __validate_series(self):
        """
        Validate the event to be downloaded
        :return: validated event input
        :rtype: None
        """
        event = self.__event.lower()
        if event not in ["historical", "dividend", "split"]:
            if event[0] not in ["h", "d", "s"]:
                event = "h"
        self.__event = event if len(event) == 1 else event[0]

    def __build_url(self):
        """
        Build the url given the parameters set
        :return: a url used to download the data
        :rtype: str
        """
        root = self.__datashelf.get_url_data().get("root").format(self.__ticker)
        period1 = self.__datashelf.get_url_data().get("period1").format(int(self.__start_date))
        period2 = self.__datashelf.get_url_data().get("period2").format(int(self.__end_date))
        interval = self.__datashelf.get_url_data().get("interval").format(
            self.__datashelf.get_interval_data().get(self.__interval)
        )
        events = self.__datashelf.get_url_data().get("events").format(
            self.__datashelf.get_events_data().get(self.__event)
        )
        adj_close = self.__datashelf.get_url_data().get("adj_close").format(str(self.__adj_close).lower())
        url = root + "&".join([period1, period2, interval, events, adj_close])
        print(url)
        return url

    def __download_file(self):
        """
        Download the file give a set of inputs
        :return: the downloaded content of the file
        :rtype: requests.models.Response
        """
        return requests.get(self.__url)

    def get_raw_results(self):
        """
        Get the downloaded raw results"
        :return: a string text with the results
        :rtype: str
        """
        return self.__raw_query_results.text

    def __parse_results(self):
        """
        Parse results in a Pandas DF
        :return: a DataFrame with the parsed results
        :rtype: pd.DataFrame
        """
        return pd.read_csv(BytesIO(self.__download_file().content))

    def get_parsed_results(self):
        """
        Get the parsed results in a DataFrame
        :return: raw results parsed in a DataFrame
        :rtype: pd.DataFrame
        """
        return self.__parsed_results

    def get_url(self):
        """
        Get the generated url to the CSV file
        :return: the url to the data
        :rtype: str
        """
        return self.__url
