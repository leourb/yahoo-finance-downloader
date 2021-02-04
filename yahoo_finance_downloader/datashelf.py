"""Module to store static data"""

INTERVAL = {
    "d": "1d",
    "w": "1wk",
    "m": "1mo"
}

EVENTS = {
    "h": "history",
    "d": "div",
    "s": "split"
}

URL_DATA = {
    "root": "https://query1.finance.yahoo.com/v7/finance/download/{}?",
    "period1": "period1={}",
    "period2": "period2={}",
    "interval": "interval={}",
    "events": "events={}",
    "adj_close": "includeAdjustedClose={}"
}


class DataShelf:
    """Class to store the static data"""

    def __init__(self):
        """Initialize the class"""
        self.__data = URL_DATA
        self.__interval = INTERVAL
        self.__events = EVENTS

    def get_url_data(self):
        """
        Return the URL_DATA dictionary publicly
        :return: a public instance of URL_DATA
        :rtype: dict
        """
        return self.__data

    def get_interval_data(self):
        """
        Return the INTERVAL dictionary publicly
        :return: a public instance of INTERVAL
        :rtype: dict
        """
        return self.__interval

    def get_events_data(self):
        """
        Return the EVENTS dictionary publicly
        :return: a public instance of EVENTS
        :rtype: dict
        """
        return self.__events
