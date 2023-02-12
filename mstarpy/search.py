import requests
import json
from bs4 import BeautifulSoup
import re

from .utils import random_user_agent
from .utils import SITE, FIELDS, FILTER
from .error import not_200_response

def filter_universe(field = FILTER, proxies = {}):
  """
  This function will use the screener of morningstar.co.uk to find the possible filters and their values.

  Args:
    
    field (str | list) : field to find

  Returns:
    dict of filter
      {'LargestRegion': ['', 'RE_AfricaDeveloped', 'RE_AfricaEmerging', 'RE_Asia4TigersEmerging', 'RE_Asiaex4TigersEmerging', 'RE_Australasia', 'RE_Canada', 'RE_CentralandEasternEurope', 'RE_CentralandLatinAmericaEmerging', 'RE_Japan', 'RE_UnitedKingdom', 'RE_UnitedStates', 'RE_WesternEuropeEuro', 'RE_WesternEuropeNonEuroexUK'], 'SustainabilityRank': ['1', '2', '3', '4', '5']}
    
  Examples:
    >>> filter_universe(['LargestRegion','SustainabilityRank'])
    >>> filter_universe('FeeLevel')
    

  """
  
  if not isinstance(field, (str, list)):
    raise TypeError('field parameter should be a string or a list')

  if 'StarRatingM255' in field:
    raise ValueError('StarRatingM255 cannot be a field')
  
  if isinstance(field, list):
    filterDataPoints = '|'.join(field)
  else:
    filterDataPoints = field

  if not isinstance(proxies, dict):
    raise TypeError('proxies parameter should be dict')

  params = {
  'outputType' : 'json',
  'filterDataPoints' : filterDataPoints,
  }

  result = general_search(params, proxies=proxies)

  all_filter ={}

  if "filters" not in result:
    return all_filter
  if not result['filters']:
    return all_filter

  for r in result['filters'][0]:
    all_filter[list(r)[0]] = r[list(r)[0]]
  
  return all_filter


