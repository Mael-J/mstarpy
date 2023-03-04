Getting Started
===============

Installation
------------

You can install it **via pip** on the terminal by typing:

.. code-block:: bash

   pip install mstarpy

You can also install it **via git** on the terminal bu using :

.. code-block:: bash

   pip install git+https://github.com/Mael-J/mstarpy.git@master


First commands
--------------

Look for funds with `search_funds`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can look for funds by using the method `search_funds`. In the following example, we will look for 40 funds in the US market with the term "technology" in their name. We want to get the name, the ID and the 12 months return. We transform the result in a pandas DataFrame to make it more clear.

.. code-block:: python

    import mstarpy
    import pandas as pd

    response = mstarpy.search_funds(term="technology", field=["Name", "fundShareClassId", "GBRReturnM12"], country="us", pageSize=40, currency ="USD")

    df = pd.DataFrame(response)
    print(df.head())

.. code-block:: python

                                Name fundShareClassId  GBRReturnM12
    0       Baron Technology Instituitional       F00001CUJ3        -21.64
    1                   Baron Technology R6       F00001CUJ1        -21.88
    2               Baron Technology Retail       F00001CUJ2        -21.91
    3         Black Oak Emerging Technology       FOUSA00LIX         -8.33
    4  BlackRock Technology Opportunities K       F000014AX6        -21.09


Look for fields with `search_field`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can find the field you need for the `search_funds` and `search_stock` methods using `search_field`. In the following example, we get all fields.

.. code-block:: python

    from mstarpy import search_field
    
    response = search_field(pattern='')

    print(response)

.. code-block:: python

    ['AdministratorCompanyId', 'AlphaM36', 'AnalystRatingScale', 'AverageCreditQualityCode', 'AverageMarketCapital', 'BetaM36', 'BondStyleBox', 'brandingCompanyId', 'categoryId', 'CategoryName', 'ClosePrice', 'currency', 'DebtEquityRatio', 'distribution', 'DividendYield', 'EBTMarginYear1', 'EffectiveDuration', 'EPSGrowth3YYear1', 'equityStyle', 'EquityStyleBox', 'exchangeCode', 'ExchangeId', 'ExpertiseAdvanced', 'ExpertiseBasic', 'ExpertiseInformed', 'FeeLevel', 'fundShareClassId', 'fundSize', 'fundStyle', 'FundTNAV', 'GBRReturnD1', 'GBRReturnM0', 'GBRReturnM1', 'GBRReturnM12', 'GBRReturnM120', 'GBRReturnM3', 'GBRReturnM36', 'GBRReturnM6', 'GBRReturnM60', 'GBRReturnW1', 'geoRegion', 'globalAssetClassId', 'globalCategoryId', 'iMASectorId', 'IndustryName', 'InitialPurchase', 'instrumentName', 'investment', 'investmentExpertise', 'investmentObjective', 'investmentType', 'investorType', 'InvestorTypeEligibleCounterparty', 'InvestorTypeProfessional', 'InvestorTypeRetail', 'LargestSector', 'LegalName', 'managementStyle', 'ManagerTenure', 'MarketCap', 'MarketCountryName', 'MaxDeferredLoad', 'MaxFrontEndLoad', 'MaximumExitCostAcquired', 'MorningstarRiskM255', 'Name', 'NetMargin', 'ongoingCharge', 'OngoingCostActual', 'PEGRatio', 'PERatio', 'PerformanceFeeActual', 'PriceCurrency', 'QuantitativeRating', 'R2M36', 'ReturnD1', 'ReturnM0', 'ReturnM1', 'ReturnM12', 'ReturnM120', 'ReturnM3', 'ReturnM36', 'ReturnM6', 'ReturnM60', 'ReturnProfileGrowth', 'ReturnProfileHedging', 'ReturnProfileIncome', 'ReturnProfileOther', 'ReturnProfilePreservation', 'ReturnW1', 'RevenueGrowth3Y', 'riskSrri', 'ROATTM', 'ROETTM', 'ROEYear1', 'ROICYear1', 'SecId', 'SectorName', 'shareClassType', 'SharpeM36', 'StandardDeviationM36', 'starRating', 'StarRatingM255', 'SustainabilityRank', 'sustainabilityRating', 'TenforeId', 'Ticker', 'totalReturn', 'totalReturnTimeFrame', 'TrackRecordExtension', 'TransactionFeeActual', 'umbrellaCompanyId', 'Universe', 'Yield_M12', 'yieldPercent']


Analysis of funds
~~~~~~~~~~~~~~~~~

Once, you know what fund you want to analyse, you can load it with the class `Funds` and then access all the methods to get data.

.. code-block:: python

    import mstarpy

    fund = mstarpy.Funds(term="FOUSA00LIX", country="us")


You can access to his property name.

.. code-block:: python

    print(fund.name)

