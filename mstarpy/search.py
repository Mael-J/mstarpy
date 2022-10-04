import requests
import json
from bs4 import BeautifulSoup
import re

from .utils import random_user_agent
from .utils import SITE, FIELDS
from .error import not_200_response




def get_bearer_token():
  """
  This function will scrape the Bearer Token needed to access MS API

  Returns:
  str bearer token
  """
  url = 'https://www.morningstar.co.uk/Common/funds/snapshot/PortfolioSAL.aspx'

  headers = {'user-agent' : random_user_agent()}


  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  script = soup.find('script', {'type':'text/javascript'})
  bearerToken = str(script).split('tokenMaaS:')[-1].split('}')[0].replace('"','').strip()
  return bearerToken

def search_field(pattern = ''):
  """
  This function retrieves the fields possible for the function dataPoint

  Args:
  pattern (str) : text contained in the field

  Returns:
      list of fields possible for the method dataPoint

  Example:
      >>> search_field('fee')
      >>> search_field('return')
      
      ['FeeLevel', 'PerformanceFeeActual', 'TransactionFeeActual']
      ['GBRReturnD1', 'GBRReturnM0', 'GBRReturnM1', 'GBRReturnM12', 'GBRReturnM120', 'GBRReturnM3', 'GBRReturnM36', 'GBRReturnM6', 'GBRReturnM60', 'GBRReturnW1', 'ReturnD1', 'ReturnM0', 'ReturnM1', 'ReturnM12', 'ReturnM120', 'ReturnM3', 'ReturnM36', 'ReturnM6', 'ReturnM60', 'ReturnProfileGrowth', 'ReturnProfileHedging', 'ReturnProfileIncome', 'ReturnProfileOther', 'ReturnProfilePreservation', 'ReturnW1', 'totalReturn', 'totalReturnTimeFrame']

  """

  regex = re.compile(f'(?i){pattern}')
  filtered_list = list(filter(lambda field : regex.search(field),FIELDS))
  print(f"possible fields for can be : {', '.join(filtered_list)}")

  return filtered_list

def search_funds(term, field, country = "", pageSize=10, currency ='EUR'):
  """
  This function will use the screener of morningstar.co.uk to find funds which include the term.

  Args:
    term (str): text to find a funds can be a the name, part of a name or the isin of the funds
    field (str) : field to find
    country (str) : text for code ISO 3166-1 alpha-2 of country
    pageSize (int): number of funds to return

  Returns:
    list of dict with SecId, TenforId and LegalName
      [{'SecId': 'F00000270E', 'TenforeId': '52.8.FR0010342600', 'LegalName': '21 Gestion Active'}, {'SecId': 'F000013BGI', 'TenforeId': '52.8.MT7000022612', 'LegalName': '24 Capital Management SICAV plc - 24 Global Currency Fund Share Class A USD Accumulation'}, {'SecId': 'F00000PZHI', 'TenforeId': '52.8.FR0011443225', 'LegalName': '29 Haussmann Actions Europe C'}, {'SecId': 'F0GBR06QS1', 'TenforeId': '52.8.FR0007057427', 'LegalName': '29 Haussmann Actions Europe D'}, {'SecId': 'F0000101BL', 'TenforeId': '52.8.FR0013266590', 'LegalName': '29 Haussmann Actions Europe 
      I'}, {'SecId': 'F00000JW7U', 'TenforeId': '52.8.LU0532306957', 'LegalName': '3F Generation Acc'}, {'SecId': 'F00000UDVR', 'TenforeId': '52.8.FR0011911189', 'LegalName': 'AAM Family Values E1'}, {'SecId': 'F00000UDVS', 'TenforeId': '52.8.FR0011911197', 'LegalName': 'AAM Family Values 
      I'}, {'SecId': 'F0GBR04RG5', 'TenforeId': '52.8.FR0007022025', 'LegalName': 'AAZ Capitalisation'}, {'SecId': 'F000000ITD', 'TenforeId': '52.8.FR0010361600', 'LegalName': 'AAZ Prestige Or'}]
    
    str if the screener find no funds which match the term
      '0 funds found whith the term rzt'
      

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



  #url
  url = "https://tools.morningstar.co.uk/api/rest.svc/klr5zyak8x/security/screener"

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
  }

  #headers
  headers = {
              'user-agent': random_user_agent(),
              }   

  response = requests.get(url,params=params, headers=headers)

  not_200_response(url, response)
    
  result =json.loads(response.content.decode())

  if result['rows']:
    return result['rows']
  else:
    print('0 funds found whith the term %s' % (term))
    return {}


    
        

