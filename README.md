<h2 align="center">Mutual funds data extraction from MorningStar with Python</h2>

mstarpy is a Python package to get mutual funds data from MorningStar.

##  Installation

To get this package working you will need to install it via pip (with a Python 3.10 version or higher) on the terminal by typing:

``$ pip install mstarpy``

##  Usage

### Load funds

Load a funds with the class Funds

```python
funds = Funds("disruptive technology", country="fr")

print(funds.name)
```

```{r, engine='python', count_lines}       
BNP Paribas Funds Disruptive Technology B USD Capitalisation
```

### Access Raw Data

You will be able to access all methods and get raw data about this funds

```python
print(funds.holdings('equity'))
```

```{r, engine='python', count_lines}       
                                     securityName       secId performanceId holdingTypeId  ...  qualRating  quantRating  bestRatingType  securityType
0                                       Apple Inc  0P000000GY    0P000000GY             E  ...           3            3            Qual       
     ST
1                                  Microsoft Corp  0P000003MH    0P000003MH             E  ...           5            4            Qual       
     ST
2                                 First Solar Inc  0P00006TF8    0P00006TF8             E  ...           3            4            Qual       
     ST
3                            Alphabet Inc Class A  0P000002HD    0P000002HD             E  ...           5            5            Qual       
     ST
4                                Visa Inc Class A  0P0000CPCP    0P0000CPCP             E  ...           4            4            Qual       
     ST
5                      Advanced Micro Devices Inc  0P0000006A    0P0000006A             E  ...           5            5            Qual       
     ST
6   Taiwan Semiconductor Manufacturing Co Ltd ADR  0P000005AR    0P000005AR             E  ...           5            4            Qual       
     ST
7                                    Entegris Inc  0P000001Z2    0P000001Z2             E  ...           3            4            Quan       
     ST
8                        Pure Storage Inc Class A  0P00016Q76    0P00016Q76             E  ...        None            4            Quan       
     ST
9                          Palo Alto Networks Inc  0P0000WI3J    0P0000WI3J             E  ...           3            4            Qual       
     ST
10                           Booking Holdings Inc  0P000004G2    0P000004G2             E  ...           5            4            Qual       
      
```

### Search funds

Look for a specific funds before loading a funds with class Funds

```python
from mstarpy import search_funds

print(search_funds('equity',['SecId','TenforeId','LegalName'], country="fr", pageSize=10,currency="EUR",filters={"GBRReturnM12":(0,5)}))
```

```{r, engine='python', count_lines}       
[{'SecId': 'F00000NRKO', 'TenforeId': '52.8.LU0733933617', 'LegalName': 'AB - Asia Ex-Japan Equity Portfolio AY JPY Acc'}, {'SecId': 'F00000NRKP', 'TenforeId': '52.8.LU0733933963', 'LegalName': 'AB - Asia Ex-Japan Equity Portfolio BY JPY Inc'}, {'SecId': 'F00000SE93', 'LegalName': 'AB - Concentrated Global Equity Portfolio S USD Acc'}, {'SecId': 'F0000139L0', 'TenforeId': '52.8.LU1934455194', 
'LegalName': 'AB - Low Volatility Total Return Equity Portfolio A USD'}, {'SecId': 'F0000139L2', 'TenforeId': '52.8.LU1934455350', 'LegalName': 'AB - Low Volatility Total Return Equity Portfolio I USD'}, {'SecId': 'F00001D6YY', 'TenforeId': '52.8.LU2399902076', 'LegalName': 'AB SICAV I - Global Low Carbon Equity Portfolio I EUR Acc'}, {'SecId': 'F000013YTV', 'TenforeId': '52.8.LU1998907270', 'LegalName': 'AB SICAV I - Low Volatility Equity Portfolio I EUR Acc'}, {'SecId': 'F0GBR052U8', 'TenforeId': '52.8.LU0128316840', 'LegalName': 'AB SICAVI - European Equity Portfolio I Acc'}, {'SecId': 'F0GBR04SJU', 'TenforeId': '52.8.LU0231455378', 'LegalName': 'Aberdeen Standard SICAV I - Asia Pacific Sustainable Equity Fund A Acc GBP'}, {'SecId': 'FOGBR05LNS', 'TenforeId': '52.8.LU0231460451', 'LegalName': 'Aberdeen Standard SICAV I - Europe ex UK Sustainable Equity FundA Acc GBP'}]
```

### Look for field

You can retrieve the list of field 

```python
from mstarpy import search_field

print(search_field("name"))

```

```{r, engine='python', count_lines}       
['CategoryName', 'instrumentName', 'LegalName', 'Name']
```

## Contribute

You can download the open-source project on GitHub [mstarpy](https://github.com/Mael-J/mstarpy) and add your touch to make the package better.

## Disclaimer

mstarpy works as an API of MorningStar. It allows to get data from the site in an easy way. mstarpy is not affiliated with MorningStar and is completly independant.