def general_search(params, proxies={}):
  """
  This function will use the screener of morningstar.co.uk to find informations about funds or classification

  Args:
    params (dict) : paramaters of the request
    proxies (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}
  
  Returns:
    list of information

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
    raise TypeError('params parameter should be dict')

  if not isinstance(proxies, dict):
    raise TypeError('proxies parameter should be dict')
  #url
  url = "https://tools.morningstar.co.uk/api/rest.svc/klr5zyak8x/security/screener"
  #headers
  headers = {
              'user-agent': random_user_agent(),
              }   

  response = requests.get(url,params=params, headers=headers,proxies=proxies)

  not_200_response(url, response)
    
  return json.loads(response.content.decode())


def search_field(pattern = ''):
  """
  This function retrieves the possible fields for the function dataPoint

  Args:
  pattern (str) : text contained in the field

  Returns:
      list of possible fields for the method dataPoint

  Example:
      >>> search_field('feE')
      >>> search_field('reTurn')
      
      ['FeeLevel', 'PerformanceFeeActual', 'TransactionFeeActual']
      ['GBRReturnD1', 'GBRReturnM0', 'GBRReturnM1', 'GBRReturnM12', 'GBRReturnM120', 'GBRReturnM3', 'GBRReturnM36', 'GBRReturnM6', 'GBRReturnM60', 'GBRReturnW1', 'ReturnD1', 'ReturnM0', 'ReturnM1', 'ReturnM12', 'ReturnM120', 'ReturnM3', 'ReturnM36', 'ReturnM6', 'ReturnM60', 'ReturnProfileGrowth', 'ReturnProfileHedging', 'ReturnProfileIncome', 'ReturnProfileOther', 'ReturnProfilePreservation', 'ReturnW1', 'totalReturn', 'totalReturnTimeFrame']

  """

  regex = re.compile(f'(?i){pattern}')
  filtered_list = list(filter(lambda field : regex.search(field),FIELDS))
  print(f"possible fields for function dataPoint can be : {', '.join(filtered_list)}")

  return filtered_list


def search_filter(pattern = ''):
  """
  This function retrieves the possible filters for the parameter filters of the function search_funds
  

  Args:
  pattern (str) : text contained in the filter

  Returns:
      list of possible filters

  Example:
      >>> search_filter('RetUrn')
      >>> search_filter('id')
      
      ['GBRReturnM0', 'GBRReturnM12', 'GBRReturnM120', 'GBRReturnM36', 'GBRReturnM60', 'ReturnProfilePreservation']
      ['AdministratorCompanyId', 'BrandingCompanyId', 'CategoryId', 'GlobalAssetClassId', 'GlobalCategoryId', 'IMASectorID', 'ShareClassTypeId', 'UmbrellaCompanyId']

  """

  regex = re.compile(f'(?i){pattern}')
  filtered_list = list(filter(lambda field : regex.search(field),FILTER))
  print(f"possible keys for the parameter filters of the method seach_funds can be : {', '.join(filtered_list)}")

  return filtered_list


def search_funds(term, field, country = "", pageSize=10, currency ='EUR', filters={}, proxies = {}):
  """
  This function will use the screener of morningstar.co.uk to find funds which include the term.

  Args:
    term (str): text to find a funds can be a the name, part of a name or the isin of the funds
    field (str | list) : field to find
    country (str) : text for code ISO 3166-1 alpha-2 of country
    pageSize (int): number of funds to return
    currency (str) : currency in 3 letters

  Returns:
    list of dict with SecId, TenforId and LegalName
      [{'SecId': 'F00000270E', 'TenforeId': '52.8.FR0010342600', 'LegalName': '21 Gestion Active'}, {'SecId': 'F000013BGI', 'TenforeId': '52.8.MT7000022612', 'LegalName': '24 Capital Management SICAV plc - 24 Global Currency Fund Share Class A USD Accumulation'}, {'SecId': 'F00000PZHI', 'TenforeId': '52.8.FR0011443225', 'LegalName': '29 Haussmann Actions Europe C'}, {'SecId': 'F0GBR06QS1', 'TenforeId': '52.8.FR0007057427', 'LegalName': '29 Haussmann Actions Europe D'}, {'SecId': 'F0000101BL', 'TenforeId': '52.8.FR0013266590', 'LegalName': '29 Haussmann Actions Europe 
      I'}, {'SecId': 'F00000JW7U', 'TenforeId': '52.8.LU0532306957', 'LegalName': '3F Generation Acc'}, {'SecId': 'F00000UDVR', 'TenforeId': '52.8.FR0011911189', 'LegalName': 'AAM Family Values E1'}, {'SecId': 'F00000UDVS', 'TenforeId': '52.8.FR0011911197', 'LegalName': 'AAM Family Values 
      I'}, {'SecId': 'F0GBR04RG5', 'TenforeId': '52.8.FR0007022025', 'LegalName': 'AAZ Capitalisation'}, {'SecId': 'F000000ITD', 'TenforeId': '52.8.FR0010361600', 'LegalName': 'AAZ Prestige Or'}]
    
    empty dict str if the screener find no funds which match the term
     
      

  Examples:
    >>> search_funds("Myria",['SecId','TenforeId','LegalName'],country="fr", pageSize=25)
    >>> search_funds("FR0011399914", 'LegalName', country="fr", pageSize=25)
    

  """

  if not isinstance(field, (str, list)):
    raise TypeError('field parameter should be a string or a list')

  if not isinstance(country, str):
    raise TypeError('country parameter should be a string')

  if country and not country.lower() in SITE.keys():
      raise ValueError(f'country parameter can only take one of the values: {", ".join(SITE.keys())}')

  if not isinstance(pageSize, int):
    raise TypeError('pageSize parameter should be an integer')

  if not isinstance(currency, str):
    raise TypeError('currency parameter should be a string')

  if not isinstance(filters, dict):
    raise TypeError('filters parameter should be a dict')

  if not isinstance(proxies, dict):
    raise TypeError('proxies parameter should be dict')


  if isinstance(field, list):
      securityDataPoints = '|'.join(field)
  else:
      securityDataPoints = field
  #if country find iso
  if country:
    iso = SITE[country.lower()]["iso3"]
    universeIds = f'FO{iso}$$ALL'
  else:
    universeIds = ""

  filter_list = []
  #loop on filter dict
  for f in filters:
    if f not in FILTER:
      print(f"{f} is not a valid filter and will be ignored. You can find the possible filters with the method search_filter().")
    else:
      #if list, IN condition
      if isinstance(filters[f], list):
          filter_list.append(f'{f}:IN:{":".join(filters[f])}')
      #if tuple, either, BTW, LT or GT condition
      elif isinstance(filters[f], tuple):
          if len(filters[f]) == 2:
              if isinstance(filters[f][0], (int,float)):
                  filter_list.append(f'{f}:BTW:{filters[f][0]}:{filters[f][1]}')
              elif filters[f][0] =="<":
                  filter_list.append(f'{f}:LT:{filters[f][1]}')
              elif filters[f][0] ==">":
                  filter_list.append(f'{f}:GT:{filters[f][1]}')
      #else IN condition
      else:
          filter_list.append(f'{f}:IN:{filters[f]}')

  print('|'.join(filter_list))
  params = {
  'page' : 1,
  'pageSize' : pageSize,
  'sortOrder' : 'LegalName asc',
  'outputType' : 'json',
  'version' : 1,
  'universeIds' : universeIds,
  'currencyId': currency,
  'securityDataPoints' : securityDataPoints,
  'term' : term,
  'filters' : '|'.join(filter_list),
  }

  result = general_search(params, proxies=proxies)

  if result['rows']:
    return result['rows']
  else:
    print('0 funds found whith the term %s' % (term))
    return {}


def token_chart(proxies={}):
  """
  This function will scrape the Bearer Token needed to access MS API chart data

  Args:
  proxies (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}

  Returns:
  str bearer token
  """

  if not isinstance(proxies, dict):
    raise TypeError('proxies parameter should be dict')

  url = 'https://www.morningstar.com/funds/xnas/afozx/chart'

  headers = {'user-agent' : random_user_agent()}

  response = requests.get(url, headers=headers,proxies=proxies)

  all_text = response.text
  if all_text.find("token") ==-1:
    return None

  token_start =all_text[all_text.find("token"):]
  return token_start[7:token_start.find("}")-1]


def token_fund_information(proxies={}):
  """
  This function will scrape the Bearer Token needed to access MS API funds information

  Args:
  proxies (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}

  Returns:
  str bearer token
  """
  if not isinstance(proxies, dict):
    raise TypeError('proxies parameter should be dict')

  url = 'https://www.morningstar.co.uk/Common/funds/snapshot/PortfolioSAL.aspx'

  headers = {'user-agent' : random_user_agent()}


  response = requests.get(url, headers=headers,proxies=proxies)
  soup = BeautifulSoup(response.text, 'html.parser')
  script = soup.find_all('script', {'type':'text/javascript'})
  bearerToken = str(script).split('tokenMaaS:')[-1].split('}')[0].replace('"','').strip()
  return bearerToken

def token_investment_strategy(proxies={}):
  """
  This function will scrape the Bearer Token needed to access the investment strategy

  Args:
  proxies (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}

  Returns:
  str bearer token
  """
  if not isinstance(proxies, dict):
    raise TypeError('proxies parameter should be dict')

  url = 'https://www.morningstar.com.au/investments/security/ASX/VHY'

  headers = {'user-agent' : random_user_agent()}

  response = requests.get(url, headers=headers, proxies = proxies)

  all_text = response.text
  if all_text.find("token") ==-1:
    return None
  start_flag ='"0P0000T416",0,'
  end_flag = 'www.morningstar.com.au'
  token_start = all_text[all_text.find(start_flag)+len(start_flag)+1:]
  return token_start[:token_start.find(end_flag)-3]