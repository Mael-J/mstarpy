
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-a59fd3?logo=buymeacoffee)](https://buymeacoffee.com/maeljourdain)
[![PYPI Downloads](https://static.pepy.tech/badge/mstarpy/month)](https://pepy.tech/project/mstarpy)

# Introduction

MStarpy is an open-source Python package designed to extract and access financial data from [morningstar.com](https://www.morningstar.com/).

It provides free access to public data on stocks and funds, empowering both retail and professional investors with the same high-quality information. Whether you're conducting research, building investment models, or creating dashboards, MStarpy makes it easy to integrate Morningstar data into your workflow.

Our mission is to democratize access to financial insights and support investors in making informed decisions.

The project is open to contributions — join us on [GitHub](https://github.com/Mael-J/mstarpy) and help improve the future of financial transparency.


# Getting Started

## Installation

You can install it **via pip** on the terminal by typing:

``` bash
pip install mstarpy
```

You can also install it **via git** on the terminal by using :

``` bash
pip install git+https://github.com/Mael-J/mstarpy.git@master
```

Import the package MStarpy as follow 

```python 

import mstarpy as ms

```

## Fund analysis

Initialize Funds to start your analysis

```python

funds = ms.Funds("VTSAX")

```

### Historical nav

Get historical nav and total return of the fund

```python
import datetime
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=10)
funds.nav(start_date,end_date)
```

```text
[{'nav': 150.01, 'totalReturn': 232.36911, 'date': '2025-07-03'},
 {'nav': 148.8, 'totalReturn': 230.49479, 'date': '2025-07-07'},
 {'nav': 148.74, 'totalReturn': 230.40185, 'date': '2025-07-08'},
 {'nav': 149.69, 'totalReturn': 231.87342, 'date': '2025-07-09'},
 {'nav': 150.1, 'totalReturn': 232.50852, 'date': '2025-07-10'},
 {'nav': 149.48, 'totalReturn': 231.54813, 'date': '2025-07-11'},
 {'nav': 149.82, 'totalReturn': 232.0748, 'date': '2025-07-14'}]

```

### Holdings of the fund

```python

funds.holdings()

```

```python

ticker	securityName	weighting	marketValue
0	MSFT	Microsoft Corp	6.02457	1.099423e+11
1	NVDA	NVIDIA Corp	5.51387	1.006226e+11
2	AAPL	Apple Inc	5.31119	9.692390e+10
3	AMZN	Amazon.com Inc	3.44210	6.281481e+10
4	META	Meta Platforms Inc Class A	2.49597	4.554891e+10

```

### More on funds

You can access many other methods to retrieve detailed information about the fund.

Examples are available in this notebook:

[MStarpy - Funds example](https://github.com/Mael-J/mstarpy/blob/pre-release/examples/MStarpy%20-%20Funds%20example.ipynb)

## Stock Analysis

Initialize Stock to start your analysis

```python

stock = ms.Stock("FR0000121014")

```

### Historical price

Get historical price of the stock

```python

import datetime
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=10)
stock.historical(start_date, end_date)

```

```text
[{'open': 483.75,
  'high': 483.75,
  'low': 475.0,
  'close': 477.7,
  'volume': 1102,
  'previousClose': 486.0,
  'date': '2025-07-04'},
 {'open': 480.0,
  'high': 480.0,
  'low': 472.2,
  'close': 475.95,
  'volume': 1322,
  'previousClose': 477.7,
  'date': '2025-07-07'}]

```

### Income Statement

```python

stock.incomeStatement()

```

```text

{'_meta': {'companyId': '0C00000VOS',
  'statementType': 'income-statement',
  'periodReport': 'Success',
  'latestReport': 'Success'},
 'columnDefs': ['2015',
  '2016',
  '2017',
  '2018',
  '2019',
  '2020',
  '2021',
  '2022',
  '2023',
  '2024',
  'TTM'],
 'filingIdList': [None,
  None,
  None,
  None,
  None,
  '328683655',
  '384266622',
  '437916148',
  '502488388',
  '577784039',
...
 'footer': {'currency': 'EUR',
  'currencySymbol': '€',
  'orderOfMagnitude': 'Million',
  'fiscalYearEndDate': '12-31'},
 'userType': 'Free'}

```

### More on stocks

You can access many other methods to retrieve detailed information about the stock.

Examples are available in this notebook:

[MStarpy - Stock example](https://github.com/Mael-J/mstarpy/blob/pre-release/examples/MStarpy%20-%20Stock%20example.ipynb)


## Look for securities

You can search for securities using the `screener_universe` method, which leverages the logic behind Morningstar's screener : <a href="https://global.morningstar.com/en-gb/tools/screener/">MorningStar screener</a>

```python

ms.screener_universe("a",
                     language = "fr",
                     field=["name", "isin", "priceToEarnings", "sector"], 
                     filters={"priceToEarnings[trailing]": ("<", 10),
                              "investmentType" : "EQ",
                              "sector": "Technology",
                              "domicile": "FRA"}
                     )
```

```text
[{'meta': {'securityID': '0P00009WB0',
   'performanceID': '0P00009WB0',
   'companyID': '0C00000VXC',
   'universe': 'EQ',
   'exchange': 'XPAR',
   'ticker': 'ATO'},
  'fields': {'name': {'value': 'Atos SE'},
   'isin': {'value': 'FR001400X2S4'},
   'priceToEarnings': {'value': 0.088323},
   'sector': {'value': 'Technology'}}},
 {'meta': {'securityID': '0P0000CKNR',
   'performanceID': '0P0000CKNR',
   'companyID': '0C00000VXC',
   'universe': 'EQ',
   'exchange': 'PINX',
   'ticker': 'AEXAF'},
  'fields': {'name': {'value': 'Atos SE'},
   'isin': {'value': 'FR001400X2S4'},
   'priceToEarnings': {'value': 0.096288},
   'sector': {'value': 'Technology'}}},
 {'meta': {'securityID': '0P0000C3TX',
   'performanceID': '0P0000C3TX',
   'companyID': '0C00000VXC',
   'universe': 'EQ',
   'exchange': 'XMUN',
...
   'ticker': 'AXI1'},
  'fields': {'name': {'value': 'Atos SE'},
   'isin': {'value': 'FR001400X2S4'},
   'priceToEarnings': {'value': 0.087758},
   'sector': {'value': 'Technology'}}}]

```

# Contribution

The project is **open-source** and you can contribute on
[Github](https://github.com/Mael-J/mstarpy).

If you would like to support my work, you can [Buy me a Coffee](https://buymeacoffee.com/maeljourdain).

# Disclaimer

MStarpy is not affiliated to
[morningstar.com](https://www.morningstar.com/) or any other companies.

The package aims to share public information about funds and stocks to
automatize analysis. It is the result of a free and independent
work.

MStarpy does not give any investment recommendations.
