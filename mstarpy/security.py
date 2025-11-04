import datetime
import re
import requests

from .error import not_200_response

from .search import (screener_universe,
                     token_chart
                     )
from .utils import (
    APIKEY,
    random_user_agent,
    LANGUAGE
    )



class Security:
    """
    Parent class to access data about security

    Args:
        term (str): text to find a fund can be a name, part of a name or the isin of the funds
        asset_type (str) : security type from the inherited, can be fund, stock, etf
        filters (dict) : filter, use the method search_filter() to find the different possible filter keys
        pageSize (int): number of securities to return
        page (int): page to return
        sortby (str) : sort by a field
        ascending (bool) : True sort by ascending order, False sort by descending order
        itemRange (int) : index of funds to return (must be inferior to PageSize)
        proxies (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}

    Examples:
        >>> Security('0P0000712R', "fund", 9, 0)
        >>> Security('visa', "stock", 25, 2)

    Raises:
        TypeError: raised whenever the parameter type is not the type expected
        ValueError : raised whenever the parameter is not valid or no fund found

    """

    def __init__(
        self,
        term:str,
        language:str="en-gb",
        asset_type:str="",
        filters:dict=None,
        itemRange:int=0,
        pageSize:int=10,
        page:int=1,
        sortby:str=None,
        ascending:bool=True,
        proxies:dict=None,
    ) -> None:
        
        if not isinstance(term, str):
            raise TypeError("term parameter should be a string")
        
        if not isinstance(language, str):
            raise TypeError("language parameter should be a string")
        
        if not isinstance(asset_type, str):
            raise TypeError("asset_type parameter should be a string")

        if not isinstance(pageSize, int):
            raise TypeError("pageSize parameter should be an integer")
        
        if not isinstance(page, int):
            raise TypeError("page parameter should be an integer")
        
        if sortby and not isinstance(sortby, str):
            raise TypeError("sortby parameter should be a string")
    
        if not isinstance(ascending, bool):
            raise TypeError("ascending parameter should be a boolean")

        if not isinstance(itemRange, int):
            raise TypeError("itemRange parameter should be an integer")

        if pageSize <= itemRange:
            raise ValueError(
                "itemRange parameter should be strictly inferior to pageSize parameter"
            )

        if filters and not isinstance(filters, dict):
            raise TypeError("filters parameter should be dict")

        if proxies and not isinstance(proxies, dict):
            raise TypeError("proxies parameter should be dict")
        
        if language not in LANGUAGE:
            raise ValueError(
                f"language parameter can only take one of the values : {', '.join(LANGUAGE)}"
            )


        self.language = language
        self.proxies = proxies
        self.filters = filters
        self.pageSize = pageSize
        self.page = page
        self.sortby = sortby
        self.ascending = ascending
        self.itemRange = itemRange

        self.asset_type = "security"

        code_list = []

        code_list = screener_universe(
                term,
                language=self.language,
                field=["isin", "name"],
                filters=filters,
                pageSize=pageSize, 
                page=page,
                sortby=sortby,
                ascending=ascending,
                proxies=self.proxies,)
        
        if code_list:
            if itemRange < len(code_list):
                self.code = code_list[itemRange]['meta']["securityID"]
                self.name = code_list[itemRange]['fields']["name"]['value']
                self.isin = code_list[itemRange]['fields']["isin"]['value']
                universe = code_list[itemRange]['meta']["universe"]

                if universe == "EQ":
                    self.asset_type = "stock"
                elif universe == "FE":
                    self.asset_type = "etf"
                elif universe == "FO":
                    self.asset_type = "fund"
                elif universe == "FC":
                    self.asset_type = "cef"

                if universe == "EQ" and asset_type in ["etf", "fund"]:
                    raise ValueError(
                        f"The security found with the term {term} is a stock and the parameter asset_type is equal to {asset_type}, the class Stock should be used with this security."
                    )

                if universe in ["FO", "FE", "FC"] and asset_type == "stock":
                    if universe == "FO":
                        raise ValueError(
                            f"The security found with the term {term} is a Open-end fund and the parameter asset_type is equal to {asset_type}, the class Fund should be used with this security."
                        )
                    elif universe == "FE":
                        raise ValueError(
                            f"The security found with the term {term} is an ETF and the parameter asset_type is equal to {asset_type}, the class Fund should be used with this security."
                        )
                    else:
                        raise ValueError(
                            f"The security found with the term {term} is a Closed-end fund and the parameter asset_type is equal to {asset_type}, the class Fund should be used with this security."
                        )


            else:
                raise ValueError(
                    f"Found only {len(code_list)} {self.asset_type} with the term {term}. The paramater itemRange must maximum equal to {len(code_list)-1}"
                )
        else:
            raise ValueError(f"0 {self.asset_type} found with the term {term}")



    def dataPoint(self, 
                  field:str|list) -> list[dict]:
        """
        This function retrieves infos about securities such as name,
        performance, risk metrics...

        Args:
        field (str or list) : field to find

        Returns:
            list of dict security infos

        Example:
            >>> Security("myria").dataPoint(['name', 'isin', 'priipsKidCosts'])
            >>> Security("myria").dataPoint('standardDeviation')

        """

        result =  screener_universe(
            self.isin, 
            language=self.language,
            field=field,
            filters=self.filters,
            proxies=self.proxies,
            pageSize=self.pageSize,
            page=self.page,
            sortby=self.sortby,
            ascending=self.ascending,
        )
        
        return result[self.itemRange]['fields']
        
    
    def GetData(self, 
                field:str, 
                params:dict=None, 
                headers:dict=None, 
                url_suffix:str="data") -> dict|list:
        """
        This function retrieves data from the MorningStar global API.
        Args:
            field (str) : endpoint of the request
            params (dict) : parameter for the request
            headers (dict) : headers of the request
            url_suffix (str) : suffix of the url

        Raises:
            TypeError raised whenever type of paramater are invalid

        Returns:
            dict with data

        Examples:
            >>> Security("rmagx").GetData("price/feeLevel")

        """

        if not isinstance(field, str):
            raise TypeError("field parameter should be a string")

        if params and not isinstance(params, dict):
            raise TypeError("params parameter should be a dict")

        if not isinstance(url_suffix, str):
            raise TypeError("url_suffix parameter should be a string")
        
        if headers and not isinstance(headers, dict):
            raise TypeError("headers parameter should be a dict")

        # url of API
        url = f"""https://api-global.morningstar.com/sal-service/v1/{self.asset_type}/{field}/{self.code}"""

        if url_suffix:
            url += f"""/{url_suffix}"""

        # headers
        default_headers = {
            "apikey": APIKEY,
        }
        if headers:
            default_headers = default_headers | headers

        #params 
        default_params = {
            "clientId": "MDC",
            "version": "4.71.0"

        }
        if params:
            default_params = default_params | params


        response = requests.get(
            url, params=default_params, headers=default_headers, proxies=self.proxies
        )

        not_200_response(url, response)

        return response

    def ltData(self, 
               field:str, 
               currency:str="EUR") -> dict:
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
            >>> Security("rmagx").ltData("price/feeLevel")

        """
        if not isinstance(field, str):
            raise TypeError("field parameter should be a string")

        # url of API
        url = f"""https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security_details/{self.code}"""

        params = {
            "viewId": field,
            "currencyId": currency,
            "itype": "msid",
            "languageId": "en",
            "responseViewFormat": "json",
        }
        response = requests.get(url, params=params, proxies=self.proxies)

        not_200_response(url, response)

        # responseis a list
        response_list = response.json()
        if response_list:
            return response_list[0]
        else:
            return {}

    def RealtimeData(self, 
                     url_suffix: str) -> dict:
        """
        This function retrieves historical data of the specified fields

        Args:
            url_suffix (str) : suffixe of the url

        Returns:
            dict of realtime data

        Examples:
            >>> Security("visa").RealtimeData("quotes")

        Raises:
            TypeError: raised whenever the parameter type 
            is not the type expected
            ConnectionError : raised whenever the response is not 200 OK

        """
        # error raised if url_suffix is not a string
        if not isinstance(url_suffix, str):
            raise TypeError("url_suffix parameter should be a string or a list")
        # url for realtime data
        url = f"""https://www.morningstar.com/api/v2/stores/realtime/{url_suffix}"""

        # header with user agent
        headers = {
                    'user-agent': random_user_agent(), 
                    }
        #parameters of the request
        params = {"securities": self.code}
        # response
        response = requests.get(url, 
                                params=params, 
                                headers=headers, 
                                proxies=self.proxies,
                                timeout=60)
        # manage response
        not_200_response(url, response)
        # result
        return response.json()
    
    def TimeSeries(self, 
                   field:str|list, 
                   start_date:datetime.datetime,
                   end_date:datetime.datetime,
                   frequency:str="daily") -> list:
        """
        This function retrieves historical data of the specified fields

        Args:
            field (str|list) : field to retrieve, can be a string or a list of string
            start_date (datetime) : start date to get history
            end_date (datetime) : end date to get history
            frequency (str) : can be daily, weekly, monthly

        Returns:
            list of dict time series

        Examples:
            >>> Security("RMAGX").TimeSeries(["nav","totalReturn"],datetime.datetime.today()- datetime.timedelta(30),datetime.datetime.today())

        Raises:
            TypeError: raised whenever the parameter type is not the type expected
            ValueError : raised whenever the parameter is not valid or no funds found

        """

        # error raised if field is not a string or a list
        if not isinstance(field, (str, list)):
            raise TypeError("field parameter should be a string or a list")

        # error raised if start_date is note a datetime.date
        if not isinstance(start_date, datetime.date):
            raise TypeError("start_date parameter should be a datetime.date")

        # error raised if end_date is note a datetime.date
        if not isinstance(end_date, datetime.date):
            raise TypeError("end_date parameter should be a datetime.date")

        # error if end_date < start_date
        if end_date < start_date:
            raise ValueError("end_date must be more recent than start_date")

        # error raised if frequency is not a string
        if not isinstance(frequency, str):
            raise TypeError("frequency parameter should be a string")

        # dict of frequency
        frequency_row = {"daily": "d", "weekly": "w", "monthly": "m"}

        if self.asset_type == "stock":
            frequency_row = {"daily": "d", 
                             "5min": "5", 
                             "10min": "10", 
                             "15min": "15", 
                             "30min": "30",
                             }
        else:
            frequency_row = {"daily": "d", "monthly": "m", "quarterly": "q"}


        # raise an error if frequency is not daily, wekly or monthly
        if frequency not in frequency_row:
            raise ValueError(
                f"frequency parameter must take one of the following value : { ', '.join(frequency_row.keys())}"
            )

        if isinstance(field, list):
            queryField = ",".join(field)
        else:
            queryField = field

        # bearer token
        bearer_token = token_chart()
        # url for nav
        url = "https://www.us-api.morningstar.com/QS-markets/chartservice/v2/timeseries"
        # header with bearer token
        headers = {
            "user-agent": random_user_agent(),
            "authorization": f"Bearer {bearer_token}",
        }
        #params of the request
        params ={
            "query" : f"{self.code}:{queryField}",
            "frequency": frequency_row[frequency],
            "startDate": start_date.strftime('%Y-%m-%d'),
            "endDate": end_date.strftime('%Y-%m-%d'),
            "trackMarketData": "3.6.3",
            "instid": "DOTCOM",
        }
        # response
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        # manage response
        not_200_response(url, response)
        # result
        result = response.json()
        # return empty list if we don't get data
        if not result:
            return []
        if "series" in result[0]:
            return result[0]["series"]

        return []
