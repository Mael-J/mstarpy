import requests
from bs4 import BeautifulSoup
import re
import warnings
import pandas as pd

from .utils import random_user_agent
from .utils import ASSET_TYPE, EXCHANGE, FIELDS, FILTER_FUND, FILTER_STOCK, FILTER_TYPE
from .error import not_200_response




def general_search(params:dict, 
                   proxies:dict=None) -> dict:
    """
    This function will use the screener of morningstar.com
    to find informations about funds or classification

    Args:
      params (dict) : paramaters of the request
      proxies (dict) : set the proxy if needed,
      example : {"http": "http://host:port","https": "https://host:port"}

    Returns:
      dict of information

    Examples:
      >>> general_search(params = {
                                  'page' : 1,
                                  'pageSize' : 10,
                                  'sortOrder' : 'LegalName asc',
                                  'outputType' : 'json',
                                  'version' : 1,
                                  'universeIds' : 'FOFRA$$ALL',
                                  'currencyId': 'EUR',
                                  'securityDataPoints' : ['FundTNAV','GBRReturnD1'],
                                  'term' : 'myria',
                                  })


    """

    if not isinstance(params, dict):
        raise TypeError("params parameter should be dict")

    if proxies and not isinstance(proxies, dict):
        raise TypeError("proxies parameter should be dict")
    # url
    url = "https://global.morningstar.com/api/v1/en/tools/screener/_data"
    # headers
    headers = {
        "user-agent": random_user_agent(),
    }

    response = requests.get(url, params=params, headers=headers, proxies=proxies)

    not_200_response(url, response)

    return response.json()


def search_field(pattern:str="",
                 display_print=True) -> list:
    """
    This function retrieves the possible fields for the screener 

    Args:
    pattern (str) : text contained in the field
    display_print (bool) : if True, print the possible fields

    Returns:
        list of possible fields for the screener of securities

    Example:
        >>> search_field('feE')
        >>> search_field('reTurn')

    """
    if not isinstance(pattern, str):
        raise TypeError("pattern parameter should be a string")
    
    headers = {"user-agent": random_user_agent()}
    
    url = "https://global.morningstar.com/api/v1/fr/stores/data-points/fields"

    response = requests.get(url, headers=headers)
    not_200_response(url, response)
    if "results" not in response.json():
        raise ValueError("No results found for the given pattern")
    
    result = response.json()["results"]
    df = pd.DataFrame(result)
    df_filtered = df.loc[df["field"].str.contains(f"(?i){pattern}",regex=True)]
    filtered_list = df_filtered["field"].tolist()

    if display_print:
        print(f"possible fields for screener can be : {', '.join(filtered_list)}")

    return filtered_list



def search_filter(pattern:str="",
                asset_type:str="",
                filter_type:str="",
                explicit:bool=False) -> list:
                  
    """
    This function retrieves the possible filters for the parameter filters of the function screener_universe

    Args:
        pattern (str): text contained in the field
        asset_type (str): type of asset, can be one of the values in ASSET_TYPE
        filter_type (str): type of filter, can be one of the values in FILTER_TYPE
        explicit (bool): if True, return a list of dict with fields and their metadata
    Returns:
        list of possible filters
        Raise[{'field': 'dividendYield', 'label': 'Dividend Yield (%)', 
        'numeric': True, 'type': 'range', 'options': 
        {'type': [{'text': 'Forward', 'value': 'forward'}, 
        {'text': 'Trailing', 'value': 'trailing', 'default': True}]}}]

        ['stockStyleBox', 'fundEquityStyleBox', 'fundFixedIncomeStyleBox', 'fundAlternativeStyleBox']
    Example:
        >>> search_filter()
        >>> search_filter(pattern="div",asset_type="stock", filter_type="dividends", explicit=True)

    """

    if not isinstance(pattern, (str)):
        raise TypeError("pattern parameter should be a string")
    if not isinstance(asset_type, (str)):
        raise TypeError("asset_type parameter should be a string")
    
    if asset_type and asset_type not in ASSET_TYPE:
        raise TypeError(
            f"asset_type parameter can only take one of the values : {','.join(ASSET_TYPE)}"
        )
    if not isinstance(filter_type, (str)):
        raise TypeError("filter_type parameter should be a string")
    
    if filter_type and filter_type not in FILTER_TYPE:
        raise TypeError(
            f"filter_type parameter can only take one of the values : {','.join(FILTER_TYPE)}"
        )
    
    headers = {"user-agent": random_user_agent()}
    url = "https://global.morningstar.com/api/v1/fr/stores/filters"

    response = requests.get(url, headers=headers)
    not_200_response(url, response)

    result = response.json()

    list_filter = ["investmentType","countriesOfSale"]
    list_filter_explicit = []
    for security_type in result["results"]:
        if asset_type:
            if security_type["id"] != f"{asset_type}-filters":
                continue
        security_filter_type = security_type["filters"]
        for filters in security_filter_type:
            if filter_type:
                if filter_type != filters["id"]:
                    continue
            for child in filters["children"]:
                if pattern:
                    if not re.search(pattern, child["field"], re.IGNORECASE):
                        continue
                if child["field"] in list_filter:
                    continue
                list_filter.append(child["field"])
                list_filter_explicit.append(child)
    if explicit:
        return list_filter_explicit
    return list_filter
    

