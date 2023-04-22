"""Module to download data from Yahoo! Finance"""

import os
import re
import urllib3

from datetime import date, datetime
from io import BytesIO
from typing import Any, Dict

import pandas as pd

from .datashelf import DataShelf


class YahooFinanceInputs(DataShelf):
    """Collect the inputs the user types to download the data from Yahoo Finance"""

    def __init__(
            self,
            ticker: str,
            start_date: str,
            end_date: str = None,
            interval: str = '1d',
            events: str = 'history',
            adj_close: bool = True
    ) -> None:
        """
        Initialize the class with the given input
        :param str ticker: single ticker to use to download the data from Yahoo! Finance
        :param str start_date: start date of the query period in a string format YYYY-MM-DD
        :param str end_date: end date of the query period in a string format YYYY-MM-DD
        :param str interval: frequency for the time-series. Default: daily
        :param str events: series to download. Default: history
        :param bool adj_close: True if you want the adjusted series, False otherwise
        :return: an instance of the class
        """
        super().__init__()
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date if end_date else date.today().strftime('%Y-%m-%d')
        self.interval = interval
        self.events = events
        self.adj_close = adj_close

    @property
    def ticker(self) -> str:
        """Return a private copy of the ticker property"""
        return self._ticker

    @ticker.setter
    def ticker(self, ticker_value: str) -> None or TypeError or ValueError:
        """
        Set the value to ticker
        :param str ticker_value: ticker string to be assigned to the variable
        :return: a valid instance variable with ticker_value as the value
        """
        if type(ticker_value) != str:
            raise TypeError(f'Ticker needs to be string! {str(ticker_value)} is {type(ticker_value)}')
        if not ticker_value:
            raise ValueError('Ticker cannot be blank')
        self._ticker = ticker_value

    @property
    def start_date(self) -> int:
        """Return a private copy of the start_date property"""
        return self._start_date

    @start_date.setter
    def start_date(self, start_date_value: str) -> None or TypeError or ValueError:
        """
        Set the value to start_date_value
        :param str start_date_value: string containing the desired start_date
        :return: a valid instance variable with start_date_value as the value
        """
        if type(start_date_value) != str:
            raise TypeError(f'start_date needs to be string. You have passed {type(start_date_value)}')
        if not start_date_value:
            raise ValueError('start_date needs to be populated')
        try:
            datetime.strptime(start_date_value, '%Y-%m-%d')
        except ValueError:
            print('start_date needs to be of YYYY-MM-DD format.')
        if datetime.strptime(start_date_value, '%Y-%m-%d').date() >= date.today():
            raise ValueError(f'start_date {start_date_value} cannot be greater or equal than today\'s date')
        self._start_date = int(datetime.strptime(start_date_value, '%Y-%m-%d').timestamp())

    @property
    def end_date(self) -> int:
        """Return a private copy of the end_date property"""
        return self._end_date

    @end_date.setter
    def end_date(self, end_date_value: str) -> None or TypeError or ValueError:
        """
        Set the value to end_date_value
        :param str end_date_value: string containing the desired end_date
        :return: a valid instance variable with end_date_value as the value
        """
        if type(end_date_value) != str:
            raise TypeError(f'end_date needs to be string. You have passed {type(end_date_value)}')
        if not end_date_value:
            raise ValueError('end_date needs to be populated')
        try:
            datetime.strptime(end_date_value, '%Y-%m-%d')
        except ValueError:
            print('end_date needs to be of YYYY-MM-DD format.')
        if (
                datetime.strptime(end_date_value, '%Y-%m-%d').date()
                <= datetime.fromtimestamp(self.start_date).date()
        ):
            raise ValueError(f'end_date {end_date_value} needs to be earlier than {self.start_date}')
        self._end_date = int(datetime.strptime(end_date_value, '%Y-%m-%d').timestamp())

    @property
    def interval(self) -> str:
        """Return a private copy of the interval property"""
        return self._interval

    @interval.setter
    def interval(self, interval_value: str) -> None or TypeError or ValueError:
        """
        Set the value to interval
        :param str interval_value: cadence of the data the user wants to return
        :return: a valid instance variable with interval_value as the value
        """
        if type(interval_value) != str or None:
            raise TypeError(
                f'interval_value needs to be string or None as it is not a mandatory parameter. '
                f'You have passed {type(interval_value)}'
            )
        if interval_value.lower() not in self.return_intervals():
            raise ValueError(
                f'interval needs to be one of these values {", ".join(self.return_intervals())}'
            )
        self._interval = interval_value

    @property
    def events(self) -> str:
        """Return a private copy of the events property"""
        return self._events

    @events.setter
    def events(self, event_value: str) -> None or TypeError or ValueError:
        """
        Set the value to events
        :param str event_value: value of the series or the corporate events to pull
        :return: a valid instance variable with event_value as the value
        """
        if type(event_value) != str or None:
            raise TypeError(
                f'event_value needs to be string or None as it is not a mandatory parameter. '
                f'You have passed {type(event_value)}'
            )
        if event_value.lower() not in self.return_events():
            raise ValueError(
                f'event_value needs to be one of these values {", ".join(self.return_events())}'
            )
        self._events = event_value

    @property
    def adj_close(self) -> str:
        """Return a private copy of the events property"""
        return self._adj_close

    @adj_close.setter
    def adj_close(self, adj_close_value: bool) -> None or TypeError or ValueError:
        """
        Set the value to adj_close
        :param bool adj_close_value: if True it will return the series adjusted by split and dividends
        :return: a valid instance variable with adj_close as the value
        """
        if type(adj_close_value) != bool or None:
            raise TypeError(
                f'adj_close_value needs to be boolean or None as it is not a mandatory parameter. '
                f'You have passed {type(adj_close_value)}'
            )
        self._adj_close = str(adj_close_value).lower()


