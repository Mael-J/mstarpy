import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

from .utils import random_user_agent
from .utils import SITE, FIELDS
from .search import search_funds, get_bearer_token



class MS:

    def __init__(self, term = None, country: str = "uk", pageSize : int =1, itemRange: int = 0):

        """
        Main class to access MS Data

        Args:
        term (str): text to find a funds can be a the name, part of a name or the isin of the funds
        country (str) : text for code ISO 3166-1 alpha-2 of country
        pageSize (int): number of funds to return
        itemRange (int) : index of funds to return (must be inferior to PageSize)

        Examples:
            >>> MS('0P0000712R', "ca", 9, 0)
            >>> MS('bond', "uk", 25, 2)

        """
        
        
        if not isinstance(country, str):
            raise TypeError('country parameter should be a string')

        if not country.lower() in SITE.keys():
            raise ValueError(f'country parameter can only take one of the values: {", ".join(SITE.keys())}')

        if not isinstance(pageSize, int):
            raise TypeError('pageSize parameter should be an integer')

        if not isinstance(itemRange, int):
            raise TypeError('itemRange parameter should be an integer')

        if pageSize <= itemRange :
            raise ValueError('itemRange parameter should be strictly inferior to pageSize parameter')


        self.site = SITE[country.lower()]["site"]
        
        self.iso3 = SITE[country.lower()]["iso3"]

        self.country = country
        
        code_list = search_funds(term,['SecId','TenforeId','LegalName'], country, pageSize)

        
        if code_list:
            if itemRange < len(code_list):
                self.code = code_list[itemRange]["SecId"]
                self.name = code_list[itemRange]["LegalName"]
                if "TenforeId" in code_list[itemRange]:
                    self.isin = code_list[itemRange]["TenforeId"][-12:]
                else:
                    self.isin = None
            else:
                raise ValueError(f'Found only {len(code_list)} funds found with the term {term}. The paramater itemRange must maximum equal to {len(code_list)-1}')
        else:
            raise ValueError(f'0 funds found with the term {term}')
        


    
    def carbonMetrics(self):
        """
        Returns:
        dict with Carbon Metrics
        """
        

        
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/esg/carbonMetrics/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-carbon-metrics",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-EN,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            
            result =json.loads(response.content.decode()) 
        else:
            print("carbonMetrics",response)
            result = {}
        return result

    def esgData(self):
        """        
        Returns:
        dict with ESG Data
        
        """

        
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/esg/v1/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-sustainability",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            
            result =json.loads(response.content.decode()) 
        else:
            print("esgData",response)
            result = {}
        return result

    def creditQuality(self):
        """        
        Returns:
        dict with credit quality data
        
        """


        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/portfolio/creditQuality/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-credit-quality",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            
            result =json.loads(response.content.decode()) 
        else:
            print("creditQuality", response)
            result = {}
        return result

    def fixedIncomeStyle(self):
        """        
        Returns:
        dict with credit fixed income data
        
        """

        
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/process/fixedIncomeStyle/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-fixed-income-style",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            
            result =json.loads(response.content.decode()) 
        else:
            print("fixedIncomeStyle", response)
            result = {}
        return result

    def sector(self):
        """        
        Returns:
        dict with sector data
        
        """

        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/portfolio/v2/sector/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-sector-exposure",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            
            result =json.loads(response.content.decode()) 
        else:
            print("sector",response)
            result = {}
        return result

    def financialMetrics(self):
        """        
        Returns:
        dict with financial ratio
        
        """

        
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/process/financialMetrics/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-financial-metrics",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            
            result =json.loads(response.content.decode()) 
        else:
            print("financialMetrics",response)
            result = {}
        return result

    def marketCapitalization(self):
        """        
        Returns:
        dict with market capitalization
        
        """

        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/process/marketCap/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-market-cap",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
        
            result =json.loads(response.content.decode()) 
        else:
            print("marketCapitalization", response)
            result = {}
        return result

    def stockStyle(self):
        """        
        Returns:
        dict with stocks data
        
        """
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/process/stockStyle/v2/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-measures",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
        
            result =json.loads(response.content.decode()) 
        else:
            print("stockStyle", response)
            result = {}
        return result

    def factorProfile(self):
        """        
        Returns:
        dict factor profile
        
        """
        
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/factorProfile/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-factor-profile",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
        
            result = json.loads(response.content.decode()) 
        else:
            print("factorProfile", response)
            result = {}
        return result

    def ownershipZone(self):
        """        
        Returns:
        dict ownership zone
        
        """
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/process/ownershipZone/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-stock-style",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
        
            result =json.loads(response.content.decode())
        else:
            print("get_ownershipZone", response)
            result = {}
        return result

    def assetAllocation(self):
        """        
        Returns:
        dict asset allocation
        
        """

        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/process/asset/v2/%s/data""" % (self.code)

        #params
        params = {
                "languageId": "en-GB",
                "locale": "en-GB",
                "clientId": "MDC_intl",
                "benchmarkId": "mstarorcat",
                "component": "sal-components-mip-asset-allocation",
                "version": "3.60.0"
        }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            result = json.loads(response.content.decode())
        else:
            print("assetAllocation", response)
            result = {}
        return result



    def holdings(self, holdingType: str = 'all'):
        """        
        Returns:
        pandas DataFrame with funds holdings
        
        """
        holdingType_to_holdingPage = {"all" : "all", "bond" : "boldHoldingPage","equity" : "equityHoldingPage", "other": "otherHoldingPage"}
        if holdingType not in holdingType_to_holdingPage:
            raise ValueError(f'parameter holdingType must take one of the following value : {", ".join(holdingType_to_holdingPage.keys())}  ')
    
        if holdingType == "all":
            return pd.DataFrame(self.position()["equityHoldingPage"]["holdingList"] + 
            self.position()["boldHoldingPage"]["holdingList"] + self.position()["otherHoldingPage"]["holdingList"] )
        else:
           return pd.DataFrame(self.position()[holdingType_to_holdingPage[holdingType]]["holdingList"])



    
    def position(self):
        """        
        Returns:
        dict with positions
        
        """

        
        #url of API
        url = """https://www.us-api.morningstar.com/sal/sal-service/fund/portfolio/holding/v2/%s/data""" % (self.code)

        #params
        params = {
            'premiumNum': '1000',
            'freeNum': '1000',
            'languageId': 'en-GB',
            'locale': 'en-GB',
            'clientId': 'MDC_intl',
            'benchmarkId': 'category',
            'component': 'sal-components-mip-holdings',
            'version': '3.40.1'
            }

        #headers
        headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': 'Bearer %s' % (get_bearer_token()),
                    'credentials': 'omit',
                    'origin': 'https://www.morningstar.co.uk',
                    'referer': 'https://www.morningstar.co.uk/',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': random_user_agent(),
                    'X-API-RequestId': '6c20ob56-8055-aa34-9632-5f5a0dbbvboi',
                    'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='
                    }    
        response = requests.get(url,params=params, headers=headers)
        if response.status_code == 200:
            result =json.loads(response.content.decode())
            
        else:
            print("position", response)
            result = {}
        return result


    def objectiveInvestment(self):
        """        
        Returns:
        str objective investment
        
        """
        
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #Page 1 - overview
        #url page overview
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}"
        #get HTML page overview
        response = requests.get(url, headers=headers)
        #if page not found
        
        if response.status_code != 200:
            raise ConnectionError(f"error {response.status_code}")
        else:
            #html page as soup
            soup = BeautifulSoup(response.text, 'html.parser')
            #investment objective funds
            return soup.find(id='overviewObjectiveDiv').find('td', {"class": "value text"}).text

    
    def referenceIndex(self, index):
        """
        Args:
            index (str) : possible values are benchmark, category     
        Returns:
            str category or benchmark

        Examples:
            >>> MS.referenceIndex("category")
            >>> MS.referenceIndex("benchmark")
        
        """
        
        index_row = {'benchmark' : 0,'category' : 1}
        if index not in index_row:
            raise ValueError(f"index parameter must take one of the following value : { ', '.join(index_row.keys())}")

                #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #Page 1 - overview
        #url page overview
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}"
        #get HTML page overview
        response = requests.get(url, headers=headers)
        #if page not found
        
        if response.status_code != 200:
            raise ConnectionError(f"error {response.status_code}")
        else:
            #html page as soup
            soup = BeautifulSoup(response.text, 'html.parser')
            benchmark_soup = soup.find(id='overviewBenchmarkDiv2Cols').find_all('td', {"class": "value text"})
            return benchmark_soup[index_row[index]].text


    def benchmark(self):
        """
        Returns:
            str benchmark
        """
        return self.referenceIndex("benchmark")


    def category(self):
        """
        Returns:
            str benchmark
        """
        return self.referenceIndex("category")

    def fundsAnnualPerformance(self):
        """
        Returns:
            dict funds annual performance
        """
        return self.AnnualPerformance('funds')


    def categoryAnnualPerformance(self):
        """
        Returns:
            dict category annual performance
        """
        return self.AnnualPerformance('category')


    def indexAnnualPerformance(self):
        """
        Returns:
            dict index annual performance
        """
        return self.AnnualPerformance('index')

    def fundsAnnualRank(self):
        """
        Returns:
            dict funds annual rank
        """
        return self.AnnualPerformance('rank')

    def AnnualPerformance(self, cat):
        """
        Args:
            cat (str) : possible values are category, funds, index, rank    
        Returns:
            dict annual performance or rank

        Examples:
            >>> MS.AnnualPerformance("category")
            >>> MS.AnnualPerformance("funds")
            >>> MS.AnnualPerformance("index")
            >>> MS.AnnualPerformance("rank")
        
        """

        cat_row = {'funds' : 0,'category' : 1, 'index' : 2, 'rank' : 3}
        if cat not in cat_row:
            raise ValueError(f"cat parameter must take one of the following value : { ', '.join(cat_row.keys())}")

        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=1"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        #label are dates
        regex = re.compile('.*heading number')
        label_list = soup.find(id='returnsCalenderYearDiv').find_all('td', {"class": regex})
        #funds performance, category performance, index performance, rank in category
        regex = re.compile('.*value number')
        #values
        value_list = soup.find(id='returnsCalenderYearDiv').find_all('td', {"class": regex})

        regex = re.compile('-|\/')
        #first col is nothing
        for i in range(1, len(label_list)):
            label = label_list[i].text
            #if today

            if regex.search(label):
                label = 'current'
            #add category to label
            if label:
                
                result[f'{cat}_annual_performance_{label}'] = value_list[i+(cat_row[cat])*(len(label_list)-1)-1].text

        return result

    def fundsCumulativePerformance(self):
        """
        Returns:
            dict funds cumulative performance
        """
        return self.CumulativePerformance('funds')

    def categoryCumulativePerformance(self):
        """
        Returns:
            dict category cumulative performance
        """
        
        return self.CumulativePerformance('category')

    def indexCumulativePerformance(self):
        """
        Returns:
            dict index cumulative performance
        """
        
        return self.CumulativePerformance('index')

    def CumulativePerformance(self, cat):
        """
        Args:
            cat (str) : possible values are category, funds, index   
        Returns:
            dict cumulative performance

        Examples:
            >>> MS.CumulativePerformance("category")
            >>> MS.CumulativePerformance("funds")
            >>> MS.CumulativePerformance("index")
        
        """

        cat_row = {'funds' : 2,'category' : 3, 'index' : 4}
        if cat not in cat_row:
            raise ValueError(f"cat parameter must take one of the following value : { ', '.join(cat_row.keys())}")
        result = {}

        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=1"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cumulative_performance_date = soup.find(id='returnsTrailingDiv').find('td', {"class": "titleBarNote"}).text
        result['cumulative_performance_date'] = cumulative_performance_date 
        #days
        regex = re.compile('.*label')
        label_list = soup.find(id='returnsTrailingDiv').find_all('td', {"class": regex})

        #cumulative performance cat
        regex = re.compile(f'.*col{str(cat_row[cat])} value number')
        value_list = soup.find(id='returnsTrailingDiv').find_all('td', {"class": regex})
        #loop on label
        for i in range(0, len(label_list)):
            #label
            label = label_list[i].text
            #perf funds
            result[f'{cat}_cumulative_performance_{label}'] = re.sub('[^0-9,-\.]','',value_list[i].text)
        return result


    def fundsQuarterlyPerformance(self):
        """
        Returns:
            dict funds quarterly performance
        """
        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=1"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        quarterly_performance_date = soup.find(id='returnsTrailingDiv').find('td', {"class": "titleBarNote"}).text
        result['quarterly_performance_date'] = quarterly_performance_date 

        #quarter label
        regex = re.compile('.*heading number')
        quarter_list = soup.find(id='returnsQuarterlyDiv').find_all('td', {"class": regex})
        #year label
        regex = re.compile('.*label')
        year_list =soup.find(id='returnsQuarterlyDiv').find_all('td', {"class": regex})
        #1st Quarter 
        regex = re.compile('.*col2 value number')
        quarter_1_list = soup.find(id='returnsQuarterlyDiv').find_all('td', {"class": regex})
        #2nd Quarter
        regex = re.compile('.*col3 value number')
        quarter_2_list = soup.find(id='returnsQuarterlyDiv').find_all('td', {"class": regex})
        #3rd Quarter
        regex = re.compile('.*col4 value number')
        quarter_3_list = soup.find(id='returnsQuarterlyDiv').find_all('td', {"class": regex})
        #4th Quarter
        regex = re.compile('.*col5 value number')
        quarter_4_list = soup.find(id='returnsQuarterlyDiv').find_all('td', {"class": regex})
        #loop on year
        for i in range(0, len(year_list)):
            label = 'performance_%s_' % (year_list[i].text)
            result[label + 'quarter_1'] = quarter_1_list[i].text
            result[label + 'quarter_2'] = quarter_2_list[i].text
            result[label + 'quarter_3'] = quarter_3_list[i].text
            result[label + 'quarter_4'] = quarter_4_list[i].text
        return result

    def contact(self):
        """
        Returns:
            dict funds contact like phone number, asset manager
        """
        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        #page 4 - info about found
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=4"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        #label
        label_list = soup.find(id='managementManagementDiv').find_all('td', {"class": "col1 label"})
        #value
        value_list = soup.find(id='managementManagementDiv').find_all('td', {"class": "col2 value number"})
        for i in range(0, len(value_list)):
            label = label_list[i].text
            
            result[label] = value_list[i].text

        return result

    def fees(self):
        """
        Returns:
            dict fees
        """
        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=5"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find(id='managementFeesDiv') == None:
            return {}
        #label
        label_list =soup.find(id='managementFeesDiv').find_all('td', {"class": "label"})
        #value
        value_list = soup.find(id='managementFeesDiv').find_all('td', {"class": "value number"}) + soup.find(id='managementFeesDiv').find_all('td', {"class": "value number jdpa"})
        for i in range(0, len(value_list)):
            label = label_list[i].text
            result[label] = re.sub('(\\n +)|(\\n)','',value_list[i].text)

        return result


    def searchField(self,pattern = ''):
        """
        Args:
        pattern (str) : text contained in the field

        Returns:
            list of fields possible for the method dataPoint

        Example:
            >>> MS.searchField('fees')
            >>> MS.searchField('return')

        """
        
        regex = re.compile(f'(?i){pattern}')
        filtered_list = list(filter(lambda field : regex.search(field),FIELDS))
        print(f"possible fields for DataPoint can be : {', '.join(filtered_list)} ")
        return filtered_list

    

    def dataPoint(self, field, currency ='EUR' ):
        """
        Args:
        field (str or list) : field to find
        currency (str) : currency in 3 letters

        Returns:
            dict funds infos

        Example:
            >>> MS.dataPoint(['largestSector', 'Name', 'ongoingCharge'])
            >>> MS.dataPoint('SharpeM36')

        """
        return search_funds(self.code, field,self.country,10,currency)
        


    
    

    

    