def screener_universe(
    term:str, 
    field:str|list="",
    filters:dict=None,
    pageSize:int=10,
    page:int=1,
    proxies:dict=None
    ) -> list:
    """
    This function will use the screener of global.morningstar.com
    to find funds, etf, stocks which include the term.

    Args:
      term (str): text to find a security can be a the name, 
      part of a name or the isin
      field (str | list) : field to find
      pageSize (int): number of securities to return
      filters (dict) : filter, use the method search_filter() 
      to find the different possible filter keys
      proxies (dict) : set the proxy if needed , example : 
      {"http": "http://host:port","https": "https://host:port"}

    Returns:
      list of dict with fund information
        [{'SecId': 'F00000270E', 'TenforeId': '52.8.FR0010342600',
        'LegalName': '21 Gestion Active'}, {'SecId': 'F000013BGI',
        'TenforeId': '52.8.MT7000022612', 'LegalName':'24 Capital Management SICAV plc - 
        24 Global Currency Fund Share Class A USD Accumulation'}, 
        {'SecId': 'F00000PZHI', 'TenforeId': '52.8.FR0011443225', 
        'LegalName': '29 Haussmann Actions Europe C'}, {'SecId': 'F0GBR06QS1', 
        'TenforeId': '52.8.FR0007057427', 'LegalName': '29 Haussmann Actions Europe D'}, 
        {'SecId': 'F0000101BL', 'TenforeId': '52.8.FR0013266590', 'LegalName': 
        '29 Haussmann Actions Europe
        I'}, {'SecId': 'F00000JW7U', 'TenforeId': '52.8.LU0532306957', 
        'LegalName': '3F Generation Acc'}, {'SecId': 'F00000UDVR', 
        'TenforeId': '52.8.FR0011911189', 'LegalName': 'AAM Family Values E1'}, 
        {'SecId': 'F00000UDVS', 'TenforeId': '52.8.FR0011911197', 'LegalName': 'AAM Family Values
        I'}, {'SecId': 'F0GBR04RG5', 'TenforeId': '52.8.FR0007022025', 'LegalName': 
        'AAZ Capitalisation'}, 
        {'SecId': 'F000000ITD', 'TenforeId': '52.8.FR0010361600', 
        'LegalName': 'AAZ Prestige Or'}]

    Examples:
      >>> search_funds("Myria",['SecId','TenforeId','LegalName'],country="fr", pageSize=25)
      >>> search_funds("FR0011399914", 'LegalName', country="fr", pageSize=25)

    """
    if not isinstance(term, str):
        raise TypeError("term parameter should be a string")
    
    if not isinstance(field, (str, list)):
        raise TypeError("field parameter should be a string or a list")
    
    if not isinstance(filters, dict):
        raise TypeError("filters parameter should be a dict")
    
    if not isinstance(pageSize, int):
        raise TypeError("pageSize parameter should be an integer")
    
    if not isinstance(page, int):
        raise TypeError("page parameter should be an integer")

    if proxies and not isinstance(proxies, dict):
        raise TypeError("proxies parameter should be dict")
    
    all_fields = search_field(display_print=False)
    if not field:
        check_field = True
    elif isinstance(field, str):
        check_field = field in all_fields
        fields = field
    else:
        check_field = set(field).issubset(set(all_fields))
        fields = ",".join(field)

    if not check_field:
        raise ValueError(
            f"""The field {field} is not a valid field.
            You can find the possible fields with the method search_field().
            Possible fields are : {', '.join(all_fields)}"""
        )
    
    query_params = f"_ ~= '{term}'"

    if filters:
        list_filter =search_filter()
        for f in filters:
            if f not in list_filter:
                warnings.warn(
                    f"""{f} is not a valid filter and will be ignored.
                    You can find the possible filters with the method search_filter()."""
                )
            else:
                # if list, IN condition
                if isinstance(filters[f], list):
                    query_params += f""" AND {f} IN ({','.join(f"'{x}'" for x in filters[f])})"""
                # if tuple, either, < or > condition
                elif isinstance(filters[f], tuple):
                    if len(filters[f]) != 2:
                        warnings.warn(f"""{f} is not a valid filter and will be ignored.
                                      The tuple has to be of a length of 2""")
                    if filters[f][0] not in ['<','<=','>=', '>']:
                         warnings.warn(f"""{f} is not a valid filter and will be ignored.
                                       The first argument of the tuple has to be one of this value {','.join(['<','<=','>=', '>'])}""")
                    if isinstance(filters[f][1,(int,float)]):
                        warnings.warn(f"""{f} is not a valid filter and will be ignored.    
                                        The second argument of the tuple has be a number.
                                            """)
                    query_params += f" AND {f} {filters[f][0]} {filters[f][1]}"
                # else IN condition
                else:
                    query_params += f" AND {f} = '{filters[f]}'"
        
    params = {
        "query": query_params,
        "fields" : fields,
        "limit": pageSize,

    }

    result = general_search(params, proxies=proxies)

    if not "results" in result:
        print(f"0 fund found whith the term {term}")
        return {}
    
    return result["results"]



