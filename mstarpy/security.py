import datetime
import json
import re
import requests

from .error import not_200_response
from .search import search_funds, search_stock, token_chart
from .utils import APIKEY, SITE, random_user_agent


#with Universe field, we can detect the asset class
#done find all stock echange and create a search_equity method
#add parameter exchange to Security class and search stocks if stock and exchange

class Security:
    """
    Parent class to access data about security

    Args:
        term (str): text to find a fund can be a name, part of a name or the isin of the funds
        country (str) : text for code ISO 3166-1 alpha-2 of country, should be '' for etf
        pageSize (int): number of funds to return
        itemRange (int) : index of funds to return (must be inferior to PageSize)
        proxies = (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}

    Examples:
        >>> Security('0P0000712R', "ca", 9, 0)
        >>> Security('visa', "", 25, 2)

    Raises:
        TypeError: raised whenever the parameter type is not the type expected
        ValueError : raised whenever the parameter is not valid or no fund found

    """

    def __init__(self, term = None, asset_type: str ="", country: str = "", exchange: str = "", pageSize: int =1, itemRange: int = 0, filters: dict={}, proxies: dict ={}):

        if not isinstance(country, str):
            raise TypeError('country parameter should be a string')

        if country and not country.lower() in SITE.keys():
            raise ValueError(f'country parameter can only take one of the values: {", ".join(SITE.keys())}')

        if not isinstance(pageSize, int):
            raise TypeError('pageSize parameter should be an integer')

        if not isinstance(itemRange, int):
            raise TypeError('itemRange parameter should be an integer')

        if pageSize <= itemRange :
            raise ValueError('itemRange parameter should be strictly inferior to pageSize parameter')

        if not isinstance(filters, dict):
            raise TypeError('filters parameter should be dict')
        
        if not isinstance(proxies, dict):
            raise TypeError('proxies parameter should be dict')

        self.proxies = proxies

        if country:
            self.site = SITE[country.lower()]["site"]
        else:
            self.site =""
        

        self.country = country
        
        self.exchange = exchange

        self.asset_type = 'security'

        code_list = []
        
        if exchange:
            code_list = search_stock(term,['fundShareClassId','SecId','TenforeId','LegalName','Universe'],exchange=exchange,pageSize=pageSize,filters =filters, proxies=self.proxies)
        else:
            code_list = search_funds(term,['fundShareClassId','SecId','TenforeId','LegalName','Universe'], country, pageSize,filters =filters, proxies = self.proxies)

        if code_list:
            if itemRange < len(code_list):
                self.code = code_list[itemRange]["fundShareClassId"]
                self.name = code_list[itemRange]["LegalName"]
                if "TenforeId" in code_list[itemRange]:
                    tenforeId = code_list[itemRange]["TenforeId"]
                    regex = re.compile("[0-9]*\.[0-9]\.")
                    self.isin = regex.sub('',tenforeId)                   
                else:
                    self.isin = None
                    
                    
                universe = code_list[itemRange]["Universe"]

                if universe[:2] == 'E0':
                    self.asset_type = 'stock'
                elif universe[:2] == 'ET':
                    self.asset_type = 'etf'
                elif universe[:2] == 'FO':
                    self.asset_type = 'fund'


                if universe[:2] == 'E0' and asset_type in ['etf', 'fund']:
                    raise ValueError(f'The security found with the term {term} is a stock and the parameter asset_type is equal to {asset_type}, the class Stock should be used with this security.')
                
                if universe[:2] in ['FO', 'ET'] and asset_type =='stock':
                    if universe[:2] == 'FO':
                        raise ValueError(f'The security found with the term {term} is a fund and the parameter asset_type is equal to {asset_type}, the class Fund should be used with this security.')
                    else:
                        raise ValueError(f'The security found with the term {term} is an ETF and the parameter asset_type is equal to {asset_type}, the class Fund should be used with this security.')



            else:
                raise ValueError(f'Found only {len(code_list)} {self.asset_type} with the term {term}. The paramater itemRange must maximum equal to {len(code_list)-1}')
        else:
            if country:
                raise ValueError(f'0 {self.asset_type} found with the term {term} and country {country}')
            elif exchange:
                raise ValueError(f'0 {self.asset_type} found with the term {term} and exchange {exchange}')
            else:
                raise ValueError(f'0 {self.asset_type} found with the term {term}')
            


    def GetData(self,field,params={},headers={}, url_suffixe='data'):
        """
        Generic function to use MorningStar global api.

        Args:
            field (str) : endpoint of the request
            params (dict) : parameter for the request
            headers (dict) : headers of the request
            url_suffixe (str) : suffie of the url

        Raises:
            TypeError raised whenever type of paramater are invalid

        Returns:
            dict with data

        Examples:
            >>> Security("rmagx", "us").GetData("price/feeLevel")

        """

        if not isinstance(field, str):
            raise TypeError('field parameter should be a string')

        if not isinstance(params, dict):
            raise TypeError('params parameter should be a dict')
        
        if not isinstance(url_suffixe, str):
            raise TypeError('url_suffixe parameter should be a string')

        #url of API
        url = f"""https://api-global.morningstar.com/sal-service/v1/{self.asset_type}/{field}/{self.code}"""

        if url_suffixe:
            url += f"""/{url_suffixe}"""


        #headers
        default_headers = {
            "apikey" : APIKEY,
        }

        all_headers = default_headers | headers
        

        response = requests.get(url,params=params, headers=all_headers,proxies=self.proxies)


        not_200_response(url,response)

        return json.loads(response.content.decode()) 
    
    def ltData(self,field,currency="EUR"):
        """
        Generic function to use MorningStar lt api.

        Args:
            field (str) : viewId in the params
            currency (str) : currency in 3 letters

        Raises:
            TypeError raised whenever type of paramater are invalid

        Returns:
            dict with data

        Examples:
            >>> Security("rmagx", "us").ltData("price/feeLevel")

        """
        if not isinstance(field, str):
            raise TypeError('field parameter should be a string')
        
        #url of API
        url = f"""https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security_details/{self.code}"""

        params = {
            "viewId": field,
            "currencyId":currency,
            "itype" :"msid",
            "languageId": "en",
            "responseViewFormat":"json",
        }
        response = requests.get(url,params=params,proxies=self.proxies)


        not_200_response(url,response)

        #responseis a list
        response_list = json.loads(response.content.decode()) 
        if response_list:
            return response_list[0]
        else:
            return {}





    def TimeSeries(self,field,start_date,end_date,frequency="daily"):
        """
        This function retrieves historical data of the specified fields
        
        Args:
            start_date (datetime) : start date to get history
            end_date (datetime) : end date to get history
            frequency (str) : can be daily, weekly, monthly 

        Returns:
            list of dict time series
            
        Examples:
            >>> Funds("RMAGX", "us").TimeSeries(["nav","totalReturn"],datetime.datetime.today()- datetime.timedelta(30),datetime.datetime.today())

        Raises:
            TypeError: raised whenever the parameter type is not the type expected
            ValueError : raised whenever the parameter is not valid or no funds found
            
        """

        #error raised if field is not a string or a list
        if not isinstance(field, (str, list)):
            raise TypeError('field parameter should be a string or a list')
        
        #error raised if start_date is note a datetime.date
        if not isinstance(start_date,datetime.date):
            raise TypeError("start_date parameter should be a datetime.date")

        #error raised if end_date is note a datetime.date
        if not isinstance(end_date,datetime.date):
            raise TypeError("end_date parameter should be a datetime.date")

        #error if end_date < start_date
        if end_date < start_date:
            raise ValueError("end_date must be more recent than start_date")
        
        
        #error raised if frequency is not a string
        if not isinstance(frequency, str):
            raise TypeError('frequency parameter should be a string')

        #dict of frequency
        frequency_row = {'daily' : 'd','weekly' : 'w', 'monthly' : 'm'}

        #raise an error if frequency is not daily, wekly or monthly
        if frequency not in frequency_row:
            raise ValueError(f"frequency parameter must take one of the following value : { ', '.join(frequency_row.keys())}")
        
        if isinstance(field, list):
            queryField = ','.join(field)
        else:
            queryField = field
                
        #bearer token
        bearer_token = token_chart()
        #url for nav
        url =f"https://www.us-api.morningstar.com/QS-markets/chartservice/v2/timeseries?query={self.code}:{queryField}&frequency={frequency_row[frequency]}&startDate={start_date.strftime('%Y-%m-%d')}&endDate={end_date.strftime('%Y-%m-%d')}&trackMarketData=3.6.3&instid=DOTCOM"
        #header with bearer token
        headers = {
                    'user-agent' : random_user_agent(), 
                    'authorization': f'Bearer {bearer_token}',
                    }
        #response
        response = requests.get(url, headers=headers, proxies=self.proxies)
        #manage response
        not_200_response(url,response)
        #result
        result =json.loads(response.content.decode())
        #return empty list if we don't get data
        if not result:
            return []
        if "series" in result[0]:
            return result[0]["series"]
        
        return []