class YahooFinanceDownloader(YahooFinanceInputs):

    def __init__(
            self,
            ticker: str,
            start_date: str,
            end_date: str,
            interval: str = '1d',
            events: str = 'history',
            adj_close: bool = True
    ) -> None:
        """
        Initialize the class with the given input
        :param str ticker: single ticker or list of tickers to use to download the data from Yahoo! Finance
        :param str start_date: start date of the query period in a string format YYYY-MM-DD
        :param str end_date: end date of the query period in a string format YYYY-MM-DD
        :param str interval: frequency for the time-series. Default: daily
        :param str events: series to download. Default: history
        :param bool adj_close: True if you want the adjusted series, False otherwise
        :return: an instance of the class
        """
        super().__init__(ticker, start_date, end_date, interval, events, adj_close)
        self._raw_query_results = self._process_request()

    def _build_url(self) -> str:
        """Build the base url to be used in the get request"""
        return f'{self.return_base_url()}{self.ticker}'

    def _standardize_parameters(self) -> Dict[str, Any]:
        """Standardize the API Key Parameters to be used for the request"""
        return {
            self.return_parameter_mapping(human_param_key): human_param_value
            for human_param_key, human_param_value in self.__dict__.items()
            if self.return_parameter_mapping(human_param_key)
        }

    def _process_request(self) -> BytesIO or ConnectionError:
        """Process the request querying the data from Yahoo! Finance"""
        http = urllib3.PoolManager()
        with http.request(
                'GET',
                self._build_url(),
                preload_content=False,
                fields=self._standardize_parameters()
        ) as response:
            data = response.read()
            file_obj = BytesIO(data)
        if self.validate_request(response):
            return file_obj
        raise ConnectionError(
            f'There was an error querying the data.\n '
            f'Status Code: {str(response.status)}\n '
            f'Message: {file_obj.getvalue().decode()}'
        )

    def to_pandas(self) -> pd.DataFrame:
        """Converts the results into a Pandas DataFrame"""
        return pd.read_csv(self._raw_query_results)

    def to_file(self, path: str = None, filename: str = None) -> None:
        """
        Write the BytesIO object to a local file
        :param str path: optional path where the user wants to save the data
        :param str filename: optional filename to be used to rename save the data
        :return: a local CSV with the data downloaded
        """
        filename_local = filename if filename else f'{self.ticker}_{self.events}'
        path_local = os.path.join(path or '', f'{filename_local}')
        assert re.search(r'^[\w.-]+$', filename_local), \
            f'filename {filename_local} needs to be alphanumeric and without extension'
        assert not re.search(r'[<>:"|.?*]', path_local), \
            f'{path_local} is not a valid path. Please use only valid paths'
        if path and not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path_local}.csv', 'wb') as file:
            bytes_data = self._raw_query_results.getvalue()
            file.write(bytes_data)
        file.close()

    def display_file(self) -> None:
        """Display the data downloaded"""
        print(self._raw_query_results.getvalue().decode('utf-8'))