def token_chart(proxies:dict=None) -> str:
    """
    This function will scrape the Bearer Token needed to access MS API chart data

    Args:
    proxies (dict) : set the proxy if needed ,
    example : {"http": "http://host:port","https": "https://host:port"}

    Returns:
    str bearer token

    """

    if proxies and not isinstance(proxies, dict):
        raise TypeError("proxies parameter should be dict")

    url = "https://www.morningstar.com/funds/xnas/afozx/chart"

    headers = {"user-agent": random_user_agent()}

    response = requests.get(url, headers=headers, proxies=proxies)

    all_text = response.text
    if all_text.find("token") == -1:
        return None

    token_start = all_text[all_text.find("token") :]
    return token_start[7 : token_start.find("}") - 1]


def token_fund_information(proxies:dict=None) -> str:
    """
    This function will scrape the Bearer Token needed to access MS API funds information

    Args:
    proxies (dict) : set the proxy if needed , example :
    {"http": "http://host:port","https": "https://host:port"}

    Returns:
    str bearer token

    """
    if proxies and not isinstance(proxies, dict):
        raise TypeError("proxies parameter should be dict")

    url = "https://www.morningstar.co.uk/Common/funds/snapshot/PortfolioSAL.aspx"

    headers = {"user-agent": random_user_agent()}

    response = requests.get(url, headers=headers, proxies=proxies, timeout=120)
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find_all("script", {"type": "text/javascript"})
    bearerToken = (
        str(script).rsplit("tokenMaaS:",maxsplit=1)[-1].split("}")[0].replace('"', "").strip()
    )
    return bearerToken


def token_investment_strategy(proxies:dict=None) -> str:
    """
    This function will scrape the Bearer Token needed to access the investment strategy

    Args:
    proxies (dict) : set the proxy if needed , example :
    {"http": "http://host:port","https": "https://host:port"}

    Returns:
    str bearer token

    """
    if proxies and not isinstance(proxies, dict):
        raise TypeError("proxies parameter should be dict")

    url = "https://www.morningstar.com.au/investments/security/ASX/VHY"

    headers = {"user-agent": random_user_agent()}

    response = requests.get(url, headers=headers, proxies=proxies, timeout=120)

    all_text = response.text
    if all_text.find("token") == -1:
        return None
    start_flag = ',"'
    end_flag = '"www.morningstar.com.au"'
    token_end = all_text[: all_text.find(end_flag) - 3]
    return token_end[token_end.rfind(start_flag) + 2 :]
