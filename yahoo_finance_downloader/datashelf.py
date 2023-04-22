"""Module to store static data"""

import urllib3

from typing import Dict, List


class DataShelf:
    """Class to store the static data"""

    @staticmethod
    def return_intervals() -> List[str]:
        """
        Return the list of allowable intervals that a user can select:
        1d = daily,
        1wk = weekly, or
        1mo = monthly
        """
        return [
            '1d',
            '1wk',
            '1mo'
        ]

    @staticmethod
    def return_events() -> List[str]:
        """
        Return the list of allowable events that a user can select
        history = historical prices,
        div = dividend,
        split = split, or
        capitalGain = capital gain
        """
        return [
            'history',
            'div',
            'split',
            'capitalGain'
        ]

    @staticmethod
    def return_base_url() -> str:
        """Return the base url to be used for the request"""
        return 'https://query1.finance.yahoo.com/v7/finance/download/'

    @staticmethod
    def validate_request(response: urllib3.response.HTTPResponse) -> bool:
        """
        Validates the request and returns True if it was successful
        :param urllib3.response.HTTPResponse response: urllib3 response needed to infer the status code of the request
        :return: True if it is a valid request, False otherwise
        """
        if str(response.status).startswith('2'):
            return True
        return False

    @staticmethod
    def return_parameter_mapping(dict_key: str) -> Dict[str, str] or None:
        """
        Return the API parameter to be used for the request based on the human parameter passed
        :param str dict_key: human parameter to be translated
        :return: a valid API parameter to be used for the request
        """
        return {
            '_start_date': 'period1',
            '_end_date': 'period2',
            '_interval': 'interval',
            '_events': 'events',
            '_adj_close': 'includeAdjustedHistory'
        }.get(dict_key)
