Search with filters
====================

You can use filters to search funds and stocks more precisely with methods `search_funds` and `search_stock`.

Choose filters
----------------

You can find the possible filters with the methods `search_filter`

for funds:

.. code-block:: python

    from mstarpy import search_filter

    filter_fund = search_filter(pattern = '', asset_type ='fund')

    print(filter_fund)

.. code-block:: python

    ['AdministratorCompanyId', 'AnalystRatingScale', 'BondStyleBox', 'BrandingCompanyId', 'CategoryId', 'CollectedSRRI', 'distribution', 'EquityStyleBox', 'ExpertiseInformed', 'FeeLevel', 'FundTNAV', 'GBRReturnM0', 'GBRReturnM12', 'GBRReturnM120', 'GBRReturnM36', 'GBRReturnM60', 'GlobalAssetClassId', 'GlobalCategoryId', 'IMASectorID', 'IndexFund', 'InvestorTypeProfessional', 'LargestRegion', 'LargestSector', 'OngoingCharge', 'QuantitativeRating', 'ReturnProfilePreservation', 'ShareClassTypeId', 'SustainabilityRank', 'UmbrellaCompanyId', 'Yield_M12']

for stocks:

.. code-block:: python

    from mstarpy import search_filter

    filter_stock = search_filter(pattern = '', asset_type ='stock')

    print(filter_stock)

.. code-block:: python

    ['debtEquityRatio', 'DividendYield', 'epsGrowth3YYear1', 'EquityStyleBox', 'GBRReturnM0', 'GBRReturnM12', 'GBRReturnM36', 'GBRReturnM60', 'GBRReturnM120', 'IndustryId', 'MarketCap', 'netMargin', 'PBRatio', 'PEGRatio', 'PERatio', 'PSRatio', 'revenueGrowth3Y', 'roattm', 'roettm', 'SectorId']


Find filters values
--------------------

Once, you know what filters you want you use the method `filter_universe` to show the possible values of each filter.

.. code-block:: python

    from mstarpy import filter_universe

    filter_value = filter_universe(["GBRReturnM12", "PERatio", "LargestSector"])

    print(filter_value)


You have two types of filters values, either qualitative or quantitative. By example, the filter LargestSector has qualitative values such as SB_Healthcare or SB_Utilities. The filter PERatio works with quantitative values between 0 and 100000.


Filter funds
------------------

Let say we want to find funds that invest mainly in the consumer defensive sector. We can use filters like in this example:

.. code-block:: python

    from mstarpy import search_funds

    response = search_funds(term='',field=["Name", "fundShareClassId", "GBRReturnM12"], country='fr', filters = {"LargestSector" : "SB_ConsumerDefensive"})
    
    df = pd.DataFrame(response)

    print(df.head())

.. code-block:: python

                                       Name fundShareClassId  GBRReturnM12
    0             AB US High Yield A2 EUR H       F00000O4X9         -9.71
    1               AB US High Yield A2 USD       F00000O4XA         -6.88
    2             AB US High Yield I2 EUR H       F00000O4X6         -9.18
    3               AB US High Yield I2 USD       F00000O4XB         -6.36
    4  abrdn China A Share Sus Eq A Acc EUR       F000015MAW         -8.41

If we want to search for funds which invest mainly in consumer defensive or healthcare sectors, we can add filters values to a list.

.. code-block:: python

    from mstarpy import search_funds

    response = search_funds(term='',field=["Name", "fundShareClassId", "GBRReturnM12"], country='fr', filters = {"LargestSector" : ["SB_ConsumerDefensive", "SB_Healthcare"]})
    
    df = pd.DataFrame(response)

    print(df.head())

.. code-block:: python

                                    Name fundShareClassId  GBRReturnM12
    0  AB Concentrated Global Eq A EUR H       F00000SJ2P        -10.46
    1  AB Concentrated Global Eq I EUR H       F00000SJ2J         -9.77
    2    AB Concentrated Global Eq I USD       F00000SE91         -5.77
    3    AB Concentrated Global Eq S USD       F00000SE93          1.16
    4   AB Concentrated Global Eq S1 EUR       F00001CYZS         -1.89


