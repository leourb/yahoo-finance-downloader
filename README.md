# Yahoo! Finance Downloader

## Abstract

The package takes data from [Yahoo! Finance](https://finance.yahoo.com) and returns it in a handy `pd.DataFrame`, in raw
bytes or the source url used to download it.
The user has flexibility in choosing the parameters he/she likes or use the default ones.

### Parameters

The following list is a list of parameters with the following enumerators listed by parameters:

- **ticker**: ticker of the instrument to retrieve data from. It must be a valid Yahoo! Finance ticker;
- **start_date**: this accepts strings in the format _YYYY-MM-DD_, and it is <u>mandatory</u>;
- **end_date**: this accepts strings in  the format _YYYY-MM-DD_, and it **not** mandatory. If left it blank, it will use today's date;
- **interval**: the interval of thr query. The acceptable values are _daily_, _weekly_ and _monthly_. The script
validates the string, or the character passed as input. Values such _daily_, _DAILY_, _d_, _D_, _days_, ... are all accepted;
- **event**: there are three different events for which you can return data from:

  1. Price History (in this context simply "history")
  2. Split
  3. Dividend

  The logic according to which the script works is the same as the last parameter: **case-insensitive** and similar words;
- **adj_close**: default parameter is `True`. However, you can pass the boolean `False` if you do not like to get
Adjusted Prices.
  
### Sample Usage

```python
from yahoo_finance_downloader import YahooFinanceDownloader

data = YahooFinanceDownloader(ticker="AAPL", start_date="2020-01-01", interval="DAYS", event="H")
print(data.get_parsed_results())
```

This query will return the historical daily prices for Apple Inc. from the 1st January 2020 till today in a 
`pd.DataFrame` format.

## Comments or Feedback

Please do not hesitate to contact me for suggestions or feedback! I'll be happy to hear from you.
