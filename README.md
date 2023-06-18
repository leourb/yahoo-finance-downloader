# Yahoo! Finance Downloader

## Abstract

The package takes data from [Yahoo! Finance](https://finance.yahoo.com), and it prints, converts to pandas or save it to
file.

## Build the package

Clone the repo into your desired location and then build the package into your terminal with:

```shell
python setup.py bdist_wheel
```

This will create the `dist` folder into the same location you have your `setup.py`.
To install the wheel, you can just run

## Download the whl

Alternatively, you can use the pre-built whl package under the `dist` folder in the repo and install it as shown below

```shell
cd dist
pip install Yahoo_Finance_Downloader-1.0.0-py3-none-any.whl
```

## Usage

### Parameters

The following list is a list of parameters with the following enumerators listed by parameters:

- **ticker**: ticker of the instrument to retrieve data from. It must be a valid Yahoo! Finance ticker;
- **start_date**: this accepts strings in the format _YYYY-MM-DD_;
- **end_date**: this accepts strings in  the format _YYYY-MM-DD_;
- **interval**: the interval of thr query. The acceptable values are _1d_, _1w_ and _1mo_;
- **event**: there are three different events for which you can return data from:

  1. _history_ for Price History
  2. _div_ for Dividends
  3. _split_ for Stock Splits
  4. _capitalGain_ for Capital Gains

- **adj_close**: default parameter is `True`. However, you can pass the boolean `False` if you do not like to get
Adjusted Prices.
  
### Sample Usage

#### Display the data on screen

```python
from yahoo_finance_downloader import YahooFinanceDownloader

data = YahooFinanceDownloader(ticker='AAPL', start_date='2020-01-01', end_date='2023-04-10', events='div')
data.display_file()
```

This query will return the historical dividends for Apple Inc. from the January 1st 2020 till April 10th 2023, and it 
will display the data on screen.

#### Return the results in a `pandas.DataFrame` object

```python
from yahoo_finance_downloader import YahooFinanceDownloader

data = YahooFinanceDownloader(ticker='AAPL', start_date='2020-01-01', end_date='2023-04-10', events='div')
data.to_pandas()
```

This query will return the historical dividends for Apple Inc. from the January 1st 2020 till April 10th 2023, and it 
will return a `pandas.DataFrame` object. This will come handy as you can join or leverage all the built-in methods that
Pandas offers.

#### Write the results on a file

```python
from yahoo_finance_downloader import YahooFinanceDownloader

data = YahooFinanceDownloader(ticker='AAPL', start_date='2020-01-01', end_date='2023-04-10', events='div')
data.to_file(path='this/is/my/file/path', filename='my-file_test')
```
This query will return the historical dividends for Apple Inc. from the January 1st 2020 till April 10th 2023, and it 
will write the results into `this/is/my/file/path` with filename `my-file_test.csv`. The function will check for you:

1. The `path` is valid
2. The `filename` is valid
3. The `path` exists (and, if not, will create the dir for you)

If no `filename` is passed, then the script will save the file in the default dir as `ticker_event.csv`