In the previous examples, we saw how to search for securities with a qualitative filter, now let see how to use quantitativer filters.


Filter stocks
------------------

We want to find stocks with a 12 months return superior to 20%. The value of filter is a 2 length tuple. the first element is the sign superior ">", the second element the 12 months return of 20.

.. code-block:: python

    from mstarpy import search_stock

    response = search_stock(term='',field=["Name", "fundShareClassId", "GBRReturnM12", "PERatio"], exchange='PARIS', filters={"GBRReturnM12" : (">", 20)})

    df = pd.DataFrame(response)

    print(df.head())

.. code-block:: python

    0    1000Mercis SA       0P0000DKX2         24.89    95.24
    1          Abeo SA       0P00018PIU         21.73    14.84
    2  ABL Diagnostics       0P00009WGF        279.01      NaN
    3           Acteos       0P00009W9O         27.01      NaN
    4      Actia group       0P00009W9P         44.36      NaN

It will work similar if we are looking for stocks with a PERatio inferior to 10. The value of filter is a 2 length tuple. the first element is the sign inferior "<", the second element is the PERatio 10.

.. code-block:: python

    from mstarpy import search_stock

    response = search_stock(term='',field=["Name", "fundShareClassId", "GBRReturnM12", "PERatio"], exchange='PARIS', filters={"PERatio" : ("<", 10)})

    df = pd.DataFrame(response)

    print(df.head())

.. code-block:: python

                        Name fundShareClassId  GBRReturnM12  PERatio
    0  Acanthe Developpement SA       0P00009W9K        -23.27     5.78
    1                    ALD SA       0P0001AM22         31.89     5.07
    2               Altarea SCA       0P00009WAG         -2.20     8.18
    3  Altur Investissement SCA       0P0000DKYA         33.38     1.98
    4                    Archos       0P00009WAT        -97.02     0.00


We can also look like stocks with a PERatio between 10 and 20. The value of filter is a 2 length tuple. the first element is the lower bound PERatio of 10, the second element is the upper bound PERatio of 20.

.. code-block:: python

    from mstarpy import search_stock

    response = search_stock(term='',field=["Name", "fundShareClassId", "GBRReturnM12", "PERatio"], exchange='PARIS', filters={"PERatio" : (10, 20)})

    df = pd.DataFrame(response)

    print(df.head())

.. code-block:: python

                Name fundShareClassId  GBRReturnM12  PERatio
    0  ABC arbitrage SA       0P00009W9I         -5.73    14.10
    1           Abeo SA       0P00018PIU         21.73    14.84
    2           AdUX SA       0P00009WIO        -32.05    11.49
    3       Altareit SA       0P00009WHA        -11.03    12.69
    4             Alten       0P00009WAH         14.25    19.96


Now we know how to use filters, we can combine them to find a precise securities universe. The world is your oyster.

.. code-block:: python

    from mstarpy import search_stock

    response = search_stock(term='',field=["Name", "fundShareClassId", "GBRReturnM12", "PERatio"], 
                            exchange='PARIS', filters={"PERatio" : ("<", '10'), "GBRReturnM12" : (">", 20), 
                                                        "debtEquityRatio" : (0, 5), "SectorId" : ["IG000BA008", "IG000BA006"] })

    df = pd.DataFrame(response)

    print(df.head())


.. code-block:: python

                            Name fundShareClassId  GBRReturnM12  PERatio
    0                 ALD SA       0P0001AM22         31.89     5.07
    1                Coheris       0P00009WDN         72.68     5.27
    2  Ediliziacrobatica SpA       0P0001GZM9         24.07     6.85
    3               Rexel SA       0P00009WO9         32.27     7.96
    4            Soditech SA       0P00009WQ2         97.45     4.49