.. code-block:: python

    'Black Oak Emerging Technology Fund'


You can show the equity holdings of the fund.

.. code-block:: python

    df_equity_holdings = fund.holdings(holdingType="equity")
    print(df_equity_holdings[["securityName", "weighting", "susEsgRiskScore"]].head())

.. code-block:: python

                        securityName  weighting  susEsgRiskScore
    0                       Apple Inc    5.03336          16.6849
    1                        KLA Corp    4.90005          16.6870
    2  Kulicke & Soffa Industries Inc    4.23065          17.2155
    3      SolarEdge Technologies Inc    4.13637          24.6126
    4                   Ambarella Inc    4.10950          33.1408


You can find the historical Nav and total return of the fund.

.. code-block:: python

    import datetime
    import pandas as pd
    start_date = datetime.datetime(2023,1,1)
    end_date = datetime.datetime(2023,3,2)
    #get historical data
    history = fund.nav(start_date=start_date,end_date=end_date, frequency="daily")
    #convert it in pandas DataFrame
    df_history = pd.DataFrame(history)

    print(df_history.head())


.. code-block:: python

        nav  totalReturn        date
    0  6.28     10.21504  2022-12-30
    1  6.23     10.13371  2023-01-03
    2  6.31     10.26383  2023-01-04
    3  6.18     10.05238  2023-01-05
    4  6.37     10.36143  2023-01-06


Look for stock with `search_stock`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can look for stocks by using the method `search_stock`. In the following example, we will look for 20 stocks on the Paris Stock Exchange with the term "AB" in their name. We want to get the name, the ID and the Sector. We transform the result in a pandas DataFrame to make it more clear.

.. code-block:: python

    import mstarpy
    import pandas as pd

    response = mstarpy.search_stock(term="AB",field=["Name", "fundShareClassId", "SectorName"], exchange='PARIS',pageSize=20)

    df = pd.DataFrame(response)
    print(df.head())

.. code-block:: python

                                Name fundShareClassId          SectorName
    0                      AB Science       0P0000NQNE          Healthcare
    1                ABC arbitrage SA       0P00009W9I  Financial Services
    2                         Abeo SA       0P00018PIU   Consumer Cyclical
    3  Abionyx Pharma Ordinary Shares       0P00015JGM          Healthcare
    4                       Abivax SA       0P00016673          Healthcare

Tips : You can get different exchange by looking at the variable EXCHANGE in mstarpy.utils

.. code-block:: python
    from mstarpy.utils import EXCHANGE

    print(list(EXCHANGE))

.. code-block:: python

    ['NYSE', 'NASDAQ', 'LSE', 'AMSTERDAM', 'ATHENS', 'BOLSA_DE_VALORES', 'BOMBAY', 'BORSA_ITALIANA', 'BRUSSELS', 'COPENHAGEN', 'HELSINKI', 'ICELAND', 'INDIA', 'IPSX', 'IRELAND', 'ISTANBUL', 'LISBON', 'LUXEMBOURG', 'OSLO_BORS', 'PARIS', 'RIGA', 'SHANGAI', 'SHENZHEN', 'SINGAPORE', 'STOCKHOLM', 'SWISS', 'TAIWAN', 'TALLIN', 'THAILAND', 'TOKYO', 'VILNIUS', 'WARSAW', 'WIENER_BOERSE']


Analysis of stocks
~~~~~~~~~~~~~~~~~

Once, you know what stock you want to analyse, you can load it with the class `Stock` and then access all the methods to get data.

.. code-block:: python

    import mstarpy

    stock = stock = mstarpy.Stock(term="0P00018PIU", exchange="PARIS")

You can access to his property name.

.. code-block:: python

    print(stock.name)

.. code-block:: python

    'Abeo SA'

You can find the historical price and volume of the stock.

.. code-block:: python

    import datetime
    import pandas as pd
    start_date = datetime.datetime(2023,1,1)
    end_date = datetime.datetime(2023,3,2)
    #get historical data
    history = stock.historical(start_date=start_date,end_date=end_date, frequency="daily")
    #convert it in pandas DataFrame
    df_history = pd.DataFrame(history)

    print(df_history.head())


.. code-block:: python

    open   high    low  close  volume  previousClose        date
    0  18.60  18.60  18.55  18.55     194          18.55  2022-12-30
    1  18.70  18.70  18.70  18.70       9          18.55  2023-01-02
    2  18.65  18.70  18.55  18.60     275          18.70  2023-01-03
    3  18.65  18.65  18.50  18.60     994          18.60  2023-01-04
    4  18.65  18.95  18.50  18.60     999          18.60  2023-01-05


You can show the financial statements such as the balance sheet.


.. code-block:: python

     bs = stock.balanceSheet(period='annual', reportType='original')
     

More commands
--------------


You can find all the methods of the classes `Funds` and `Stocks` in the part Indices and tables of this documentation.
