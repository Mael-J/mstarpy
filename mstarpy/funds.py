import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from .utils import SITE, APIKEY, random_user_agent
from .search import search_funds, token_chart
from .error import no_site_error, not_200_response




class Funds:
    """
    Main class to access data about funds and etf
    Args:
        term (str): text to find a fund can be a name, part of a name or the isin of the funds
        country (str) : text for code ISO 3166-1 alpha-2 of country, should be '' for etf
        pageSize (int): number of funds to return
        itemRange (int) : index of funds to return (must be inferior to PageSize)

    Examples:
        >>> Funds('0P0000712R', "ca", 9, 0)
        >>> Funds('bond', "uk", 25, 2)

    Raises:
        TypeError: raised whenever the parameter type is not the type expected
        ValueError : raised whenever the parameter is not valid or no fund found

    """

    def __init__(self, term = None, country: str = "", pageSize : int =1, itemRange: int = 0):
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

        if country:
            self.site = SITE[country.lower()]["site"]
        else:
            self.site =""
        

        self.country = country
        
        code_list = search_funds(term,['fundShareClassId','SecId','TenforeId','LegalName'], country, pageSize)

        self.asset_type = 'fund'

        if code_list:
            if itemRange < len(code_list):
                self.code = code_list[itemRange]["fundShareClassId"]
                self.name = code_list[itemRange]["LegalName"]
                if "TenforeId" in code_list[itemRange]:
                    tenforeId = code_list[itemRange]["TenforeId"]
                    if  "126.1." in tenforeId:
                        self.asset_type = 'etf'
                    regex = re.compile("52.8.|126.1.")
                    self.isin = regex.sub('',tenforeId)                   
                else:
                    self.isin = None
                    
            else:
                raise ValueError(f'Found only {len(code_list)} fund with the term {term}. The paramater itemRange must maximum equal to {len(code_list)-1}')
        else:
            if country:
                raise ValueError(f'0 fund found with the term {term} and country {country}')
            else:
                raise ValueError(f'0 fund found with the term {term}')
        

    def allocationMap(self):
        """    
        This function retrieves the asset allocation of the funds, index and category.

        Returns:
            dict with allocation map

        Examples:
            >>> Funds("myria", "fr").allocationMap()

            {'assetType': 'EQUITY', 'portfolioDate': '2022-08-31T05:00:00.000', 'portfolioDateCategory': '2022-08-31T05:00:00.000', 'portfolioDateIndex': '2022-08-31T05:00:00.000', 'portfolioDateGlobal': '2022-08-31T05:00:00.000', 'portfolioDateCategoryGlobal': '2022-08-31T05:00:00.000', 'portfolioDateIndexGlobal': '2022-08-31T05:00:00.000', 'fundName': 'Myria Actions Durables Europe', 'categoryName': 'Europe Large-Cap Blend Equity', 
            'indexName': 'Morningstar Eur TME GR EUR', 'allocationMap': {'AssetAllocCash': {'netAllocation': '1.59410', 'shortAllocation': '1.43321', 'longAllocation': '3.02731', 'longAllocationIndex': '0.00309', 'longAllocationCategory': '4.74916', 'targetAllocation': None}, 'AssetAllocNotClassified': {'netAllocation': '0.0', 'shortAllocation': '0.0', 'longAllocation': '0.0', 'longAllocationIndex': '0.0234', 'longAllocationCategory': '0.00175', 'targetAllocation': None}, 'AssetAllocNonUSEquity': {'netAllocation': '97.26880', 'shortAllocation': '0.00000', 'longAllocation': '97.26880', 'longAllocationIndex': '98.41604', 'longAllocationCategory': '92.60715', 'targetAllocation': None}, 
            'AssetAllocOther': {'netAllocation': '0.00000', 'shortAllocation': '0.00000', 'longAllocation': '0.00000', 'longAllocationIndex': '0.08330', 'longAllocationCategory': '4.14142', 'targetAllocation': None}, 'AssetAllocUSEquity': {'netAllocation': '1.13710', 'shortAllocation': '0.00000', 'longAllocation': '1.13710', 'longAllocationIndex': '1.47416', 'longAllocationCategory': '1.75082', 'targetAllocation': None}, 'AssetAllocBond': {'netAllocation': '0.00000', 'shortAllocation': '0.00000', 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '0.17067', 'targetAllocation': None}},
            'countryCode': 'FRA', 'securityType': None, 'dualViewData': {'performanceId': '0P00019Q8D', 'marketValueStockLong': '98.44704', 'marketValueStockShort': None, 'marketValueStockNet': '98.44704', 'marketValueBondLong': None, 'marketValueBondShort': None, 'marketValueBondNet': None, 'marketValueCashLong': '1.92656', 'marketValueCashShort': '-0.36399', 'marketValueCashNet': '1.56257', 'marketValueDerivativeLong': None, 'marketValueDerivativeShort': '-0.00961', 'marketValueDerivativeNet': '-0.00961', 'marketValueFundLong': None, 'marketValueFundShort': None, 'marketValueFundNet': None, 'marketValueOtherLong': None, 'marketValueOtherShort': None, 'marketValueOtherNet': None, 'economicExposureCurrencyLong': '2.06232', 'economicExposureCurrencyShort': '-0.36399', 'economicExposureCurrencyNet': '1.69833', 'economicExposureFixedIncomeLong': None, 'economicExposureFixedIncomeShort': None, 'economicExposureFixedIncomeNet': None, 'economicExposureEquityLong': '98.44704', 'economicExposureEquityShort': None, 'economicExposureEquityNet': '98.44704', 'economicExposureOtherLong': None, 'economicExposureOtherShort': None, 'economicExposureOtherNet': None, 'marketValueAsOf': '2022-08-31T05:00:00.000', 'economicExposureAsOf': '2022-08-31T05:00:00.000', 'dualViewAsOf': '2022-08-31T05:00:00.000', 'marketValueTotal': {'longVal': 100.3736, 'shortVal': -0.3736, 'netVal': 100.0}, 'economicExposureTotal': {'longVal': 100.50936, 'shortVal': -0.36399, 'netVal': 100.14537}}, 'targetDate': None, 'hasRegionalAssetAlloc': False, 'globalAllocationMap': {'assetAllocPreferred': {'netAllocation': '0.00000', 'shortAllocation': '0.00000', 'longAllocation': '0.00000', 'longAllocationIndex': '0.02340', 'longAllocationCategory': '0.00007', 'targetAllocation': None}, 'assetAllocOther': {'netAllocation': '0.00000', 'shortAllocation': '0.00000', 'longAllocation': '0.00000', 'longAllocationIndex': '0.08330', 'longAllocationCategory': '4.14142', 'targetAllocation': None}, 'assetAllocEquity': {'netAllocation': '98.40590', 'shortAllocation': '0.00000', 'longAllocation': '98.40590', 'longAllocationIndex': '99.89020', 'longAllocationCategory': '94.35797', 'targetAllocation': None}, 'assetAllocCash': {'netAllocation': '1.59410', 'shortAllocation': '1.43321', 'longAllocation': '3.02731', 
            'longAllocationIndex': '0.00309', 'longAllocationCategory': '4.74916', 'targetAllocation': None}, 'assetAllocConvertible': {'netAllocation': '0.00000', 'shortAllocation': '0.00000', 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '0.00168', 'targetAllocation': None}, 'assetAllocFixedIncome': {'netAllocation': '0.00000', 'shortAllocation': '0.00000', 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '0.17067', 'targetAllocation': None}}}

        """
        return self.GetFundsData("process/asset/v2")

    def allocationWeighting(self):
        """
        This function retrieves the Growth/Blend/Value and market capitalizaton allocation size of the funds.

        Returns:
            dict with allocation

        Examples:
            >>> Funds("myria", "fr").allocationWeighting()

            {'portfolioDate': '2022-08-31T05:00:00.000', 'masterPortfolioId': '2852268', 'largeValue': '25.98000', 'largeBlend': '34.66300', 'largeGrowth': '33.87000', 
            'middleValue': '0.83100', 'middleBlend': '3.19300', 'middleGrowth': '1.35200', 
            'smallValue': '0.05000', 'smallBlend': '0.06100', 'smallGrowth': '0.00000'}
        
        """
        return self.GetFundsData("process/weighting")

    def analystRating(self):
        """
        This function retrieves the rating of the funds

        Returns:
            list of dict with ratings

            >>> Funds("RMAGX", "us").analystRating()

            [{'rating': '7', 'percent': 0.3039297897, 'noPremiumChinaFund': False}, {'rating': '6', 'percent': 0.5495932499, 'noPremiumChinaFund': False}, 
            {'rating': '5', 'percent': 0.0959166043, 'noPremiumChinaFund': False}, {'rating': '4', 'percent': 0.0381999262, 'noPremiumChinaFund': False}, 
            {'rating': '3', 'percent': 0.0002092845, 'noPremiumChinaFund': False}, {'rating': '2', 'percent': 0.0, 'noPremiumChinaFund': False}, 
            {'rating': '1', 'percent': 0.0, 'noPremiumChinaFund': False}, {'rating': '0', 'percent': 0.0121511453, 'noPremiumChinaFund': False}]

        """
        

        return self.GetFundsData("parent/analystRating")

    def analystRatingTopFunds(self):
        """
        This function retrieves the rating Top funds

        Returns:
            dict with ratings

            >>> Funds("RMAGX", "us").analystRatingTopFunds()
            
            {'userType': 'Free', 'analystRatingFundList': [{'rating': '7', 'calendarYearFlow': -1747646088.0, 'netAsset': 69496484161.0, 'epUsedFor3YearReturn': 
            '0', 'trailing3YearReturn': 10.31222, 'trailing3YearReturnRank': 66.0, 'fundShareClassId': 'FOUSA00FUP', 'name': '_PO_', 'returnEndDate': '2022-08-31T05:00:00.000', 'fundId': 'FSUSA002RR', 'secId': 'FOUSA00FUP', 'securityType': 'FO'}, {'rating': '7', 'calendarYearFlow': -35131408.0, 'netAsset': 65421718187.0, 'epUsedFor3YearReturn': '0', 'trailing3YearReturn': 2.72222, 'trailing3YearReturnRank': 55.0, 'fundShareClassId': 'F000002P1T', 'name': 
            '_PO_', 'returnEndDate': '2022-08-31T05:00:00.000', 'fundId': 'FSUSA000PI', 'secId': 'F000002P1T', 'securityType': 'FO'}, {'rating': '7', 'calendarYearFlow': 802630652.0, 'netAsset': 35266725344.0, 'epUsedFor3YearReturn': '0', 'trailing3YearReturn': 9.35787, 'trailing3YearReturnRank': 57.0, 'fundShareClassId': 'FOUSA00B8C', 'name': '_PO_', 'returnEndDate': '2022-08-31T05:00:00.000', 'fundId': 'FSUSA0003P', 'secId': 'FOUSA00B8C', 'securityType': 'FO'}, {'rating': '7', 'calendarYearFlow': -2041927486.0, 'netAsset': 31659783482.0, 'epUsedFor3YearReturn': '0', 'trailing3YearReturn': 7.11897, 'trailing3YearReturnRank': 80.0, 'fundShareClassId': 'FOUSA00B49', 'name': '_PO_', 'returnEndDate': '2022-08-31T05:00:00.000', 'fundId': 'FSUSA0001Y', 'secId': 'FOUSA00B49', 'securityType': 'FO'}, {'rating': '7', 'calendarYearFlow': 362724000.0, 'netAsset': 24686749469.0, 'epUsedFor3YearReturn': '0', 'trailing3YearReturn': 9.70209, 'trailing3YearReturnRank': 13.0, 'fundShareClassId': 'F000002PIY', 'name': '_PO_', 'returnEndDate': '2022-08-31T05:00:00.000', 'fundId': 'FSUSA001SL', 'secId': 'F000002PIY', 'securityType': 'FO'}], 'footerFundFlowDate': '2022-08-31T05:00:00.000', 'footerReturnDate': '2022-08-31T05:00:00.000', 'currency': 'USD', 'noPremiumChinaFund': False}

        """
        
        return self.GetFundsData("parent/analystRating/topfunds")


    def analystRatingTopFundsUpDown(self):
        """
        This function retrieves the rating funds Up Down

        Returns:
            dict with ratings

            >>> Funds("RMAGX", "us").analystRatingTopFundsUpDown()
            
            {'topAnalystRatingUpDownList': [{'fundName': '_PO_', 'mstarCurrRating': '2', 'mstarPrevRating': None, 'mstarCurrRatingValue': 'Neutral', 'mstarPrevRatingValue': None, 'currRatingDate': '2022-06-16T05:00:00.000', 'prevRatingDate': None, 'netAsset': 9270918076.0, 'fundId': 'FS00009QUT', 'securityType': 'FO', 'secId': 'F00000OSYR'}, 
            {'fundName': '_PO_', 'mstarCurrRating': '5', 'mstarPrevRating': '4', 'mstarCurrRatingValue': 'Gold', 'mstarPrevRatingValue': 'Silver', 'currRatingDate': '2022-07-29T05:00:00.000', 'prevRatingDate': '2021-08-04T05:00:00.000', 'netAsset': 65421718187.0, 'fundId': 'FSUSA000PI', 'securityType': 'FO', 'secId': 'F000002P1T'}, 
            {'fundName': '_PO_', 'mstarCurrRating': '4', 'mstarPrevRating': '3', 'mstarCurrRatingValue': 'Silver', 'mstarPrevRatingValue': 'Bronze', 'currRatingDate': '2022-08-01T05:00:00.000', 'prevRatingDate': '2021-08-10T05:00:00.000', 'netAsset': 13056877278.0, 'fundId': 'FSUSA001SK', 'securityType': 'FO', 'secId': 'FOUSA00E5P'}, 
            {'fundName': '_PO_', 'mstarCurrRating': '5', 'mstarPrevRating': '4', 'mstarCurrRatingValue': 'Gold', 'mstarPrevRatingValue': 'Silver', 'currRatingDate': '2022-08-10T05:00:00.000', 'prevRatingDate': '2020-09-09T05:00:00.000', 'netAsset': 3914319698.0, 'fundId': 'FSUSA09086', 'securityType': 'FO', 'secId': 'FOUSA06YL3'}, 
            {'fundName': '_PO_', 'mstarCurrRating': '3', 'mstarPrevRating': None, 'mstarCurrRatingValue': 'Bronze', 'mstarPrevRatingValue': None, 'currRatingDate': '2022-08-12T05:00:00.000', 'prevRatingDate': None, 'netAsset': 5862800318.0, 'fundId': 'FS0000C5U3', 'securityType': 'FO', 'secId': 'F00000WFZG'}], 'userType': 'Free', 'currency': 'USD', 'securityType': 'FO', 'name': 'American Funds Mortgage R6', 'secId': 'F00000JNX4', 'noPremiumChinaFund': False}
    
        """

        return self.GetFundsData("parent/analystRating/topfundsUpDown")


    def AnnualPerformance(self, cat):
        """
        This function retrieves the annual performance of the funds, index, category or the annual rank of the funds.

        Args:
            cat (str) : possible values are category, funds, index, rank    
        Returns:
            dict annual performance or rank

        Raises:
            ValueError : raised whenever parameter cat is not category, funds, index, or rank

        Examples:
            >>> Funds("myria", "fr").AnnualPerformance("category")
            >>> Funds("myria", "fr").AnnualPerformance("funds")
            >>> Funds("myria", "fr").AnnualPerformance("index")
            >>> Funds("myria", "fr").AnnualPerformance("rank")

            {'category_annual_performance_2016': '-4,29', 'category_annual_performance_2017': '1,11', 'category_annual_performance_2018': '-2,75', 'category_annual_performance_2019': '-2,32', 'category_annual_performance_2020': '-8,64', 'category_annual_performance_2021': '-2,39', 'category_annual_performance_current': '0,37'}
            {'funds_annual_performance_2016': '-4,63', 'funds_annual_performance_2017': '11,29', 'funds_annual_performance_2018': '-15,56', 'funds_annual_performance_2019': '22,27', 'funds_annual_performance_2020': '-9,89', 'funds_annual_performance_2021': '20,55', 'funds_annual_performance_current': '-14,25'}
            {'index_annual_performance_2016': '-7,21', 'index_annual_performance_2017': '1,05', 'index_annual_performance_2018': '-4,99', 'index_annual_performance_2019': '-3,78', 'index_annual_performance_2020': '-6,57', 'index_annual_performance_2021': '-4,58', 'index_annual_performance_current': '-2,41'}
            {'rank_annual_performance_2016': '88', 'rank_annual_performance_2017': '29', 'rank_annual_performance_2018': '80', 'rank_annual_performance_2019': '76', 'rank_annual_performance_2020': '96', 'rank_annual_performance_2021': '77', 'rank_annual_performance_current': '52'}
        
        """
        no_site_error(self.code,self.name,self.country,self.site)

        cat_row = {'funds' : 0,'category' : 1, 'index' : 2, 'rank' : 3}
        if cat not in cat_row:
            raise ValueError(f"cat parameter must take one of the following value : { ', '.join(cat_row.keys())}")

        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=1"
        
        response = requests.get(url, headers=headers)
        not_200_response(url,response)
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

    def benchmark(self):
        """
        This function retrieves the benchmark name of the funds.

        Returns:
            str benchmark name

        Examples:
            >>> Funds("myria", "fr").benchmark()

            STOXX Europe Ex UK Large NR EUR

        """
        return self.referenceIndex("benchmark")

    def carbonMetrics(self):
        """
        This function retrieves the carbon metrics of the funds.

        Returns:
            dict with carbon metrics

        Examples:
            >>> Funds("myria", "fr").carbonMetrics()

            {'carbonPortfolioCoveragePct': '95.90', 'carbonRiskScore': None, 
            'carbonRiskScoreCategoryAverage': '6.95', 'carbonRiskScoreCategoryHigh': '16.99', 
            'carbonRiskScoreCategoryLow': '2.42', 'carbonRiskScoreCategoryAverageDate': '2022-06-30T05:00:00.000', 
            'carbonRiskScoreCategoryRankPct': None, 'carbonRiskScoreDate': '2022-06-30T05:00:00.000', 
            'categoryDate': '2022-06-30T05:00:00.000', 'categoryName': 'Europe Large-Cap Blend Equity', 
            'fossilFuelInvolvementPctCategoryAverage': '7.46', 'fossilFuelInvolvementPct': None, 
            'fossilFuelInvolvementPctCategoryHigh': '27.68', 'fossilFuelInvolvementPctCategoryLow': '0.00', 
            'isLowCarbon': None}
            
        """

        return self.GetFundsData("esg/carbonMetrics")

    def category(self):
        """
        This function retrieves the category name of the funds.

        Returns:
            str category name

        Examples:
            >>> Funds("myria", "fr").category()

            MSCI Europe NR EUR

        """
        return self.referenceIndex("category")

    def categoryAnnualPerformance(self):
        """
        This function retrieves the annual performance of the category.
  
        Returns:
            dict annual performance of the category


        Examples:
            >>> Funds("myria", "fr").categoryAnnualPerformance()

            {'category_annual_performance_2016': '-4,29', 'category_annual_performance_2017': '1,11', 'category_annual_performance_2018': '-2,75', 'category_annual_performance_2019': '-2,32', 'category_annual_performance_2020': '-8,64', 'category_annual_performance_2021': '-2,39', 'category_annual_performance_current': '0,37'}

        """
        return self.AnnualPerformance('category')

    def categoryCumulativePerformance(self):
        """
        This function retrieves the cumulative performance of the category.
  
        Returns:
            dict cumulative performance of the category

        Examples:
            >>> Funds("myria", "fr").categoryCumulativePerformance()

            {'cumulative_performance_date': '26/09/2022', 'category_cumulative_performance_1 jour': '-0,46', 'category_cumulative_performance_1 semaine': '-0,68', 'category_cumulative_performance_1 mois': '2,04', 'category_cumulative_performance_3 mois': '0,77', 
            'category_cumulative_performance_6 mois': '2,03', "category_cumulative_performance_Début d'année": '1,51', 'category_cumulative_performance_1 an': '0,56', 'category_cumulative_performance_3 ans (annualisée)': '-4,07', 
            'category_cumulative_performance_5 ans (annualisée)': '-3,35', 'category_cumulative_performance_10 ans (annualisée)': '-'}
        
        """
        
        return self.CumulativePerformance('category')

    def contact(self):
        """
        This function retrieves information about the asset manager.
  
        Returns:
            dict contact

        Examples:
            >>> Funds("myria", "fr").contact()

            {'Société de gestion': 'Myria Asset Management', 'Téléphone': '-', 'Site Internet': 'www.myria-am.com', 'Adresse': '32, avenue d'Iéna', '\xa0': 'France', 
            'PEA': 'oui', 'PEAPME': 'non', 'Domicile': 'France', 'Structure légale': 'FCP', 'UCITS': 'oui'}
        
        """
        no_site_error(self.code,self.name,self.country,self.site)
        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        #page 4 - info about found
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=4"
        response = requests.get(url, headers=headers)
        not_200_response(url,response)
        soup = BeautifulSoup(response.text, 'html.parser')
        #label
        label_list = soup.find(id='managementManagementDiv').find_all('td', {"class": "col1 label"})
        #value
        value_list = soup.find(id='managementManagementDiv').find_all('td', {"class": "col2 value number"})
        for i in range(0, len(value_list)):
            label = label_list[i].text
            
            result[label] = value_list[i].text

        return result

    def costIllustration(self):
        """
        This function retrieves the cost of the funds.
  
        Returns:
            dict cost of funds

        Examples:
            >>> Funds("FOUSA00E5P", "us").costIllustration()

            {'prospectusDate': '2022-02-01T06:00:00.000', 'expectedReturn': 5.0, 'initial': 10000.0, 'mer': None, 'priceTemplate': 'USA_OE', 'baseCurrencyId': 'USD', 'costItems': [{'year': 1, 'endNetAsset': 10469.64417789839, 'purchase': 575.0, 'ongoing': 71.2309942498, 'redemption': 0.0, 'total': 646.2309942498, 'purchasePer': 0.0549206821, 'ongoingPer': 0.0068035736, 'redemptionPer': 0.0, 'totalPer': 0.0617242557}, {'year': 5, 'endNetAsset': 12555.319702494042, 'purchase': 575.0, 'ongoing': 387.5656754635, 'redemption': 0.0, 'total': 962.5656754635, 'purchasePer': 0.0457973205, 'ongoingPer': 0.0308686425, 'redemptionPer': 0.0, 'totalPer': 0.076665963}, {'year': 10, 'endNetAsset': 15698.364028376052, 'purchase': 575.0, 'ongoing': 864.2716218792, 
            'redemption': 0.0, 'total': 1439.2716218792, 'purchasePer': 0.0366280205, 'ongoingPer': 0.0550548847, 'redemptionPer': 0.0, 'totalPer': 0.0916829053}]}
        
        """
        return self.GetFundsData("price/costIllustration")

    def couponRange(self):
        """
        This function retrieves the coupon of the funds, index and category.
  
        Returns:
            dict coupon

        Examples:
            >>> Funds("rmagx", "us").couponRange()

            {'fundCouponRange': {'portfolioDate': '2022-06-30T05:00:00.000', 'name': 'American Funds Mortgage R6', 'coupon0': 5.72643, 'coupon0To2': 25.8586, 'coupon2To4': 40.83286, 'coupon4To6': 26.16087, 'coupon6To8': 0.00773, 'coupon8To10': 0.0, 'couponMoreThan10': 0.0}, 
            'categoryCouponRange': {'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Intermediate Government', 'coupon0': 0.17705, 'coupon0To2': 56.95988, 'coupon2To4': 35.27511, 'coupon4To6': 10.72757, 'coupon6To8': 0.41473, 'coupon8To10': 0.00038, 'couponMoreThan10': -0.29354}, 
            'benchmarkCouponRange': None, 'morningstarIndexCouponRange': {'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Morningstar US Trsy Bd TR USD', 'coupon0': 0.0, 'coupon0To2': 59.67448, 'coupon2To4': 39.12677, 'coupon4To6': 1.19873, 'coupon6To8': 0.0, 'coupon8To10': 0.0, 'couponMoreThan10': 0.0}}
        
        """
        return self.GetFundsData("process/couponRange")


    def creditQuality(self):
        """
        This function retrieves the credit notation of the funds, index and category.
  
        Returns:
            dict credit notation

        Examples:
            >>> Funds("rmagx", "us").creditQuality()

            {'fundName': 'American Funds Mortgage R6', 'categoryName': 'Intermediate Government', 'indexName': 'Morningstar US Trsy Bd TR USD', 
            'fund': {'creditQualityDate': '2022-06-30T05:00:00.000', 'creditQualityAAA': '97.85000', 'creditQualityAA': '0.83000', 'creditQualityA': '0.00000', 'creditQualityBBB': '0.00000', 'creditQualityBB': '0.00000', 'creditQualityB': '0.00000', 'creditQualityBelowB': '0.00000', 'creditQualityNotRated': '1.32000'}, 
            'category': {'creditQualityDate': '2022-06-30T05:00:00.000', 'creditQualityAAA': '94.34350', 'creditQualityAA': '2.62926', 'creditQualityA': '1.38331', 'creditQualityBBB': '0.50800', 'creditQualityBB': '0.13555', 'creditQualityB': '0.11274', 'creditQualityBelowB': '0.04023', 'creditQualityNotRated': '0.84709'}, 
            'index': {'creditQualityDate': None, 'creditQualityAAA': None, 'creditQualityAA': None, 'creditQualityA': None, 'creditQualityBBB': None, 'creditQualityBB': None, 'creditQualityB': None, 'creditQualityBelowB': None, 'creditQualityNotRated': None}}
        
        """
        return self.GetFundsData("portfolio/creditQuality")

    def dataPoint(self, field, currency ='EUR'):
        """
        This function retrieves infos about funds such as name, performance, risk metrics...

        Args:
        field (str or list) : field to find
        currency (str) : currency in 3 letters

        Returns:
            list of dict funds infos

        Example:
            >>> Funds("myria", "fr").dataPoint(['largestSector', 'Name', 'ongoingCharge'])
            >>> Funds("myria", "fr").dataPoint('SharpeM36')
            [{'largestSector': 'SB_Healthcare', 'Name': 'Myria Actions Durables Europe', 'ongoingCharge': 1.08}]
            [{'SharpeM36': 0.11}]

        """
        return search_funds(self.code, field,self.country,10,currency)

    def distribution(self, period = "annual"):
        """
        This function retrieves the coupon distributed by the funds.

        Args:
            period (str) : annual or latest
        
        Raises:
            ValueError whenever the pariod parameter is not annual or latest

        Returns:
            dict distribution of coupon

        Example:
            >>> Funds("rmagx", "us").distribution("annual")
            
            {'distribution': [{'distributionDate': '2022-08-31T05:00:00.000', 'distributionNav': 9.34, 'income': 0.12042030000000001, 'capGainShortTerm': 0.0, 'capGainLongTerm': 0.0, 'returnOfCapital': 0.0, 'total': 0.12042030000000001, 'interestIncome': None, 'foreignIncome': None, 'capitalGains': None, 'canadianDividend': None}, {'distributionDate': '2021-12-31T06:00:00.000', 'distributionNav': 10.18, 'income': 0.0746213, 'capGainShortTerm': 0.0, 'capGainLongTerm': 0.0, 'returnOfCapital': 0.0, 'total': 0.0746213, 'interestIncome': None, 'foreignIncome': None, 'capitalGains': None, 'canadianDividend': None}, {'distributionDate': '2020-12-31T06:00:00.000', 'distributionNav': 10.28, 'income': 0.14304508, 'capGainShortTerm': 0.239, 'capGainLongTerm': 0.1107, 'returnOfCapital': 0.0, 'total': 0.49274507999999995, 'interestIncome': None, 'foreignIncome': None, 'capitalGains': None, 'canadianDividend': None}, {'distributionDate': '2019-12-31T06:00:00.000', 'distributionNav': 10.07, 'income': 0.25909676000000004, 'capGainShortTerm': 0.0554, 'capGainLongTerm': 0.0331, 'returnOfCapital': 0.0, 'total': 0.34759675999999995, 'interestIncome': None, 'foreignIncome': None, 'capitalGains': None, 'canadianDividend': None}, {'distributionDate': '2018-12-31T06:00:00.000', 'distributionNav': 9.9, 'income': 0.21256776000000005, 'capGainShortTerm': 0.0, 'capGainLongTerm': 0.0, 'returnOfCapital': 0.0, 'total': 0.21256776000000005, 'interestIncome': None, 'foreignIncome': None, 'capitalGains': None, 'canadianDividend': None}], 'baseCurrencyId': 'USD', 'template': 'OE_USA_FIXEDINCOME'}

        """


        period_choice = ["annual", "latest"]
        if period not in period_choice:
            raise ValueError(f'period parameter can only take one of the values: {", ".join(period_choice)}')

        return self.GetFundsData(f"distribution/{period}")



    def CumulativePerformance(self, cat):
        """
        This function retrieves the cumulative performance of funds, index and category.

        Args:
            cat (str) : possible values are category, funds, index

        Returns:
            dict cumulative performance

        Examples:
            >>> Funds("myria", "fr").CumulativePerformance("funds")
            >>> Funds("myria", "fr").CumulativePerformance("index")
            >>> Funds("myria", "fr").CumulativePerformance("category")

            {'cumulative_performance_date': '26/09/2022', 'funds_cumulative_performance_1 jour': '-0,49', 'funds_cumulative_performance_1 semaine': '-4,31', 'funds_cumulative_performance_1 mois': '-7,17', 'funds_cumulative_performance_3 mois': '-5,18', 'funds_cumulative_performance_6 mois': '-11,31', "funds_cumulative_performance_Début d'année": '-18,53', 'funds_cumulative_performance_1 an': '-15,41', 'funds_cumulative_performance_3 ans (annualisée)': '-2,73', 'funds_cumulative_performance_5 ans (annualisée)': '-1,74', 'funds_cumulative_performance_10 ans (annualisée)': '-'}
            {'cumulative_performance_date': '26/09/2022', 'index_cumulative_performance_1 jour': '-0,42', 'index_cumulative_performance_1 semaine': '-0,71', 'index_cumulative_performance_1 mois': '1,49', 'index_cumulative_performance_3 mois': '0,55', 'index_cumulative_performance_6 mois': '0,89', "index_cumulative_performance_Début d'année": '-1,22', 'index_cumulative_performance_1 an': '-3,16', 'index_cumulative_performance_3 ans (annualisée)': '-4,73', 'index_cumulative_performance_5 ans (annualisée)': '-4,43', 'index_cumulative_performance_10 ans (annualisée)': '-'}
            {'cumulative_performance_date': '26/09/2022', 'category_cumulative_performance_1 jour': '-0,46', 'category_cumulative_performance_1 semaine': '-0,68', 'category_cumulative_performance_1 mois': '2,04', 'category_cumulative_performance_3 mois': '0,77', 'category_cumulative_performance_6 mois': '2,03', "category_cumulative_performance_Début d'année": '1,51', 'category_cumulative_performance_1 an': '0,56', 'category_cumulative_performance_3 ans (annualisée)': '-4,07', 'category_cumulative_performance_5 ans (annualisée)': '-3,35', 'category_cumulative_performance_10 ans (annualisée)': '-'}
        
        """
        no_site_error(self.code,self.name,self.country,self.site)
        cat_row = {'funds' : 2,'category' : 3, 'index' : 4}
        if cat not in cat_row:
            raise ValueError(f"cat parameter must take one of the following value : { ', '.join(cat_row.keys())}")
        result = {}

        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=1"
        
        response = requests.get(url, headers=headers)
        not_200_response(url,response)
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

    def equityStyle(self):
        """
        This function retrieves the equity style of the funds and category.

        Returns:
            dict equity style

        Examples:
            >>> Funds("myria", "fr").equityStyle()

            {'portfolioDate': '2022-08-31T05:00:00.000', 'assetType': 'EQUITY', 'fund': {'prospectiveEarningsYield': 12.03844, 'prospectiveBookValueYield': 1.8135, 'prospectiveRevenueYield': 1.21333, 'prospectiveCashFlowYield': 6.76284, 'prospectiveDividendYield': 4.69964, 'forecasted5YearEarningsGrowth': 9.87483, 'forecastedEarningsGrowth': 24.99911, 'forecastedBookValueGrowth': 4.39037, 'forecastedRevenueGrowth': 0.88596, 'forecastedCashFlowGrowth': 18.98939, 'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Myria Actions Durables Europe', 'secId': 'F00000YIJ0', 'currencyId': 'EUR'}, 'categoryAverage': {'prospectiveEarningsYield': 11.96095, 'prospectiveBookValueYield': 1.73223, 'prospectiveRevenueYield': 1.23013, 'prospectiveCashFlowYield': 6.87331, 'prospectiveDividendYield': 4.24151, 'forecasted5YearEarningsGrowth': 11.40056, 'forecastedEarningsGrowth': 19.96503, 'forecastedBookValueGrowth': 4.75903, 'forecastedRevenueGrowth': 2.20284, 'forecastedCashFlowGrowth': 13.83039, 'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Europe Large-Cap Blend Equity', 'secId': 'EUCA000511', 'currencyId': ''}, 'indexAverage': {'prospectiveEarningsYield': 11.07388, 'prospectiveBookValueYield': 1.5651, 'prospectiveRevenueYield': 1.11395, 'prospectiveCashFlowYield': 5.96117, 'prospectiveDividendYield': 4.3768, 'forecasted5YearEarningsGrowth': 11.18655, 'forecastedEarningsGrowth': 24.87068, 'forecastedBookValueGrowth': 4.49942, 'forecastedRevenueGrowth': 1.64071, 'forecastedCashFlowGrowth': 14.56048, 'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Morningstar Eur TME GR EUR', 'secId': 'F000016V5C', 'currencyId': ''}}
        """
        return self.GetFundsData("process/stockStyle/v2")
    
    def equityStyleBoxHistory(self):
        """
        This function retrieves the equity style history of the funds

        Returns:
            dict equity style history

        Examples:
            >>> Funds("myria", "fr").equityStyleBoxHistory()

            {'history': [{'year': 2022, 'portfolioDate': '2022-08-31T05:00:00.000', 'style': 2, 'percentage': 97.01546, 'relativeVolatility': None, 'categoryName': 'EAA Fund Europe Large-Cap Blend Equity'}], 'secId': 'F00000YIJ0', 'masterPortfolioId': '2852268', 'asOfDate': '2022-08-31T05:00:00.000'}

        """
        return self.GetFundsData("process/equityStyleBoxHistory")

    def esgData(self):
        """
        This function retrieves ESG data of the funds and category

        Returns:
            dict ESG data

        Examples:
            >>> Funds("myria", "fr").esgData()

            {'userType': 'Free', 'esgData': {'sociallyResponsibleFund': None, 'ethicalIssueStrategyFocus': None, 'portfolioDate': '2022-07-31T00:00:00.000', 'portfolioDateSustainabilityRating': '2022-07-31T05:00:00.000', 'fundESGScore': None, 'percentAUMCoveredESG': 99.38456, 'fundSustainabilityScore': 19.24, 'percentAUMCoveredControversy': 99.98864, 'categoryRankDate': '2022-07-31T05:00:00.000', 'sustainabilityFundQuintile': 3, 'sustainabilityPercentCategoryRank': 42.0, 'sustainabilityMandate': 'Yes', 'secId': 'F00000YIJ0', 'performanceId': '0P00019Q8D', 'tradingSymbol': None, 'iSIN': None, 'fundId': 'FS0000D31F', 'masterPortfolioId': '2852268', 'categoryId': 'EUCA000511', 'name': 'Myria Actions Durables Europe', 'controversyDeduction': None, 'categoryName': 'Europe Large-Cap Blend Equity', 'globalCategoryName': 'Europe Equity Large Cap', 'fundHistoryAvgSustainabilityScore': 19.24794, 'historicalSustainabilityScoreGlobalCategoryAverage': 19.64834, 'currentSustainabilityScoreGlobalCategoryAverage': 19.58899, 'numberofFundsAnalyzedinCategorySustainability': 2669, 'HistoryAvgSustainabilityPercentCategoryRank': None, 'sustainabilityRatingCorporateContributionPercent': 100.0, 'sustainabilityRatingSovereignContributionPercent': 0.0, 'portfolioSovereignsustainabilityscore': None, 'historicalSovereignSustainabilityScore': None, 'historicalSovereignSustainabilityCategoryAverage': 15.04535, 'sovereignSustainabilityRatingPercentOfEligiblePortfolioCovered': None, 'sustainabilityMandateSurveyed': None}, 'esgScoreCalculation': {'basedPercentAUM': 99.38456, 'portfolioESGScore': None, 'portfolioESGScoreCategory': None, 'controversyScore': None, 'controversyScoreCategory': None, 'sustainabilityScore': 19.24, 'sustainabilityScoreCategory': 19.58899, 'environmentalScore': 4.14, 'environmentalScoreCategory': None, 'socialScore': 8.22, 'socialScoreCategory': None, 'governanceScore': 6.88, 'governanceScoreCategory': None, 'portfolioDate': '2022-07-31T05:00:00.000', 'portfolioSustainabilityScore': 19.24, 'portfolioEnvironmentalRiskScore': 4.14, 'portfolioSocialRiskScore': 8.22, 'portfolioGovernanceRiskScore': 6.88, 'portfolioUnallocatedEsgRiskScore': 0.0, 'percentAUMCoveredControversy': 99.98864, 'esgFundQuintile': None, 'esgPercentCategoryRank': None, 'controversyFundQuintile': None, 'controversyPercentCategoryRank': None, 'ePercentCategoryRank': None, 'sPercentCategoryRank': None, 'gPercentCategoryRank': None, 'categoryRankDate': '2022-07-31T05:00:00.000', 'historicalSustainabilityScoreGlobalCategoryAverage': 19.64834, 'currentSustainabilityScoreGlobalCategoryAverage': 19.58899, 'HistoryAvgSustainabilityPercentCategoryRank': 42.0, 'numberofFundsAnalyzedinCategorySustainability': 2669}, 
            'esgHoldingsAnalyst': '_PO_', 'esgScoreDistribution': '_PO_', 'esgLevelDistribution': '_PO_', 'sustainabilityIntentionality': {'investmentId': 'FS0000D31F', 'eSGIncorporation': True, 'eSGEngagement': True, 'genderDiversity': False, 'lowCarbonFossilFuelFree': False, 'communityDevelopment': False, 'environmental': False, 'otherImpactThemes': False, 'renewableEnergy': False, 'waterFocused': False, 'generalEnvironmentalSector': False, 'sustainableInvestmentOverall': True, 'eSGFundOverall': True, 'impactFundOverall': False, 'environmentalSectorOverall': False, 'createdOn': '2019-01-08 04:00:00.0', 'lastUpdateDate': '2022-09-28 04:01:00.0', 'usesNormsBasedScreening': None, 'excludesAbortionStemCells': None, 'excludesAdultEntertainment': None, 'excludesAlcohol': None, 'excludesAnimalTesting': None, 'excludesControversialWeapons': None, 'excludesFurSpecialtyLeather': None, 'excludesGambling': None, 'excludesGMOs': None, 'excludesMilitaryContracting': None, 'excludesNuclear': None, 'excludesPalmOil': None, 'excludesPesticides': None, 'excludesSmallArms': None, 'excludesThermalCoal': None, 'excludesTobacco': None, 'excludesOther': None, 'employsExclusionsOverall': None}}
        
        """

        return self.GetFundsData("esg/v1")

    def factorProfile(self):
        """
        This function retrieves the factor profile of the funds, index and category

        Returns:
            dict factor profile

        Examples:
            >>> Funds("myria", "fr").factorProfile()

            {'name': 'Myria Actions Durables Europe', 'categoryId': 'EUCA000511', 'categoryName': 'Europe Large-Cap Blend Equity', 'indexId': 'F000016V5C', 'indexName': 'Morningstar Eur TME GR EUR', 'indexEffectiveDate': '2022-08-31', 'categoryEffectiveDate': '2022-08-31', 'ticker': None, 'id': '0P00019Q8D', 'effectiveDate': '2022-08-31', 'factors': {'style': {'categoryAvg': 43.972717, 'indexAvg': 53.582795, 'percentile': 41.810942, 'historicRange': [{'year': '1', 'min': 37.737166, 'max': 50.694038}, {'year': '3', 'min': 37.737166, 'max': 50.694038}, {'year': '5', 'min': 37.737166, 'max': 50.694038}]}, 'yield': {'categoryAvg': 44.894873, 'indexAvg': 32.632299, 'percentile': 32.396237, 'historicRange': [{'year': '1', 'min': 25.010467, 'max': 40.238631}, {'year': '3', 'min': 25.010467, 'max': 40.238631}, {'year': '5', 'min': 25.010467, 'max': 40.238631}]}, 'quality': {'categoryAvg': 48.689334, 'indexAvg': 54.731861, 'percentile': 43.387003, 'historicRange': [{'year': '1', 'min': 40.856001, 'max': 50.587487}, {'year': '3', 'min': 40.856001, 'max': 50.587487}, {'year': '5', 'min': 40.856001, 'max': 50.587487}]}, 'momentum': {'categoryAvg': 54.346187, 'indexAvg': 41.592238, 'percentile': 47.615288, 'historicRange': [{'year': '1', 'min': 35.098478, 'max': 58.163375}, {'year': '3', 'min': 35.098478, 'max': 58.163375}, {'year': '5', 'min': 35.098478, 'max': 58.163375}]}, 'volatility': {'categoryAvg': 59.365095, 'indexAvg': 64.87211, 'percentile': 72.380962, 'historicRange': [{'year': '1', 'min': 58.840344, 'max': 74.446747}, {'year': '3', 'min': 58.840344, 'max': 74.446747}, {'year': '5', 'min': 58.840344, 'max': 74.446747}]}, 'liquidity': {'categoryAvg': 42.525891, 'indexAvg': 36.874471, 'percentile': 50.802125, 'historicRange': [{'year': '1', 'min': 30.942716, 'max': 53.826165}, {'year': '3', 'min': 30.942716, 'max': 53.826165}, {'year': '5', 'min': 30.942716, 'max': 53.826165}]}, 'size': {'categoryAvg': 64.682823, 'indexAvg': 77.751371, 'percentile': 92.165035, 'historicRange': [{'year': '1', 'min': 92.165035, 'max': 94.167559}, {'year': '3', 'min': 92.165035, 'max': 94.167559}, {'year': '5', 'min': 92.165035, 'max': 94.167559}]}}}
        
        """
        return self.GetFundsData("factorProfile")

    def feeLevel(self):
        """        
        This function retrieves the fees of the fund.

        Returns:
            dict fees

        Examples:
            >>> Funds("rmagx", "us").feeLevel()

            {'morningstarFeeLevelRankDate': '2022-08-31T05:00:00.000', 'morningstarFeeLevelGroup': '$GFS$000E9', 'name': 'Government Retirement, Large', 'morningstarFeeLevel': 1, 'morningstarFeeLevelPercentileRank': 1.0, 'morningstarFeeLevelGroupSize': 29.0, 'median': 0.44, 'morningstarFeeLevelGroupStartingDistribution': 0.22, 'morningstarFeeLevelGroup1stBreakpointDistribution': 0.32, 'morningstarFeeLevelGroup2ndBreakpointDistribution': 0.39, 'morningstarFeeLevelGroup3rdBreakpointDistribution': 0.48, 'morningstarFeeLevelGroup4thBreakpointDistribution': 0.6, 'morningstarFeeLevelGroupEndBreakpointDistribution': 0.67, 'fundFee': 0.22, 'reportDate': '2021-08-31T05:00:00.000', 'peerMedian': 2.5555555555555554, 'fundIndex': 0.0, 'prospectusExpenseRatio': 0.22, 'icrFund': None, 'priceTemplate': 'USA_OE', 'morningstarTotalCostRatioPDS': None}

        """
        return self.GetFundsData("price/feeLevel")

    def fees(self):
        """        
        This function retrieves the fees of the fund (by scraping pages);

        Returns:
            dict fees

        Examples:
            >>> Funds("myria", "fr").fees()

            {'Frais de souscription max': '5,00%', 'Frais de rachat max.': 'n/a', 'Frais de conversion': '-', 'Frais de gestion annuels maximum': '0,50%', 'Frais courants': '1,08%'}
        
        """
        no_site_error(self.code,self.name,self.country,self.site)
        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=5"
        response = requests.get(url, headers=headers)
        not_200_response(url,response)
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

    def financialMetrics(self):
        """        
        This function retrieves the final metrics of the funds and category.

        Returns:
            dict financial metrics

        Examples:
            >>> Funds("rmagx", "us").financialMetrics()

            {'userType': 'Free', 'fund': {'masterPortfolioId': '564578', 'portfolioDate': '2022-06-30T05:00:00.000', 'wideMoatPercentage': '_PO_', 'narrowMoatPercentage': 
            '_PO_', 'noMoatPercentage': '_PO_', 'financialHealthGradeType': '_PO_', 'profitabilityGradeType': '_PO_', 'growthGradeType': '_PO_', 'roic': '_PO_', 'cashReturn': '_PO_', 'freeCashFlowYield': '_PO_', 'debtToCapital': '_PO_', 'securityName': 'American Funds Mortgage R6'}, 'category': {'masterPortfolioId': '210755', 'portfolioDate': '2022-08-31T05:00:00.000', 'wideMoatPercentage': '_PO_', 'narrowMoatPercentage': '_PO_', 'noMoatPercentage': '_PO_', 'financialHealthGradeType': '_PO_', 'profitabilityGradeType': '_PO_', 'growthGradeType': '_PO_', 'roic': '_PO_', 'cashReturn': '_PO_', 'freeCashFlowYield': '_PO_', 'debtToCapital': '_PO_', 'securityName': 'Intermediate Government'}, 'index': {'masterPortfolioId': '1853142', 'portfolioDate': '2022-08-31T05:00:00.000', 'wideMoatPercentage': '_PO_', 'narrowMoatPercentage': '_PO_', 'noMoatPercentage': '_PO_', 'financialHealthGradeType': '_PO_', 'profitabilityGradeType': '_PO_', 'growthGradeType': '_PO_', 'roic': '_PO_', 'cashReturn': '_PO_', 'freeCashFlowYield': '_PO_', 'debtToCapital': '_PO_', 'securityName': 'Morningstar US Trsy Bd TR USD'}}
        
        """
        return self.GetFundsData("process/financialMetrics")


    def fixedIncomeStyle(self):
        """        
        This function retrieves the fixed income style of the funds and category.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("rmagx", "us").fixedIncomeStyle()

            {'isCan': False, 'portfolioDate': '2022-06-30T05:00:00.000', 'assetType': 'FIXEDINCOME', 'fixedIncStyleBox': 2, 'fund': {'secId': 'F00000JNX4', 'secName': 'American Funds Mortgage R6', 'portfolioDate': '2022-06-30T05:00:00.000', 'avgEffectiveDuration': 5.90335, 'modifiedDuration': None, 'avgEffectiveMaturity': None, 
            'avgCreditQualityName': 'AAA', 'surveyedAverageSurveyedCreditRating': 'AAA', 'calculatedAverageCreditRating': None, 'avgCreditQualityDate': '2022-06-30T05:00:00.000', 'avgCoupon': 3.19527, 'avgPrice': 97.05785, 'yieldToMaturity': 4.184}, 'categoryAverage': {'secId': '$FOCA$GI$$', 'secName': 'Intermediate Government', 'portfolioDate': '2022-08-31T05:00:00.000', 'avgEffectiveDuration': 5.48744, 'modifiedDuration': 5.79579, 'avgEffectiveMaturity': 7.31705, 'avgCreditQualityName': 'AAA', 'surveyedAverageSurveyedCreditRating': 'AAA', 'calculatedAverageCreditRating': None, 'avgCreditQualityDate': '2022-06-30T05:00:00.000', 'avgCoupon': 2.24416, 'avgPrice': 94.6374, 'yieldToMaturity': 3.96993}}

        """

        return self.GetFundsData("process/fixedIncomeStyle")

    def fixedincomeStyleBoxHistory(self):
        """        
        This function retrieves the fixed income style history of the funds.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("rmagx", "us").fixedincomeStyleBoxHistory()

            {'history': [{'year': 2022, 'portfolioDate': '2022-06-30T05:00:00.000', 'style': 2, 'percentage': 65.12712, 'relativeVolatility': None, 'categoryName': 'US Fund Intermediate Government'}, {'year': 2021, 'portfolioDate': '2021-12-31T06:00:00.000', 'style': 1, 'percentage': 63.32053, 'relativeVolatility': None, 'categoryName': 'US Fund Intermediate Government'}, {'year': 2020, 'portfolioDate': '2020-12-31T06:00:00.000', 'style': 1, 'percentage': 64.09708, 'relativeVolatility': None, 'categoryName': 'US Fund Intermediate Government'}, {'year': 2019, 'portfolioDate': '2019-12-31T06:00:00.000', 'style': 1, 'percentage': 79.54471, 'relativeVolatility': None, 'categoryName': 'US Fund Intermediate Government'}, {'year': 2018, 'portfolioDate': '2018-12-31T06:00:00.000', 'style': 2, 'percentage': 74.84264, 'relativeVolatility': None, 'categoryName': 'US Fund Intermediate Government'}], 'secId': 'F00000JNX4', 'masterPortfolioId': '564578', 'asOfDate': '2022-06-30T05:00:00.000'}

        """
        return self.GetFundsData("process/fixedincomeStyleBoxHistory")

    def fundsAnnualPerformance(self):
        """        
        This function retrieves the annual performance of the funds.

        Returns:
            dict funds annual performance 

        Examples:
            >>> Funds("myria", "fr").fundsAnnualPerformance()

            {'funds_annual_performance_2016': '-4,63', 'funds_annual_performance_2017': '11,29', 'funds_annual_performance_2018': '-15,56', 'funds_annual_performance_2019': '22,27', 'funds_annual_performance_2020': '-9,89', 'funds_annual_performance_2021': '20,55', 'funds_annual_performance_current': '-14,25'}
        
        """
        return self.AnnualPerformance('funds')

    def fundsAnnualRank(self):
        """        
        This function retrieves the annual rank of the funds in percentile.

        Returns:
            dict funds annual rank

        Examples:
            >>> Funds("myria", "fr").fundsAnnualRank()

            {'rank_annual_performance_2016': '88', 'rank_annual_performance_2017': '29', 'rank_annual_performance_2018': '80', 'rank_annual_performance_2019': '76', 'rank_annual_performance_2020': '96', 'rank_annual_performance_2021': '77', 'rank_annual_performance_current': '52'}
        """
        return self.AnnualPerformance('rank')

    def fundsCumulativePerformance(self):
        """        
        This function retrieves the cumulative performance of the funds.

        Returns:
            dict funds cumulative performance

        Examples:
            >>> Funds("myria", "fr").fundsCumulativePerformance()

            {'cumulative_performance_date': '26/09/2022', 'funds_cumulative_performance_1 jour': '-0,49', 'funds_cumulative_performance_1 semaine': '-4,31', 'funds_cumulative_performance_1 mois': '-7,17', 'funds_cumulative_performance_3 mois': '-5,18', 'funds_cumulative_performance_6 mois': '-11,31', "funds_cumulative_performance_Début d'année": '-18,53', 'funds_cumulative_performance_1 an': '-15,41', 'funds_cumulative_performance_3 ans (annualisée)': '-2,73', 'funds_cumulative_performance_5 ans (annualisée)': '-1,74', 'funds_cumulative_performance_10 ans (annualisée)': '-'}
        
        """
        return self.CumulativePerformance('funds')

    def fundsQuarterlyPerformance(self):
        """        
        This function retrieves the quarterly performance of the funds.

        Returns:
            dict funds quarterly performance

        Examples:
            >>> Funds("myria", "fr").fundsCumulativePerformance()

            {'quarterly_performance_date': '26/09/2022', 'performance_2022_quarter_1': '-7,25', 'performance_2022_quarter_2': '-9,35', 'performance_2022_quarter_3': '-', 'performance_2022_quarter_4': '-', 'performance_2021_quarter_1': '7,81', 'performance_2021_quarter_2': '5,77', 'performance_2021_quarter_3': '-0,20', 'performance_2021_quarter_4': '5,93', 'performance_2020_quarter_1': '-23,96', 'performance_2020_quarter_2': '13,14', 'performance_2020_quarter_3': '-3,36', 'performance_2020_quarter_4': '8,39', 'performance_2019_quarter_1': '10,48', 'performance_2019_quarter_2': '4,93', 'performance_2019_quarter_3': '2,17', 'performance_2019_quarter_4': '3,23', 'performance_2018_quarter_1': '-3,92', 'performance_2018_quarter_2': '0,97', 'performance_2018_quarter_3': '0,03', 'performance_2018_quarter_4': '-12,98', 'performance_2017_quarter_1': '5,47', 'performance_2017_quarter_2': '4,36', 'performance_2017_quarter_3': '2,04', 'performance_2017_quarter_4': '-0,91'}
        
        """
        no_site_error(self.code,self.name,self.country,self.site)
        result = {}
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}&tab=1"
        
        response = requests.get(url, headers=headers)
        not_200_response(url,response)
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

    def GetFundsData(self,field,params={}):
        """
        Generic function to use MorningStar global api for funds.

        Args:
            field (str) : endpoint of the request
            params (dict) : parameter for the request

        Raises:
            TypeError raised whenever type of paramater are invalid

        Returns:
            dict with funds data

        Examples:
            >>> Funds("rmagx", "us").GetFundsData("price/feeLevel")

            {'morningstarFeeLevelRankDate': '2022-08-31T05:00:00.000', 'morningstarFeeLevelGroup': '$GFS$000E9', 'name': 'Government Retirement, Large', 'morningstarFeeLevel': 1, 'morningstarFeeLevelPercentileRank': 1.0, 'morningstarFeeLevelGroupSize': 29.0, 'median': 0.44, 'morningstarFeeLevelGroupStartingDistribution': 0.22, 'morningstarFeeLevelGroup1stBreakpointDistribution': 0.32, 'morningstarFeeLevelGroup2ndBreakpointDistribution': 0.39, 'morningstarFeeLevelGroup3rdBreakpointDistribution': 0.48, 'morningstarFeeLevelGroup4thBreakpointDistribution': 0.6, 'morningstarFeeLevelGroupEndBreakpointDistribution': 0.67, 'fundFee': 0.22, 'reportDate': '2021-08-31T05:00:00.000', 'peerMedian': 2.5555555555555554, 'fundIndex': 0.0, 'prospectusExpenseRatio': 0.22, 'icrFund': None, 'priceTemplate': 'USA_OE', 'morningstarTotalCostRatioPDS': None}

        """

        if not isinstance(field, str):
            raise TypeError('field parameter should be a string')

        if not isinstance(params, dict):
            raise TypeError('params parameter should be a dict')

        #url of API
        url = f"""https://api-global.morningstar.com/sal-service/v1/{self.asset_type}/{field}/{self.code}/data"""


        #headers
        headers = {
            "apikey" : APIKEY,
        }

        response = requests.get(url,params=params, headers=headers)


        not_200_response(url,response)

        return json.loads(response.content.decode()) 


    def graphData(self):
        """        
        This function retrieves historical data of the funds.

        Returns:
            dict historical data

        Examples:
            >>> Funds("myria", "fr").graphData()

            {'startYear': 2012, 'latestDate': '2022-08-31T05:00:00.000', 'endYear': 2022, 'secId': 'F00000YIJ0', 'currency': 'EUR', 'data': [{'yr': 2012, 'naQ1': 2.464477033, 'naQ2': 2.235847794, 'naQ3': 2.390125638, 'naQ4': 2.372812015, 'naYr': 2.372812015, 'nfQ1': -0.047098652, 'nfQ2': -0.070992663, 'nfQ3': -0.024836406, 'nfQ4': -0.074109929, 'nfYr': -0.21703765, 'numFund': 17, 'industryMarketShare': 0.0559487, 'growthRate': -9.4092724, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2013, 'naQ1': 3.194399804, 'naQ2': 3.442772317, 'naQ3': 3.816702249, 'naQ4': 3.8546572, 'naYr': 3.8546572, 'nfQ1': 0.757345049, 'nfQ2': 0.29710732, 'nfQ3': 0.10691278, 'nfQ4': -0.0973476, 'nfYr': 1.064017549, 'numFund': 30, 'industryMarketShare': 0.08002847, 'growthRate': 44.84204995, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2014, 'naQ1': 3.927479244, 'naQ2': 4.061212859, 'naQ3': 3.901098262, 'naQ4': 2.405659141, 'naYr': 2.405659141, 'nfQ1': -0.044491881, 
            'nfQ2': -0.046020271, 'nfQ3': -0.041260313, 'nfQ4': -0.016291675, 'nfYr': -0.14806414, 'numFund': 33, 'industryMarketShare': 0.04235961, 'growthRate': -3.84117529, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2015, 'naQ1': 4.381275393, 'naQ2': 4.322273742, 'naQ3': 3.222528809, 'naQ4': 3.369017376, 'naYr': 3.369017376, 'nfQ1': -0.104764233, 'nfQ2': -0.046621245, 'nfQ3': -0.127947598, 'nfQ4': -0.036210426, 'nfYr': -0.315543502, 'numFund': 38, 'industryMarketShare': 0.05420981, 'growthRate': -13.11671702, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2016, 'naQ1': 2.749482462, 'naQ2': 3.084331608, 'naQ3': 2.697440797, 
            'naQ4': 2.929405575, 'naYr': 2.929405575, 'nfQ1': 0.042629864, 'nfQ2': -0.051730097, 'nfQ3': -0.078133351, 'nfQ4': 0.099158505, 'nfYr': 0.011924921, 'numFund': 38, 'industryMarketShare': 0.04426975, 'growthRate': 0.35395843, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2017, 'naQ1': 2.905459428, 'naQ2': 2.956446018, 'naQ3': 3.011333783, 'naQ4': 2.97599636, 'naYr': 2.97599636, 'nfQ1': -0.172462219, 'nfQ2': -0.040957871, 'nfQ3': -0.006021127, 'nfQ4': -0.024037606, 'nfYr': -0.243478823, 'numFund': 36, 'industryMarketShare': 0.03988733, 'growthRate': -8.31154365, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2018, 'naQ1': 2.854676298, 'naQ2': 2.812776938, 'naQ3': 2.772873545, 'naQ4': 2.417144848, 'naYr': 2.417144848, 'nfQ1': -0.035047001, 'nfQ2': -0.0421686, 'nfQ3': -0.032215405, 'nfQ4': -0.024875408, 'nfYr': -0.134306414, 'numFund': 32, 'industryMarketShare': 0.03406822, 'growthRate': -4.51298986, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2019, 'naQ1': 2.570570766, 'naQ2': 2.524971015, 'naQ3': 2.463577471, 'naQ4': 2.413580097, 'naYr': 2.413580097, 'nfQ1': -0.058482129, 'nfQ2': -0.117375392, 'nfQ3': -0.086800469, 'nfQ4': -0.119468465, 'nfYr': -0.382126455, 'numFund': 31, 'industryMarketShare': 0.02869889, 'growthRate': -15.80900107, 
            'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2020, 'naQ1': 1.78167016, 'naQ2': 2.017066222, 'naQ3': 2.029954347, 'naQ4': 2.144201339, 'naYr': 2.144201339, 'nfQ1': -0.061129362, 'nfQ2': -0.022424582, 'nfQ3': -0.026901527, 'nfQ4': -0.086423606, 'nfYr': -0.196879077, 'numFund': 20, 'industryMarketShare': 0.02418613, 'growthRate': -8.15713874, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2021, 'naQ1': 2.215748096, 'naQ2': 2.252728103, 'naQ3': 2.189458162, 'naQ4': 2.199564794, 'naYr': 2.199564794, 'nfQ1': -0.059169294, 'nfQ2': -0.198106981, 'nfQ3': -0.071887543, 'nfQ4': -0.100211793, 'nfYr': -0.429375611, 'numFund': 16, 'industryMarketShare': 0.02074277, 'growthRate': -20.02496702, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}, {'yr': 2022, 'naQ1': 1.93610077, 'naQ2': 1.723817952, 'naQ3': None, 'naQ4': None, 'naYr': 1.805962297, 'nfQ1': -0.052301651, 'nfQ2': -0.00400788, 'nfQ3': 0.034751063, 'nfQ4': None, 'nfYr': -0.021558468, 'numFund': 15, 'industryMarketShare': 0.01952641, 'growthRate': -0.98012425, 'nfMagnitude': 'Bil', 'naMagnitude': 'Bil'}]}
                    
        """

        return self.GetFundsData("parent/graphData")

    def historicalData(self):
        """
        This function retrieves the historical price of the funds, index and category

        Returns:
            dict with historical data

        Examples:
            >>> Funds("myria", "fr").historicalData()

            {'userType': 'Free', 'baseCurrency': 'EUR', 'asOfDate': '2022-09-26T00:00:00.000', 'startDate': '2012-01-01T00:00:00.000', 'categoryName': 'Europe Large-Cap Blend Equity', 'indexName': 'Morningstar Eur TME GR EUR', 'graphData': {'fund': [{'date': '2015-11-30', 'value': 10099.3}, {'date': '2015-12-31', 'value': 9512.0}, {'date': '2016-01-31', 'value': 8861.1}, {'date': '2016-02-29', 'value': 8581.7}, {'date': '2016-03-31', 'value': 8655.199999999999}, {'date': '2016-04-30', 'value': 8679.8}, {'date': '2016-05-31', 'value': 8823.0}, {'date': '2016-06-30', 'value': 8252.300000000001}, {'date': '2016-07-31', 'value': 8651.7}, {'date': '2016-08-31', 'value': 8706.0}, {'date': '2016-09-30', 'value': 8682.300000000001}, {'date': '2016-10-31', 'value': 8576.4}, {'date': '2016-11-30', 'value': 8574.3}, {'date': '2016-12-31', 'value': 9071.2}, {'date': '2017-01-31', 'value': 9021.9}, {'date': '2017-02-28', 'value': 9290.0}, {'date': '2017-03-31', 'value': 9567.4}, {'date': '2017-04-30', 'value': 9945.6}, {'date': '2017-05-31', 'value': 10296.199999999999}, {'date': '2017-06-30', 'value': 9984.9}, {'date': '2017-07-31', 'value': 9924.6}, {'date': '2017-08-31', 'value': 9809.7}, {'date': '2017-09-30', 'value': 10188.699999999999}, {'date': '2017-10-31', 'value': 10248.499999999998}, {'date': '2017-11-30', 'value': 10110.5}, {'date': '2017-12-31', 'value': 10095.6}, {'date': '2018-01-31', 'value': 10267.2}, {'date': '2018-02-28', 'value': 9931.9}, {'date': '2018-03-31', 'value': 9699.6}, {'date': '2018-04-30', 'value': 9926.8}, {'date': '2018-05-31', 'value': 9821.5}, {'date': '2018-06-30', 'value': 9793.6}, {'date': '2018-07-31', 'value': 9950.3}, {'date': '2018-08-31', 'value': 9879.1}, {'date': '2018-09-30', 'value': 9796.3}, {'date': '2018-10-31', 'value': 9165.3}, {'date': '2018-11-30', 'value': 9112.6}, {'date': '2018-12-31', 'value': 8524.9}, {'date': '2019-01-31', 'value': 8882.7}, {'date': '2019-02-28', 'value': 9257.8}, {'date': '2019-03-31', 'value': 9418.2}, {'date': '2019-04-30', 'value': 9825.7}, {'date': '2019-05-31', 'value': 9420.7}, {'date': '2019-06-30', 'value': 9882.9}, {'date': '2019-07-31', 'value': 9882.7}, {'date': '2019-08-31', 'value': 9779.6}, {'date': '2019-09-30', 'value': 10097.7}, {'date': '2019-10-31', 'value': 10057.6}, {'date': '2019-11-30', 'value': 10273.2}, {'date': '2019-12-31', 'value': 10423.399999999998}, {'date': '2020-01-31', 'value': 10229.699999999999}, {'date': '2020-02-29', 'value': 9357.8}, {'date': '2020-03-31', 'value': 7925.599999999999}, {'date': '2020-04-30', 'value': 8336.8}, {'date': '2020-05-31', 'value': 8580.2}, {'date': '2020-06-30', 'value': 8967.0}, {'date': '2020-07-31', 'value': 8760.3}, {'date': '2020-08-31', 'value': 8956.1}, {'date': '2020-09-30', 'value': 8665.5}, {'date': '2020-10-31', 'value': 8132.200000000001}, {'date': '2020-11-30', 'value': 9265.5}, {'date': '2020-12-31', 'value': 9392.5}, {'date': '2021-01-31', 'value': 9250.7}, {'date': '2021-02-28', 'value': 9519.0}, {'date': '2021-03-31', 'value': 10126.0}, {'date': '2021-04-30', 'value': 10347.9}, {'date': '2021-05-31', 'value': 10606.099999999999}, {'date': '2021-06-30', 'value': 10710.2}, {'date': '2021-07-31', 'value': 10786.199999999999}, {'date': '2021-08-31', 'value': 11069.1}, {'date': '2021-09-30', 'value': 10689.000000000002}, {'date': '2021-10-31', 'value': 11126.099999999999}, {'date': '2021-11-30', 'value': 10702.400000000001}, {'date': '2021-12-31', 'value': 11322.999999999998}, {'date': '2022-01-31', 'value': 10914.8}, {'date': '2022-02-28', 'value': 10456.800000000001}, {'date': '2022-03-31', 'value': 10501.7}, {'date': '2022-04-30', 'value': 10390.5}, {'date': '2022-05-31', 'value': 10385.199999999999}, {'date': '2022-06-30', 
            'value': 9519.6}, {'date': '2022-07-31', 'value': 10163.9}, {'date': '2022-08-31', 'value': 9709.5}, {'date': '2022-09-26', 'value': 9224.7}], 'index': [{'date': '2015-11-30', 'value': 10100.997926241138}, {'date': '2015-12-31', 'value': 9564.68772758299}, {'date': '2016-01-31', 'value': 8987.652810750973}, {'date': '2016-02-29', 'value': 8812.340487172096}, {'date': '2016-03-31', 'value': 8961.655501546189}, {'date': '2016-04-30', 'value': 9154.087529800909}, {'date': '2016-05-31', 'value': 9358.629354968092}, {'date': '2016-06-30', 'value': 8986.299445416213}, {'date': '2016-07-31', 'value': 9289.64663653437}, {'date': '2016-08-31', 'value': 9353.293657114458}, {'date': '2016-09-30', 'value': 9352.40470373525}, {'date': '2016-10-31', 'value': 9283.026150660839}, {'date': '2016-11-30', 'value': 9382.676389130957}, {'date': '2016-12-31', 'value': 9961.816533840063}, {'date': '2017-01-31', 'value': 9925.177428810894}, {'date': '2017-02-28', 'value': 10203.314131748964}, {'date': '2017-03-31', 'value': 10542.537465397882}, {'date': '2017-04-30', 'value': 10738.959991656406}, {'date': '2017-05-31', 'value': 10897.264248048754}, {'date': '2017-06-30', 'value': 10629.452609429669}, {'date': '2017-07-31', 'value': 10601.237988308518}, {'date': '2017-08-31', 'value': 10544.891166429761}, {'date': '2017-09-30', 'value': 10938.184810275308}, {'date': '2017-10-31', 'value': 11147.115838765278}, {'date': '2017-11-30', 'value': 10910.415590840103}, {'date': '2017-12-31', 'value': 11002.603086424442}, {'date': '2018-01-31', 'value': 11202.816502855874}, {'date': '2018-02-28', 'value': 10786.63698232205}, {'date': '2018-03-31', 'value': 10575.453428261944}, {'date': '2018-04-30', 'value': 11052.43818924069}, {'date': '2018-05-31', 'value': 11072.470356530652}, {'date': '2018-06-30', 'value': 11012.721972248872}, {'date': '2018-07-31', 'value': 11362.142274171887}, {'date': '2018-08-31', 'value': 11090.64704495534}, {'date': '2018-09-30', 'value': 11181.833566914047}, {'date': '2018-10-31', 'value': 10593.401546901361}, {'date': '2018-11-30', 'value': 10512.484780859788}, {'date': '2018-12-31', 'value': 9944.335059905985}, {'date': '2019-01-31', 'value': 10590.76256423964}, {'date': '2019-02-28', 'value': 11005.973454123312}, {'date': '2019-03-31', 'value': 11242.073857870178}, {'date': '2019-04-30', 'value': 11670.981902178677}, {'date': '2019-05-31', 'value': 11144.412425324008}, {'date': '2019-06-30', 'value': 11643.46466450507}, {'date': '2019-07-31', 'value': 11690.94880938203}, {'date': '2019-08-31', 'value': 11500.804456558366}, {'date': '2019-09-30', 'value': 11937.599785176299}, {'date': '2019-10-31', 'value': 12069.496863295946}, {'date': 
            '2019-11-30', 'value': 12396.179287945091}, {'date': '2019-12-31', 'value': 12669.05174102269}, {'date': '2020-01-31', 'value': 12503.434144601693}, 
            {'date': '2020-02-29', 'value': 11422.967928329139}, {'date': '2020-03-31', 'value': 9758.796231962979}, {'date': '2020-04-30', 'value': 10384.185300574401}, {'date': '2020-05-31', 'value': 10726.400582729833}, {'date': '2020-06-30', 'value': 11040.508288168154}, {'date': '2020-07-31', 'value': 10894.103248486992}, {'date': '2020-08-31', 'value': 11207.631714837893}, {'date': '2020-09-30', 'value': 11045.04561849105}, {'date': '2020-10-31', 'value': 10475.625845665943}, {'date': '2020-11-30', 'value': 11970.741638525886}, {'date': '2020-12-31', 'value': 12284.717484141114}, {'date': '2021-01-31', 'value': 12189.99281928531}, {'date': '2021-02-28', 'value': 12513.962197772677}, {'date': '2021-03-31', 'value': 13333.69159398476}, {'date': '2021-04-30', 'value': 13616.382532351252}, {'date': '2021-05-31', 'value': 14008.939177388762}, {'date': '2021-06-30', 'value': 14392.093138940441}, {'date': '2021-07-31', 'value': 14664.965464432338}, {'date': '2021-08-31', 'value': 14974.972374027413}, {'date': '2021-09-30', 'value': 14576.245748230402}, {'date': '2021-10-31', 'value': 15248.836295595838}, {'date': '2021-11-30', 'value': 14834.396980245465}, {'date': '2021-12-31', 'value': 15642.164515166645}, {'date': '2022-01-31', 'value': 15124.52629262864}, {'date': '2022-02-28', 'value': 14518.463459617597}, {'date': '2022-03-31', 'value': 14515.101193610812}, {'date': '2022-04-30', 'value': 14439.629274990995}, {'date': '2022-05-31', 'value': 14340.198101171341}, {'date': '2022-06-30', 'value': 13224.756943974638}, {'date': '2022-07-31', 'value': 14238.576536018461}, {'date': '2022-08-31', 'value': 13550.09646531659}, {'date': '2022-09-26', 'value': 12712.08831211816}], 'category': [{'date': '2015-11-30', 'value': 10129.465150758773}, {'date': '2015-12-31', 'value': 
            9701.065557262555}, {'date': '2016-01-31', 'value': 9057.4226697338}, {'date': '2016-02-29', 'value': 8871.694518488892}, {'date': '2016-03-31', 'value': 9018.033231303001}, {'date': '2016-04-30', 'value': 9132.267529496912}, {'date': '2016-05-31', 'value': 9375.067540526077}, {'date': '2016-06-30', 'value': 8864.80116421857}, {'date': '2016-07-31', 'value': 9191.164432247222}, {'date': '2016-08-31', 'value': 9265.634762252468}, {'date': '2016-09-30', 'value': 9234.23497992687}, {'date': '2016-10-31', 'value': 9130.190951904802}, {'date': '2016-11-30', 'value': 9206.081060644314}, {'date': '2016-12-31', 'value': 9677.495318054354}, {'date': '2017-01-31', 'value': 9661.544116773131}, {'date': '2017-02-28', 'value': 9906.392242174594}, {'date': '2017-03-31', 'value': 10225.021626860309}, {'date': '2017-04-30', 'value': 10456.316530773045}, {'date': '2017-05-31', 'value': 10610.193480950466}, {'date': '2017-06-30', 'value': 10350.6775410649}, {'date': '2017-07-31', 'value': 10322.673489945508}, {'date': '2017-08-31', 'value': 10228.155841724565}, {'date': '2017-09-30', 'value': 10597.729080666757}, {'date': '2017-10-31', 'value': 10803.09243308845}, {'date': '2017-11-30', 'value': 10584.908424038038}, {'date': '2017-12-31', 'value': 10651.246580847013}, {'date': '2018-01-31', 'value': 10832.73947721685}, {'date': '2018-02-28', 'value': 10449.887288799751}, {'date': '2018-03-31', 'value': 10222.663242050527}, {'date': '2018-04-30', 'value': 10643.237867770697}, {'date': '2018-05-31', 'value': 10708.600069928858}, {'date': '2018-06-30', 'value': 10593.624958659693}, {'date': '2018-07-31', 'value': 10863.541692542538}, {'date': '2018-08-31', 'value': 10689.75484544963}, {'date': '2018-09-30', 'value': 10680.932693740628}, {'date': '2018-10-31', 'value': 10012.815910022658}, {'date': '2018-11-30', 'value': 9883.3376353285}, {'date': '2018-12-31', 'value': 9296.913490150586}, {'date': '2019-01-31', 'value': 9873.31960421884}, {'date': '2019-02-28', 'value': 10249.163714520986}, {'date': '2019-03-31', 'value': 10436.345284706284}, {'date': '2019-04-30', 'value': 10813.605737799777}, {'date': '2019-05-31', 'value': 10304.865656675493}, {'date': '2019-06-30', 'value': 10725.968795550496}, {'date': '2019-07-31', 'value': 10756.863306585665}, {'date': '2019-08-31', 'value': 10601.899736354155}, {'date': '2019-09-30', 'value': 10934.28632279952}, {'date': 
            '2019-10-31', 'value': 11045.711774926887}, {'date': '2019-11-30', 'value': 11357.675877145828}, {'date': '2019-12-31', 'value': 11575.331595774278}, {'date': '2020-01-31', 'value': 11450.819923327157}, {'date': '2020-02-29', 'value': 10569.096437455946}, {'date': '2020-03-31', 'value': 9002.248163896129}, {'date': '2020-04-30', 'value': 9655.581827606495}, {'date': '2020-05-31', 'value': 9987.670909934837}, {'date': '2020-06-30', 'value': 10271.78447056939}, {'date': '2020-07-31', 'value': 10249.763194716385}, {'date': '2020-08-31', 'value': 10565.738250492765}, {'date': '2020-09-30', 'value': 10434.652321888467}, {'date': '2020-10-31', 'value': 9896.797895571286}, {'date': '2020-11-30', 'value': 11199.514862536433}, {'date': '2020-12-31', 'value': 11470.529962748273}, {'date': '2021-01-31', 'value': 11397.40012301247}, {'date': '2021-02-28', 'value': 11649.375639912978}, {'date': '2021-03-31', 'value': 12347.227101607741}, {'date': '2021-04-30', 'value': 12609.088844114385}, {'date': '2021-05-31', 'value': 12912.096361582839}, {'date': '2021-06-30', 'value': 13116.181670577833}, {'date': '2021-07-31', 'value': 13360.376196577081}, {'date': '2021-08-31', 'value': 13661.532443618502}, {'date': '2021-09-30', 'value': 13213.653390689804}, {'date': '2021-10-31', 'value': 13776.539651049192}, {'date': '2021-11-30', 'value': 13456.899194015588}, {'date': '2021-12-31', 'value': 14107.072366594708}, {'date': '2022-01-31', 'value': 13462.727201439364}, {'date': '2022-02-28', 'value': 12967.1761296359}, {'date': '2022-03-31', 'value': 13112.243287560148}, {'date': '2022-04-30', 'value': 12948.83505169048}, {'date': '2022-05-31', 'value': 12813.209697193479}, {'date': '2022-06-30', 'value': 11798.33468559014}, {'date': '2022-07-31', 'value': 12682.510981697294}, {'date': '2022-08-31', 'value': 12050.644599068648}, {'date': '2022-09-26', 'value': 11251.033314798367}]}, 'fundFlowData': [{'date': '2012-01-31', 'value': None}, {'date': '2012-02-29', 'value': None}, {'date': '2012-03-31', 'value': None}, {'date': '2012-04-30', 'value': None}, {'date': '2012-05-31', 'value': None}, {'date': '2012-06-30', 'value': None}, {'date': '2012-07-31', 'value': None}, {'date': '2012-08-31', 'value': None}, {'date': '2012-09-30', 'value': None}, {'date': '2012-10-31', 'value': None}, {'date': '2012-11-30', 'value': None}, {'date': '2012-12-31', 'value': None}, {'date': '2013-01-31', 'value': None}, {'date': '2013-02-28', 'value': None}, {'date': '2013-03-31', 'value': None}, {'date': '2013-04-30', 'value': None}, {'date': '2013-05-31', 'value': None}, {'date': '2013-06-30', 'value': None}, {'date': '2013-07-31', 'value': None}, {'date': '2013-08-31', 'value': None}, {'date': '2013-09-30', 'value': None}, {'date': '2013-10-31', 'value': None}, {'date': '2013-11-30', 'value': None}, {'date': '2013-12-31', 'value': None}, {'date': '2014-01-31', 'value': None}, {'date': '2014-02-28', 'value': None}, {'date': '2014-03-31', 'value': None}, {'date': '2014-04-30', 'value': None}, {'date': '2014-05-31', 'value': None}, {'date': '2014-06-30', 'value': None}, {'date': '2014-07-31', 'value': None}, {'date': '2014-08-31', 'value': None}, {'date': '2014-09-30', 'value': None}, {'date': '2014-10-31', 'value': None}, {'date': '2014-11-30', 'value': None}, {'date': '2014-12-31', 'value': None}, {'date': '2015-01-31', 'value': None}, {'date': '2015-02-28', 'value': None}, {'date': '2015-03-31', 'value': None}, {'date': '2015-04-30', 'value': None}, {'date': '2015-05-31', 'value': None}, {'date': '2015-06-30', 'value': None}, {'date': '2015-07-31', 'value': None}, {'date': '2015-08-31', 'value': None}, {'date': '2015-09-30', 'value': None}, {'date': '2015-10-31', 'value': None}, {'date': '2015-11-30', 
            'value': 48630399.0}, {'date': '2015-12-31', 'value': 3765439.109}, {'date': '2016-01-31', 'value': 737021.982}, {'date': '2016-02-29', 'value': 267563.172}, {'date': '2016-03-31', 'value': -27.23}, {'date': '2016-04-30', 'value': -225.991}, {'date': '2016-05-31', 'value': 518694.087}, {'date': '2016-06-30', 'value': -375.321}, {'date': '2016-07-31', 'value': -155566.429}, {'date': '2016-08-31', 'value': -2046068.549}, {'date': '2016-09-30', 'value': 76.584}, {'date': '2016-10-31', 'value': -131840.165}, {'date': '2016-11-30', 'value': 50203007.573}, {'date': '2016-12-31', 'value': -1106618.288}, {'date': '2017-01-31', 'value': -1741948.179}, {'date': '2017-02-28', 'value': -15147887.431}, {'date': '2017-03-31', 'value': -325340.919}, 
            {'date': '2017-04-30', 'value': -1740048.738}, {'date': '2017-05-31', 'value': -978733.815}, {'date': '2017-06-30', 'value': -828724.605}, {'date': '2017-07-31', 'value': -763861.351}, {'date': '2017-08-31', 'value': -441079.429}, {'date': '2017-09-30', 'value': -540261.843}, {'date': '2017-10-31', 'value': 3520175.706}, {'date': '2017-11-30', 'value': -1870539.415}, {'date': '2017-12-31', 'value': -383920.99}, {'date': '2018-01-31', 'value': 
            -299031.801}, {'date': '2018-02-28', 'value': -576103.866}, {'date': '2018-03-31', 'value': -573390.391}, {'date': '2018-04-30', 'value': -522944.419}, {'date': '2018-05-31', 'value': -177470.635}, {'date': '2018-06-30', 'value': -442087.242}, {'date': '2018-07-31', 'value': -2118869.424}, {'date': '2018-08-31', 'value': -694110.561}, {'date': '2018-09-30', 'value': -341543.879}, {'date': '2018-10-31', 'value': -3298754.921}, {'date': '2018-11-30', 'value': -660757.625}, {'date': '2018-12-31', 'value': -5073315.108}, {'date': '2019-01-31', 'value': -310942.617}, {'date': '2019-02-28', 'value': 203075.888}, {'date': '2019-03-31', 'value': -48072.4}, {'date': '2019-04-30', 'value': -1713109.393}, {'date': '2019-05-31', 'value': -538.882}, {'date': '2019-06-30', 'value': -2128228.298}, {'date': '2019-07-31', 'value': 621480.065}, {'date': '2019-08-31', 'value': -3554401.618}, {'date': '2019-09-30', 'value': -577611.075}, {'date': '2019-10-31', 'value': 1809467.086}, {'date': '2019-11-30', 'value': 2021381.118}, {'date': '2019-12-31', 'value': -462481.25}, {'date': '2020-01-31', 'value': 8948980.064}, {'date': '2020-02-29', 'value': -473518.553}, {'date': '2020-03-31', 'value': -12911183.873}, {'date': '2020-04-30', 'value': 95979.47}, {'date': '2020-05-31', 'value': 207469.043}, {'date': '2020-06-30', 'value': 12148.497}, 
            {'date': '2020-07-31', 'value': -210406.444}, {'date': '2020-08-31', 'value': -1249784.233}, {'date': '2020-09-30', 'value': 4185875.806}, {'date': '2020-10-31', 'value': -499536.716}, {'date': '2020-11-30', 'value': -5899545.264}, {'date': '2020-12-31', 'value': 2129634.067}, {'date': '2021-01-31', 'value': -730050.441}, {'date': '2021-02-28', 'value': -1187179.867}, {'date': '2021-03-31', 'value': -904151.514}, {'date': '2021-04-30', 'value': -414186.949}, {'date': '2021-05-31', 'value': -518585.344}, {'date': '2021-06-30', 'value': -1416051.521}, {'date': '2021-07-31', 'value': -492610.071}, {'date': '2021-08-31', 'value': -1367081.876}, {'date': '2021-09-30', 'value': -534512.876}, {'date': '2021-10-31', 'value': -591737.806}, {'date': '2021-11-30', 'value': -1096145.955}, {'date': '2021-12-31', 'value': -1314351.227}, {'date': '2022-01-31', 'value': -600583.288}, {'date': '2022-02-28', 'value': -407682.635}, {'date': '2022-03-31', 'value': -935479.076}, {'date': '2022-04-30', 'value': -456353.061}, {'date': '2022-05-31', 'value': -316697.295}, {'date': '2022-06-30', 'value': 3360672.82}, {'date': '2022-07-31', 'value': -172675.191}, {'date': '2022-08-31', 'value': -126619.454}, {'date': '2022-09-30', 'value': None}, {'date': '2022-10-31', 'value': None}, {'date': '2022-11-30', 'value': None}, {'date': '2022-12-31', 'value': None}], 'managerChange': [], 'table': {'columnDefs': ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', 'YTD'], 'growth10KReturnData': [{'label': 'fund', 'endDate': '2022-09-26T00:00:00.000', 'datum': [None, None, None, None, '-4.63415', '11.29288', '-15.55826', '22.27006', '-9.89025', '20.55363', '-18.53131'], 'epFlag': [False, False, False, False, False, False, False, False, False, False, False]}, {'label': 'category', 'endDate': '2022-09-26T00:00:00.000', 'datum': ['17.80595', '19.61344', '5.28444', '10.79321', '-0.34643', '10.178', '-12.8128', '24.58935', '-1.24863', '22.94787', '-19.89547'], 'epFlag': [False, False, False, False, False, False, False, False, False, False, False]}, {'label': 'index', 'endDate': '2022-09-26T00:00:00.000', 'datum': ['18.48241', '18.65813', '6.17978', '8.42815', '4.15203', '10.44776', '-9.61834', '27.39969', 
            '-3.03365', '27.33027', '-18.73191'], 'epFlag': [False, False, False, False, False, False, False, False, False, False, False]}, {'label': 'percentileRank', 'endDate': '2022-09-26T00:00:00.000', 'datum': [None, None, None, None, '88', '29', '80', '76', '96', '77', None], 'epFlag': [False, False, False, False, False, False, False, False, False, False, False]}, {'label': 'fundNumber', 'endDate': '2022-09-26T00:00:00.000', 'datum': ['1436', '1448', '1548', '1588', '1734', '1846', '1958', '2050', '1878', '1915', '746'], 'epFlag': [True, True, True, True, False, False, False, False, False, False, False]}, {'label': 'categoryName', 'endDate': None, 'datum': [None, None, None, 'EAA Fund Europe Large-Cap Blend Equity', 'EAA Fund Europe Large-Cap Blend Equity', 'EAA Fund Europe Large-Cap Blend Equity', 'EAA Fund Europe Large-Cap Blend Equity', 'EAA Fund Europe Large-Cap Blend Equity', 'EAA Fund Europe Large-Cap Blend Equity', 'EAA Fund Europe Large-Cap Blend Equity', 'EAA Fund Europe Large-Cap Blend Equity'], 'epFlag': []}, {'label': 'categoryNameAbbr', 'endDate': None, 'datum': [None, None, None, 'EU0511', 'EU0511', 'EU0511', 'EU0511', 'EU0511', 'EU0511', 'EU0511', 'EU0511'], 'epFlag': []}]}, 'currentValues': [{'type': 'fund', 'name': None, 'baseCurrency': 'EUR', 'currentValue': 9224.7, 'currentSymbol': '€'}, {'type': 'index', 'name': '', 'baseCurrency': 'EUR', 'currentValue': 12712.08831211816, 'currentSymbol': '€'}, {'type': 'category', 'name': '', 'baseCurrency': 'EUR', 'currentValue': 11251.033314798367, 'currentSymbol': '€'}], 'instrumentId': '52.8.FR0013028339', 'fundFlowQuarterlyData': [], 'isLimitAgeData': False, 'cur': 'EUR', 'isUKCefAvailable': False, 'template': 'SA_USA'}

        """
        
        #url
        url = f"""https://api-global.morningstar.com/sal-service/v1/{self.asset_type}/performance/v3/{self.code}"""
        #headers
        headers = {
            "apikey" : APIKEY,
        }

        response = requests.get(url, headers=headers)

        not_200_response(url,response)
        
        return json.loads(response.content.decode()) 


    def historicalExpenses(self):
        """        
        This function retrieves historical expenses of the funds.

        Returns:
            dict historical expenses

        Examples:
            >>> Funds("rmagx", "us").historicalExpenses()

            {'feeLevelComparisonGroup': 'Government Retirement, Large', 'currentYear': '2022', 'fundExpenseHistoryList': [{'annualReportDate': '2018-08-31T05:00:00.000', 'netExpenseRatio': 0.3, 'managementExpenseRatio': None}, {'annualReportDate': '2019-08-31T05:00:00.000', 'netExpenseRatio': 0.29, 'managementExpenseRatio': None}, {'annualReportDate': '2020-08-31T05:00:00.000', 'netExpenseRatio': 0.25, 'managementExpenseRatio': None}, {'annualReportDate': '2021-08-31T05:00:00.000', 'netExpenseRatio': 0.22, 'managementExpenseRatio': None}], 'feeLevelMedianList': [{'date': '2018-12-31T06:00:00.000', 'median': 0.46}, {'date': '2019-12-31T06:00:00.000', 'median': 0.47}, {'date': '2020-12-31T06:00:00.000', 'median': 0.455}, {'date': '2021-12-31T06:00:00.000', 'median': 0.44}, {'date': '2022-08-31T05:00:00.000', 'median': 0.44}], 'categoryExpenseAverageList': [{'year': '2022', 'categoryExpenseRatio': 0.709, 'categoryManagementExpenseRatio': None}, {'year': '2018', 'categoryExpenseRatio': 0.782, 'categoryManagementExpenseRatio': None}, {'year': '2019', 'categoryExpenseRatio': 0.785, 'categoryManagementExpenseRatio': None}, {'year': '2020', 'categoryExpenseRatio': 0.753, 'categoryManagementExpenseRatio': None}, {'year': '2021', 'categoryExpenseRatio': 0.706, 'categoryManagementExpenseRatio': None}]}
        
        """
        if self.asset_type == 'etf':
            return {}
        return self.GetFundsData("price/historicalExpenses")

    def holdings(self, holdingType: str = 'all'):
        """        
        This function retrieves holdings of the funds.

        Args:
            holdingType (str) : paramater to select the king of holdings, bonds, stocks, others or all

        Returns:
            pandas DataFrame holdings

        Raises:
            ValueError whenever the parameter is not all, bond, equity or other

        Examples:
            >>> Funds("myria", "fr").holdings("all")
            >>> Funds("myria", "fr").holdings("bond")
            >>> Funds("myria", "fr").holdings("equity")
            >>> Funds("myria", "fr").holdings("other")

                                       securityName       secId performanceId holdingTypeId  ...  qualRating  quantRating  bestRatingType  securityType
            0                             Nestle SA  0P0000A5EE    0P0000A5EE             E  ...           3            3            Qual            ST
            1                      Roche Holding AG  0P0000AZ48    0P0000AZ48             E  ...           5            4            Qual            ST
            2                       ASML Holding NV  0P0000ALDL    0P0000ALDL             E  ...           5            3            Qual            ST
            3                           Novartis AG  0P0000A5FH    0P0000A5FH             E  ...           4            4            Qual            ST
            4   LVMH Moet Hennessy Louis Vuitton SE  0P00009WL3    0P00009WL3             E  ...           2            3            Qual            ST

        """
        holdingType_to_holdingPage = {"all" : "all", "bond" : "boldHoldingPage","equity" : "equityHoldingPage", "other": "otherHoldingPage"}
        if holdingType not in holdingType_to_holdingPage:
            raise ValueError(f'parameter holdingType must take one of the following value : {", ".join(holdingType_to_holdingPage.keys())}  ')
    
        if holdingType == "all":
            return pd.DataFrame(self.position()["equityHoldingPage"]["holdingList"] + 
            self.position()["boldHoldingPage"]["holdingList"] + self.position()["otherHoldingPage"]["holdingList"] )
        else:
           return pd.DataFrame(self.position()[holdingType_to_holdingPage[holdingType]]["holdingList"])

    def indexAnnualPerformance(self):
        """
        This function retrieves the annual performance of the index.
  
        Returns:
            dict annual performance of the index


        Examples:
            >>> Funds("myria", "fr").indexAnnualPerformance()

            {'index_annual_performance_2016': '-7,21', 'index_annual_performance_2017': '1,05', 'index_annual_performance_2018': '-4,99', 'index_annual_performance_2019': 
            '-3,78', 'index_annual_performance_2020': '-6,57', 'index_annual_performance_2021': '-4,58', 'index_annual_performance_current': '-2,41'}

        """
        return self.AnnualPerformance('index')

    def indexCumulativePerformance(self):
        """
        This function retrieves the cumulative performance of the index.
  
        Returns:
            dict cumulative performance of the index


        Examples:
            >>> Funds("myria", "fr").indexCumulativePerformance()

            {'cumulative_performance_date': '26/09/2022', 'index_cumulative_performance_1 jour': '-0,42', 'index_cumulative_performance_1 semaine': '-0,71', 'index_cumulative_performance_1 mois': '1,49', 'index_cumulative_performance_3 mois': '0,55', 'index_cumulative_performance_6 mois': '0,89', "index_cumulative_performance_Début d'année": '-1,22', 'index_cumulative_performance_1 an': '-3,16', 'index_cumulative_performance_3 ans (annualisée)': '-4,73', 'index_cumulative_performance_5 ans (annualisée)': '-4,43', 'index_cumulative_performance_10 ans (annualisée)': '-'}
        
        """
        
        return self.CumulativePerformance('index')

    def marketCapitalization(self):
        """
        This function retrieves the marketCapitalization breakdown of the funds, category and index.
  
        Returns:
            dict market capitalization


        Examples:
            >>> Funds("myria", "fr").marketCapitalization()

            {'portfolioDate': '2022-08-31T05:00:00.000', 'assetType': 'EQUITY', 'currencyId': 'EUR', 'fund': {'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Myria Actions Durables Europe', 'avgMarketCap': 78534.26123, 'giant': 56.34528, 'large': 36.19509, 'medium': 5.2644, 'small': 0.10863, 'micro': 0.0}, 'category': {'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Europe Large-Cap Blend Equity', 'avgMarketCap': 46610.56573, 'giant': 39.27023, 'large': 35.83477, 'medium': 17.88083, 'small': 0.31315, 'micro': 0.01735}, 'index': {'portfolioDate': '2022-08-31T05:00:00.000', 'name': 'Morningstar Eur TME GR EUR', 'avgMarketCap': 47357.05144, 'giant': 41.94314, 'large': 41.62452, 'medium': 16.10521, 'small': 0.149, 'micro': 0.0}}
        
        """
        return self.GetFundsData("process/marketCap")


    def maturitySchedule(self):
        """
        This function retrieves the maturity breakdown of the funds and category.
  
        Returns:
            dict maturity

        Examples:
            >>> Funds("rmagx", "us").maturitySchedule()

            {'fund': {'date': '2022-06-30T05:00:00.000', 'name': 'American Funds Mortgage R6', 'schedule': ['7.59099', '1.75764', '2.86851', '4.15766', '1.58966', '4.93620', '58.45084', '10.67651']}, 'benchMark': None, 'category': {'date': '2022-08-31T05:00:00.000', 'name': 'Intermediate Government', 'schedule': ['3.16287', '4.43564', '14.33945', '36.00389', '0.71253', '1.90584', '37.50619', '5.14632']}, 'proxy': {'date': '2022-08-31T05:00:00.000', 'name': 'Morningstar US Trsy Bd TR USD', 'schedule': ['33.90583', '21.52942', '15.50681', '9.03698', '0.00000', '5.92073', '12.84950', '0.00000']}, 'scheduleLabel': ['Maturity1-3Yr%', 'Maturity3-5Yr%', 'Maturity5-7Yr%', 'Maturity7-10Yr%', 'Maturity10-15Yr%', 'Maturity15-20Yr%', 'Maturity20-30Yr%', 'Maturity30+Yr%']}
        
        """
        return self.GetFundsData("process/maturitySchedule")


    def maxDrawDown(self, year = 3):
        """
        This function retrieves the the max drawdown of the funds, index and category.
  
        Args:
            year (int) : period of calculation in year

        Returns:
            dict max drawdown

        Raises:
            TypeError whenever the parameter year is not an integer

        Examples:
            >>> Funds("myria", "fr").marketVolatilityMeasure()

            {'year': 3, 'maxDrawDownAsOfDate': '2022-08-31T05:00:00.000', 'fundName': 'Myria Actions Durables Europe', 'indexName': 'Morningstar Eur TME GR EUR', 'categoryName': 'Europe Large-Cap Blend Equity', 'peakDate': '2020-01-01T00:00:00.000', 'valleyDate': '2020-03-31T00:00:00.000', 'duration': 3.0, 'inceptionDate': '2015-11-25T06:00:00.000', 'calculationBenchmark': 'MSCI Europe NR EUR', 'cur': 'EUR', 'measureMap': {'fund': {'secId': 'F00000YIJ0', 'asOfDate': '2022-08-31T05:00:00.000', 'upside': 91.446, 'downside': 116.07, 'maxDrawDown': -23.9633902597, 'peakDate': '2020-01-01T00:00:00.000', 'valleyDate': '2020-03-31T00:00:00.000', 'duration': 3.0, 'isAddExtendedFlag': False}, 'index': {'secId': 'F000016V5C', 'asOfDate': '2022-08-31T05:00:00.000', 'upside': None, 'downside': None, 'maxDrawDown': -22.9713828113, 'peakDate': '2020-01-01T00:00:00.000', 'valleyDate': '2020-03-31T00:00:00.000', 'duration': 3.0, 'isAddExtendedFlag': False}, 'category': {'secId': 'EUCA000511', 'asOfDate': '2022-08-31T05:00:00.000', 'upside': 97.812, 'downside': 102.698, 'maxDrawDown': -22.2434389098, 'peakDate': '2020-01-01T00:00:00.000', 'valleyDate': '2020-03-31T00:00:00.000', 'duration': 3.0, 'isAddExtendedFlag': False}}}
        
        """

        if not isinstance(year, int):
            raise TypeError('year parameter should be an integer')


        return self.GetFundsData("performance/marketVolatilityMeasure", params = {"year": year})

    def morningstarAnalyst(self):
        """
        This function retrieves the raiting of MorningStar analyst.
  
        Returns:
            dict rating

        Examples:
            >>> Funds("rmagx", "us").morningstarAnalyst()

            {'morningstarRatingFor3Year': 5, 'morningstarRatingFor5Year': 5, 'morningstarRatingFor10Year': 5, 'overallMorningstarRating': 5, 'categoryMedalist': [{'secId': 'FOUSA00K5U', 'endDate': '2022-05-26 00:00:00.0', 'tradingSymbol': 'PDMIX', 'legalName': 'PIMCO GNMA and Government Securities Fund Institutional Class', 'name': 'PIMCO GNMA and Government Secs Instl', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -15.03372, 'trailing1YearReturn': -15.46618, 'trailing3YearReturn': -3.4169, 'trailing5YearReturn': -0.86364, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.52, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '1059402122', 'flow1Yr': -527446530.452, 'fundShareClassTypeId': '6', 'fundShareClassTypeName': 'Inst', 'lastShareClassNetAsset': 446272272.0, 'SecurityType': 'FO'}, {'secId': 'F00000JNX4', 'endDate': '2022-06-06 00:00:00.0', 'tradingSymbol': 'RMAGX', 'legalName': 'American Funds Mortgage Fund® Class R-6', 'name': 'American Funds Mortgage R6', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -12.13728, 'trailing1YearReturn': -12.08033, 'trailing3YearReturn': -1.99699, 'trailing5YearReturn': -0.19013, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.22, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '7933429876', 'flow1Yr': 200213581.41, 'fundShareClassTypeId': '12', 'fundShareClassTypeName': 'Retirement', 'lastShareClassNetAsset': 7426905998.0, 'SecurityType': 'FO'}, {'secId': 'FOUSA00B7H', 'endDate': '2021-11-12 00:00:00.0', 'tradingSymbol': 'AMUSX', 'legalName': 'American Funds U.S. Government Securities Fund® Class A', 'name': 'American Funds US Government Sec A', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -12.68602, 'trailing1YearReturn': -12.66343, 'trailing3YearReturn': -1.79101, 'trailing5YearReturn': -0.08197, 'ePUsedFor1YearReturn': 
            0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.62, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '17977215406', 'flow1Yr': -2113419313.058, 'fundShareClassTypeId': '1', 'fundShareClassTypeName': 'A', 'lastShareClassNetAsset': 3102501745.0, 'SecurityType': 'FO'}, {'secId': 'FOUSA00CFZ', 'endDate': '2022-09-21 00:00:00.0', 'tradingSymbol': 'FGMNX', 'legalName': 'Fidelity® GNMA Fund', 'name': 'Fidelity® GNMA', 'analystRating': '_PO_', 'overallMorningstarRating': '4', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -13.4398, 'trailing1YearReturn': -13.72737, 'trailing3YearReturn': -3.57772, 'trailing5YearReturn': -1.08504, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.45, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '2778044671', 'flow1Yr': -805981617.491, 'fundShareClassTypeId': '10', 'fundShareClassTypeName': 'No Load', 'lastShareClassNetAsset': 2778044671.0, 'SecurityType': 'FO'}, {'secId': 'FOUSA00CG4', 'endDate': '2022-09-18 00:00:00.0', 'tradingSymbol': 'FGOVX', 'legalName': 'Fidelity® Government Income Fund', 'name': 'Fidelity® Government Income', 'analystRating': '_PO_', 'overallMorningstarRating': '3', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -14.19508, 'trailing1YearReturn': -14.37134, 'trailing3YearReturn': -3.73601, 'trailing5YearReturn': -0.80501, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.45, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '3591886157', 'flow1Yr': 496561836.233, 'fundShareClassTypeId': '10', 'fundShareClassTypeName': 'No Load', 'lastShareClassNetAsset': 1753255679.0, 'SecurityType': 'FO'}, {'secId': 'FOUSA00D3M', 'endDate': '2022-09-26 00:00:00.0', 'tradingSymbol': 'HLGAX', 'legalName': 'JPMorgan Government Bond Fund Class I', 'name': 'JPMorgan Government Bond I', 'analystRating': '_PO_', 'overallMorningstarRating': '4', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -13.15349, 'trailing1YearReturn': -13.57978, 'trailing3YearReturn': -3.30534, 'trailing5YearReturn': -0.47438, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.48, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '1803448158', 'flow1Yr': -704337865.604, 'fundShareClassTypeId': '6', 'fundShareClassTypeName': 'Inst', 'lastShareClassNetAsset': 826667749.0, 'SecurityType': 'FO'}, {'secId': 'FOUSA00FQL', 'endDate': '2021-11-15 00:00:00.0', 'tradingSymbol': 'VFIIX', 'legalName': 'Vanguard GNMA Fund Investor Shares', 'name': 'Vanguard GNMA Inv', 'analystRating': '_PO_', 'overallMorningstarRating': '4', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -13.25766, 'trailing1YearReturn': -13.62469, 'trailing3YearReturn': -3.64936, 'trailing5YearReturn': -1.03881, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.21, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '18242421183', 'flow1Yr': -4179440264.604, 'fundShareClassTypeId': '7', 'fundShareClassTypeName': 'Inv', 'lastShareClassNetAsset': 5534183043.0, 'SecurityType': 'FO'}], 'topRated': [{'secId': 'FOUSA00K5U', 'endDate': '2022-05-26 00:00:00.0', 'tradingSymbol': 'PDMIX', 'legalName': 'PIMCO GNMA and Government Securities Fund Institutional Class', 'name': 'PIMCO GNMA and Government Secs Instl', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -15.03372, 'trailing1YearReturn': -15.46618, 'trailing3YearReturn': -3.4169, 'trailing5YearReturn': -0.86364, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.52, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '1059402122', 'flow1Yr': -527446530.452, 'fundShareClassTypeId': '6', 'fundShareClassTypeName': 'Inst', 'lastShareClassNetAsset': 446272272.0, 'SecurityType': 'FO'}, {'secId': 'F00000JNX4', 'endDate': '2022-06-06 00:00:00.0', 'tradingSymbol': 'RMAGX', 'legalName': 'American Funds Mortgage Fund® Class R-6', 'name': 'American Funds Mortgage R6', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -12.13728, 'trailing1YearReturn': -12.08033, 'trailing3YearReturn': -1.99699, 'trailing5YearReturn': -0.19013, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.22, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '7933429876', 'flow1Yr': 200213581.41, 'fundShareClassTypeId': '12', 'fundShareClassTypeName': 'Retirement', 'lastShareClassNetAsset': 7426905998.0, 
            'SecurityType': 'FO'}, {'secId': 'FOUSA00B7H', 'endDate': '2021-11-12 00:00:00.0', 'tradingSymbol': 'AMUSX', 'legalName': 'American Funds U.S. Government Securities Fund® Class A', 'name': 'American Funds US Government Sec A', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -12.68602, 'trailing1YearReturn': -12.66343, 'trailing3YearReturn': -1.79101, 'trailing5YearReturn': -0.08197, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.62, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '17977215406', 'flow1Yr': -2113419313.058, 'fundShareClassTypeId': '1', 'fundShareClassTypeName': 'A', 'lastShareClassNetAsset': 3102501745.0, 'SecurityType': 'FO'}], 'highestAsset': [{'secId': 'F00000JNX4', 'endDate': '2022-06-06 00:00:00.0', 'tradingSymbol': 'RMAGX', 'legalName': 'American Funds Mortgage Fund® Class R-6', 'name': 'American Funds Mortgage R6', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -12.13728, 'trailing1YearReturn': -12.08033, 'trailing3YearReturn': -1.99699, 'trailing5YearReturn': -0.19013, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.22, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '7933429876', 'flow1Yr': 200213581.41, 'fundShareClassTypeId': '12', 'fundShareClassTypeName': 'Retirement', 
            'lastShareClassNetAsset': 7426905998.0, 'SecurityType': 'FO'}, {'secId': 'FOUSA00FQL', 'endDate': '2021-11-15 00:00:00.0', 'tradingSymbol': 'VFIIX', 'legalName': 'Vanguard GNMA Fund Investor Shares', 'name': 'Vanguard GNMA Inv', 'analystRating': '_PO_', 'overallMorningstarRating': '4', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -13.25766, 'trailing1YearReturn': -13.62469, 'trailing3YearReturn': -3.64936, 'trailing5YearReturn': -1.03881, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.21, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '18242421183', 'flow1Yr': -4179440264.604, 'fundShareClassTypeId': '7', 'fundShareClassTypeName': 'Inv', 'lastShareClassNetAsset': 5534183043.0, 'SecurityType': 'FO'}, {'secId': 'FOUSA00B7H', 'endDate': '2021-11-12 00:00:00.0', 'tradingSymbol': 'AMUSX', 'legalName': 'American Funds U.S. Government Securities Fund® Class A', 'name': 'American Funds US Government Sec A', 'analystRating': '_PO_', 'overallMorningstarRating': '5', 'ePUsedForOverallRating': None, 'trailingYearToDateReturn': -12.68602, 'trailing1YearReturn': -12.66343, 'trailing3YearReturn': -1.79101, 'trailing5YearReturn': -0.08197, 'ePUsedFor1YearReturn': 0.0, 'ePUsedFor5YearReturn': 0.0, 'ePUsedFor3YearReturn': 0.0, 'expenseRatio': 0.62, 'managementExpenseRatio': None, 'ongoingCharge': None, 'baseCurrencyId': 'USD', 'tNAInShareClassCurrency': '17977215406', 'flow1Yr': -2113419313.058, 'fundShareClassTypeId': '1', 'fundShareClassTypeName': 'A', 'lastShareClassNetAsset': 3102501745.0, 'SecurityType': 'FO'}], 'analystRating': '_PO_', 'analystRatingDate': '2022-06-06 00:00:00.0', 'morningstarRatingDate': '2022-08-31 00:00:00.0', 'history': [{'date': '2019-09-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2019-10-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2019-11-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2019-12-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-01-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-02-29T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-03-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-04-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-05-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-06-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-07-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-08-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-09-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-10-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-11-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2020-12-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-01-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-02-28T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-03-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-04-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-05-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-06-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-07-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-08-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-09-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-10-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-11-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2021-12-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-01-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-02-28T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-03-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-04-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-05-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-06-30T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-07-31T00:00:00.000', 'rating': '_PO_'}, {'date': '2022-08-31T00:00:00.000', 'rating': '_PO_'}], 'userType': 'Free', 'flagshipShareClassID': 
            None, 'flagshipName': None, 'isAusFlagship': False, 'quantHistory': [{'endDate': '2017-06-30T05:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 0.5, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2017-07-24T16:58:00.000'}, {'endDate': '2017-07-31T05:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 1.0, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2017-08-21T17:35:00.000'}, {'endDate': '2017-08-31T05:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 1.0, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2017-09-22T17:34:00.000'}, {'endDate': '2017-09-30T05:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 1.0, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2017-10-20T17:38:00.000'}, {'endDate': '2017-10-31T05:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 1.0, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2017-11-21T03:39:00.000'}, {'endDate': '2017-11-30T06:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 1.0, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2017-12-21T22:17:00.000'}, {'endDate': '2017-12-31T06:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 0.5, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2018-01-25T01:08:00.000'}, {'endDate': '2018-01-31T06:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 'price': 0.5, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2018-02-22T17:41:00.000'}, {'endDate': '2018-02-28T06:00:00.000', 'parent': 1.0, 'people': 0.5, 'performance': 1.0, 
            'price': 0.5, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2018-03-21T16:36:00.000'}, {'endDate': '2018-03-31T05:00:00.000', 'parent': 1.0, 'people': 0.5, 
            'performance': 1.0, 'price': 0.5, 'process': 1.0, 'quantRating': 5, 'lastUpdate': '2018-04-20T16:56:00.000'}], 'quantRating': None, 'quantRatingDate': None}
                    
        """

        return self.GetFundsData("morningstarAnalyst")

    def multiLevelFixedIncomeData(self, primary = "superEffectiveDuration", secondary = "superSector.weight"):
        """
        This function retrieves the exposures of fixed income

        Args:
            primary (str) : can be superEffectiveDuration, superYieldToWorst, creditQuality
            secondary (str) : can be superSector.weight, region.weight, creditQuality.weight

        Returns:
            dict exposures

        Raises:
            ValueError whenever the primary and seconday paramater is not a value expected

        Examples:
            >>> Funds("rmagx", "us").multiLevelFixedIncomeData()

            {'fundName': 'American Funds Mortgage R6', 'assetType': 'FIXEDINCOME', 'asOfDate': '2022-06-30T00:00:00.000', 'primary': 'superEffectiveDuration', 'secondary': 'superSector', 'data': [{'secondaryAttributeName': 'Government', 'weight': 40.61405, 'primaryData': {'Negative': None, '0 to 1%': 34.07425, '1 to 3%': 1.19957, '3 to 5%': 1.00176, '5 to 7%': 2.52617, '7 to 10%': 0.22344, '10 to 20%': 0.80488, 'Greater than 20%': 0.78399, 'Unknown': None, 'Not Applicable': None, 'weight': 40.61405}}, {'secondaryAttributeName': 'Municipal', 'weight': None, 'primaryData': {'Negative': None, '0 to 1%': 
            None, '1 to 3%': None, '3 to 5%': None, '5 to 7%': None, '7 to 10%': None, '10 to 20%': None, 'Greater than 20%': None, 'Unknown': None, 'Not Applicable': None, 'weight': None}}, {'secondaryAttributeName': 'Corporate', 'weight': None, 'primaryData': {'Negative': None, '0 to 1%': None, '1 to 3%': None, '3 to 5%': None, '5 to 7%': None, '7 to 10%': None, '10 to 20%': None, 'Greater than 20%': None, 'Unknown': None, 'Not Applicable': None, 'weight': None}}, {'secondaryAttributeName': 'Securitized', 'weight': 50.40543, 'primaryData': {'Negative': 0.57848, '0 to 1%': 0.51714, '1 to 3%': 6.98837, '3 to 5%': 22.50464, '5 to 7%': 14.26127, '7 to 10%': 1.76286, '10 to 20%': None, 'Greater than 20%': None, 'Unknown': 3.79266, 'Not Applicable': None, 'weight': 50.40543}}, {'secondaryAttributeName': 'Derivatives', 'weight': None, 'primaryData': {'Negative': None, '0 to 1%': None, '1 to 3%': None, '3 to 5%': None, '5 to 7%': None, '7 to 10%': None, '10 to 20%': None, 'Greater than 20%': None, 'Unknown': None, 'Not Applicable': None, 'weight': None}}, {'secondaryAttributeName': 'Cash & Equivalents', 'weight': 8.8348, 'primaryData': {'Negative': None, '0 to 1%': 8.8348, '1 to 3%': None, '3 to 5%': None, '5 to 7%': None, '7 to 10%': None, '10 to 20%': None, 'Greater than 20%': None, 'Unknown': None, 'Not Applicable': None, 'weight': 8.8348}}, {'secondaryAttributeName': 'Unknown', 'weight': 0.14573, 'primaryData': {'Negative': None, '0 to 1%': None, '1 to 3%': None, '3 to 5%': None, '5 to 7%': None, '7 to 10%': None, '10 to 20%': None, 'Greater than 20%': None, 'Unknown': 0.14573, 'Not Applicable': None, 'weight': 0.14573}}]}

        
        """

        primary_choice = ["superEffectiveDuration","superYieldToWorst", "creditQuality"]
        secondary_choice = ["superSector.weight", "region.weight", "creditQuality.weight"]

        if primary not in primary_choice:
            raise ValueError(f'primary parameter can only take one of the values: {", ".join(primary_choice)}')
        
        if secondary not in secondary_choice:
            raise ValueError(f'secondary parameter can only take one of the values: {", ".join(secondary_choice)}')

        if primary == "creditQuality" and secondary == "creditQuality.weight":
            raise ValueError(f'primary and secondary parameters cannot be both credit quality')

        return self.GetFundsData("multiLevelFixedIncomeData", params = {"primary": primary,"secondary": secondary})

    def nav(self, start_date,end_date,frequency="daily"):
        """
        This function retrieves the NAV of the funds

        Returns:
            list of dict with nav

            >>> Funds("RMAGX", "us").nav()

            [{
                "nav": 376.35,
                "totalReturn": 575.01685,
                "date": "2023-01-31"
            },
            {
                "nav": 380.28,
                "totalReturn": 581.02141,
                "date": "2023-02-01"
            }]

        Raises:
            TypeError: raised whenever the parameter type is not the type expected
            ValueError : raised whenever the parameter is not valid or no funds found
        """
        #error raised if start_date is note a datetime.date
        if not isinstance(start_date,datetime.date):
            raise TypeError("start_date parameter should be a datetime.date")

        #error raised if end_date is note a datetime.date
        if not isinstance(end_date,datetime.date):
            raise TypeError("end_date parameter should be a datetime.date")

        #error if end_date < start_date
        if end_date < start_date:
            raise ValueError("end_date must be more recent than start_date")

        #dict of frequency
        frequency_row = {'daily' : 'd','weekly' : 'w', 'monthly' : 'm'}

        #raise an error if frequency is not daily, wekly or monthly
        if frequency not in frequency_row:
            raise ValueError(f"frequency parameter must take one of the following value : { ', '.join(frequency_row.keys())}")
        
        #bearer token
        bearer_token = token_chart()
        #url for nav
        url =f"https://www.us-api.morningstar.com/QS-markets/chartservice/v2/timeseries?query={self.code}:nav,totalReturn&frequency={frequency_row[frequency]}&startDate={start_date.strftime('%Y-%m-%d')}&endDate={end_date.strftime('%Y-%m-%d')}&trackMarketData=3.6.3&instid=MSERP"
        #header with bearer token
        headers = {
                    'user-agent' : random_user_agent(), 
                    'authorization': f'Bearer {bearer_token}',
                    }
        #response
        response = requests.get(url, headers=headers)
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
            
        



    def objectiveInvestment(self):
        """        
        This function retrieves the objective of investment of the fund (by scraping pages);

        Returns:
            str objective investment

        Examples:
            >>> Funds("myria", "fr").objectiveInvestment()

            L'objectif de gestion du FCP est d'offrir un portefeuille composé de valeurs cotées sur les marchés des pays membres de l'Union Européenne à des souscripteurs 
            qui souhaitent investir sur les marchés d'actions européens. L'action du gérant vise à obtenir, sur la période de placement recommandée, une performance supérieure à celle de l'indice STOXX Europe ex UK Large® (dividendes réinvestis) représentatif de l'évolution des principales valeurs boursières de l'Union Européenne et de la Suisse, en sélectionnant des titres dans un univers restreint grâce à un filtre extra-financier fondé sur des critères quantitatifs de Gouvernance, 
            de Responsabilité sociale et sociétale, et de respect de l'environnement.
            Bien que nommé « Myria Actions Durables Europe », le fonds ne bénéficie pas du label ISR.
        """
        
        no_site_error(self.code,self.name,self.country,self.site)
        #headers random agent
        headers = {'user-agent' : random_user_agent()}
        #Page 1 - overview
        #url page overview
        url = f"{self.site}funds/snapshot/snapshot.aspx?id={self.code}"
        #get HTML page overview
        response = requests.get(url, headers=headers)
        #if page not found

        not_200_response(url,response)
        #html page as soup
        soup = BeautifulSoup(response.text, 'html.parser')
        #investment objective funds
        return soup.find(id='overviewObjectiveDiv').find('td', {"class": "value text"}).text

    def otherFee(self):
        """
        This function retrieves the other fee of the etf

        Returns:
            dict fees

        Examples:
            >>> Funds("American Century Foc Dynmc Gr ETF").otherFee()
            
            {'expenseWaiver': False, 'expenseReimbursement': None, 'expirationDate': None, 'expenseWaivers': None}
                    
        """
        return self.GetFundsData("price/otherFee")


    def ownershipZone(self):
        """        
        This function retrieves ownershipZone of the funds, index and category.

        Returns:
            dict ownershipZone

        Examples:
            >>> Funds("myria", "fr").ownershipZone()

            {'portfolioDate': '2022-08-31T05:00:00.000', 'fund': {'portfolioDate': '2022-08-31T05:00:00.000', 'scaledSizeScore': 313.034, 'scaledStyleScore': 146.716, 'sizeVariance': 60.703, 'styleVariance': 129.764, 'rho': 0.231, 'secId': 'F00000YIJ0', 'name': 'Myria Actions Durables Europe', 'objectZone75Percentile': 2.477}, 'benchmark': {'portfolioDate': '2022-08-31T05:00:00.000', 'scaledSizeScore': 279.883, 'scaledStyleScore': 133.831, 'sizeVariance': 73.359, 'styleVariance': 130.45, 'rho': 0.145, 'secId': 'F000016V5C', 'name': 'Morningstar Eur TME GR EUR', 'objectZone75Percentile': 3.04}, 'category': {'portfolioDate': '2022-08-31T05:00:00.000', 'scaledSizeScore': 279.493, 'scaledStyleScore': 147.115, 'sizeVariance': 75.69, 'styleVariance': 125.886, 'rho': 0.151, 'secId': 'EUCA000511', 'name': 'Europe Large-Cap Blend Equity', 'objectZone75Percentile': 2.804}}
        """

        return self.GetFundsData("process/ownershipZone")

    def parentMstarRating(self):

        """
        This function retrieves the raiting of parent by MorningStar analyst.
  
        Returns:
            list of dict rating

        Examples:
            >>> Funds("rmagx", "us").parentMstarRating()

            [{'naPercentage': 0.0001618873, 'mstarRating': '1'}, {'naPercentage': 0.0486402178, 'mstarRating': '2'}, {'naPercentage': 0.4050766321, 'mstarRating': '3'}, {'naPercentage': 0.3224827296, 'mstarRating': '4'}, {'naPercentage': 0.2236385332, 'mstarRating': '5'}, {'naPercentage': 0.0, 'mstarRating': 'Not Rated'}]
        
        """


        return self.GetFundsData("parent/parentMstarRating")

    def parentSummary(self):
        """
        This function retrieves info about the parent.
  
        Returns:
            dict parent info

        Examples:
            >>> Funds("rmagx", "us").parentSummary()

            {'secId': 'F00000JNX4', 'fundId': 'FSUSA0B07G', 'companyId': '0C00001YPH', 'marketName': 'US Open-end ex MM ex FoF ex Feeder', 'firmName': 'American Funds', 'currency': 'USD', 'netAsset': 1908002314120.0, 'netFlowTTM': -21913764984.0, 'netAssetTTM': 2307099660250.0, 'assetGrowthRate': -0.0094984041, 'numFund': 38, 'managerRetention5Year': 96.0}
        
        """
        return self.GetFundsData("parent/parentSummary")

    def people(self):
        """
        This function retrieves info about people who works in the company.
  
        Returns:
            dict people info

        Examples:
            >>> Funds("rmagx", "us").people()

            {'inceptionDate': '2010-11-01T05:00:00.000', 'averageManagerTenure': 7.94, 'longestManagerTenure': 11.92, 'advisorType': 'Capital Research and Management Company', 'subadvised': '0', 'managerCount': 3, 'womenOnTeams': None, 'advisorList': [{'advisorId': '0C00001DKF', 'advisorDisplayName': 'Capital Research and Management Company', 'regionId': None, 'languageId': None, 'subAdvisorId': None, 'subAdvisorName': None}], 'subAdvisorList': [], 'currentManagerList': [{'personId': 
            '147767', 'familyName': 'MacDonald', 'middleName': 'N.', 'givenName': 'Fergus', 'startDate': '2010-11-01T05:00:00.000', 'ownershipLevelId': '7', 'endDate': None, 'gender': 'male', 'genderSourceType': 'reported'}, {'personId': '173796', 'familyName': 'Betanzos', 'middleName': 'J.', 'givenName': 'David', 'startDate': '2013-11-01T05:00:00.000', 'ownershipLevelId': '6', 'endDate': None, 'gender': 'male', 'genderSourceType': 'reported'}, {'personId': '200392', 'familyName': 'Edmonds', 'middleName': 'V.', 'givenName': 'Oliver', 'startDate': '2019-10-30T05:00:00.000', 'ownershipLevelId': '5', 'endDate': None, 'gender': None, 'genderSourceType': 'reported'}], 'pastManagerList': [{'personId': '107716', 'familyName': 'Phoa', 'middleName': 'K.-S.', 'givenName': 'Wesley', 'startDate': '2010-11-01T05:00:00.000', 'ownershipLevelId': '5', 'endDate': '2013-11-01T05:00:00.000', 'gender': 'male', 'genderSourceType': 'reported'}, {'personId': '84745', 'familyName': 'Adams', 'middleName': None, 'givenName': 'Kevin', 'startDate': '2011-11-01T05:00:00.000', 'ownershipLevelId': '1', 'endDate': '2013-11-01T05:00:00.000', 'gender': 'male', 'genderSourceType': 'reported'}], 'lastTurnoverRatio': 10.15, 'longestTenureStartDate': '2010-11-01'}
        
        """
        return self.GetFundsData("people")

    def position(self):

        """
        This function retrieves the hodings of the funds.
  
        Returns:
            dict holdings

        Examples:
            >>> Funds("myria", "fr").position()

            {'masterPortfolioId': '2852268', 'secId': 'F00000YIJ0', 'baseCurrencyId': 'EUR', 'domicileCountryId': 'FRA', 'numberOfHolding': 77, 'numberOfEquityHolding': 65, 'numberOfBondHolding': 0, 'numberOfOtherHolding': 12, 'topNCount': 0, 'portfolioSuppression': '0', 'assetType': 'EQUITY', 'holdingSummary': {'portfolioDate': '2022-08-31T05:00:00.000', 'topHoldingWeighting': 37.22957, 'equityNumberOfHolding': 65, 'fixedIncomeNumberOfHolding': 0, 'numberOfHolding': 77, 'numberOfOtherHolding': 12, 'lastTurnover': None, 'LastTurnoverDate': None, 'secId': 'F00000YIJ0', 'averageTurnoverRatio': None, 'womenDirectors': 38.8822557, 'womenExecutives': 14.7704398}, 'holdingActiveShare': {'activeShareValue': 59.58997, 'activeShareDate': '2022-08-31T05:00:00.000', 'etfBenchmarkProxyName': 'iShares Core MSCI Europe UCITS ETF'}, 'equityHoldingPage': {'pageSize': 25, 'pageNumber': 1, 'totalPage': 1, 'numberOfCurPageHolding': 24, 'numberOfAllHolding': 24, 'holdingList': [{'securityName': 'Nestle SA', 'secId': '0P0000A5EE', 'performanceId': '0P0000A5EE', 'holdingTypeId': 'E', 'weighting': 6.64513, 'numberOfShare': 26118.0, 'marketValue': 3052615.0, 'shareChange': 0.0, 'country': 'Switzerland', 'ticker': None, 'totalReturn1Year': -3.3718, 'forwardPERatio': 21.2766, 'stockRating': '3', 'economicMoat': 'Wide  ', 'sector': 'Consumer Defensive', 'sectorCode': 'consumerDefensive', 'holdingTrend': {'trend': [2735806.0, 2938631.0, 3131976.0, 3052615.0]}, 'holdingType': 'Equity', 'isin': 'CH0038863350', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Swiss Franc', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 24.1311, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '3', 'quantRating': '3', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Roche Holding AG', 'secId': '0P0000AZ48', 'performanceId': '0P0000AZ48', 'holdingTypeId': 'E', 'weighting': 4.84293, 'numberOfShare': 6915.0, 'marketValue': 2224729.0, 'shareChange': 0.0, 'country': 'Switzerland', 'ticker': None, 'totalReturn1Year': -3.6424, 'forwardPERatio': 15.949, 'stockRating': '5', 'economicMoat': 'Wide  ', 'sector': 'Healthcare', 'sectorCode': 'healthcare', 'holdingTrend': {'trend': [1973176.0, 2160459.0, 2246106.0, 2224729.0]}, 'holdingType': 'Equity', 'isin': 'CH0012032048', 'cusip': None, 'secondarySectorId': '304006', 'superSectorName': 'corporate', 'primarySectorName': 'Preferred', 'secondarySectorName': 'Health-Care', 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Swiss Franc', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 23.5296, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '5', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'ASML Holding NV', 'secId': '0P0000ALDL', 'performanceId': '0P0000ALDL', 'holdingTypeId': 'E', 'weighting': 4.15044, 'numberOfShare': 3934.0, 'marketValue': 1906613.0, 'shareChange': -258.0, 'country': 'Netherlands', 'ticker': None, 'totalReturn1Year': -31.8789, 'forwardPERatio': 21.9298, 'stockRating': '5', 'economicMoat': 'Wide  ', 'sector': 'Technology', 'sectorCode': 'technology', 'holdingTrend': {'trend': [2036800.0, 1921741.0, 2328237.0, 1906613.0]}, 'holdingType': 'Equity', 'isin': 'NL0010273215', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 10.9124, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '5', 'quantRating': '3', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Novartis AG', 'secId': '0P0000A5FH', 'performanceId': '0P0000A5FH', 'holdingTypeId': 'E', 'weighting': 3.89021, 'numberOfShare': 22140.0, 'marketValue': 1787072.0, 'shareChange': 0.0, 'country': 'Switzerland', 'ticker': None, 'totalReturn1Year': 0.9306, 'forwardPERatio': 11.534, 'stockRating': '4', 'economicMoat': 'Wide  ', 'sector': 'Healthcare', 'sectorCode': 'healthcare', 'holdingTrend': {'trend': [1667258.0, 1742474.0, 1863070.0, 1787072.0]}, 'holdingType': 'Equity', 'isin': 'CH0012005267', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Swiss Franc', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 
            'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 17.2337, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '4', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'LVMH Moet Hennessy Louis Vuitton SE', 'secId': '0P00009WL3', 'performanceId': '0P00009WL3', 'holdingTypeId': 'E', 'weighting': 3.67462, 'numberOfShare': 2607.0, 'marketValue': 1688032.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': 0.0484, 'forwardPERatio': 19.3424, 'stockRating': '2', 'economicMoat': 'Wide  ', 'sector': 'Consumer Cyclical', 'sectorCode': 'consumerCyclical', 'holdingTrend': {'trend': [1411184.0, 1513141.0, 1759725.0, 1688032.0]}, 'holdingType': 'Equity', 'isin': 'FR0000121014', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 12.383, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '2', 'quantRating': '3', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Novo Nordisk A/S Class B', 'secId': '0P0000A5BQ', 'performanceId': '0P0000A5BQ', 'holdingTypeId': 'E', 'weighting': 3.49925, 'numberOfShare': 15086.0, 'marketValue': 1607472.0, 'shareChange': 0.0, 'country': 'Denmark', 'ticker': None, 'totalReturn1Year': 23.8396, 'forwardPERatio': 25.8398, 'stockRating': '3', 'economicMoat': 'Wide  ', 'sector': 'Healthcare', 'sectorCode': 'healthcare', 'holdingTrend': {'trend': [1325902.0, 1480639.0, 1730355.0, 1607472.0]}, 'holdingType': 'Equity', 'isin': 'DK0060534915', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Danish Krone', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 24.0231, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '3', 'quantRating': '3', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'TotalEnergies SE', 'secId': '0P00009WRK', 'performanceId': '0P00009WRK', 'holdingTypeId': 'E', 'weighting': 3.47201, 'numberOfShare': 31465.0, 'marketValue': 1594961.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': 23.2491, 'forwardPERatio': 3.9683, 'stockRating': '4', 'economicMoat': 'None  ', 'sector': 'Energy', 'sectorCode': 'energy', 'holdingTrend': {'trend': [1139595.0, 1579760.0, 1565698.0, 1594961.0]}, 'holdingType': 'Equity', 'isin': 'FR0000120271', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 29.1491, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '4', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Linde PLC', 'secId': '0P000004FA', 'performanceId': '0P000004FA', 'holdingTypeId': 'E', 'weighting': 3.16921, 'numberOfShare': 5181.0, 'marketValue': 1455861.0, 'shareChange': 0.0, 'country': 'United Kingdom', 'ticker': None, 'totalReturn1Year': -6.5512, 'forwardPERatio': 20.6612, 'stockRating': '4', 'economicMoat': 'Narrow', 'sector': 'Basic Materials', 
            'sectorCode': 'basicMaterials', 'holdingTrend': {'trend': [1415374.0, 1408725.0, 1530467.0, 1455861.0]}, 'holdingType': 'Equity', 'isin': 'IE00BZ12WP82', 'cusip': 'G5494J103', 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'US Dollar', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 8.2081, 'susEsgRiskGlobes': 5, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Negligible', 'qualRating': '4', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Deutsche Telekom AG', 'secId': '0P00009QP1', 'performanceId': '0P00009QP1', 'holdingTypeId': 'E', 'weighting': 1.98012, 'numberOfShare': 48415.0, 'marketValue': 909621.0, 'shareChange': 0.0, 'country': 'Germany', 'ticker': None, 'totalReturn1Year': 4.2309, 'forwardPERatio': 10.6045, 'stockRating': '4', 'economicMoat': 'Narrow', 'sector': 'Communication Services', 'sectorCode': 'communicationsServices', 'holdingTrend': {'trend': [764960.0, 753252.0, 895968.0, 909621.0]}, 'holdingType': 'Equity', 'isin': 'DE0005557508', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-04-30T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 16.2964, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '4', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Schneider Electric SE', 'secId': '0P00009WP6', 'performanceId': '0P00009WP6', 'holdingTypeId': 'E', 'weighting': 1.90565, 'numberOfShare': 7370.0, 'marketValue': 875409.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -16.7199, 'forwardPERatio': 14.7275, 'stockRating': '4', 'economicMoat': 'Wide  ', 'sector': 'Industrials', 'sectorCode': 'industrials', 'holdingTrend': {'trend': [861987.0, 839051.0, 991560.0, 875409.0]}, 'holdingType': 'Equity', 'isin': 'FR0000121972', 'cusip': None, 
            'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 17.4769, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '4', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Sanofi SA', 'secId': '0P00009WOZ', 'performanceId': '0P00009WOZ', 
            'holdingTypeId': 'E', 'weighting': 1.89628, 'numberOfShare': 10600.0, 'marketValue': 871108.0, 'shareChange': -1538.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -1.6249, 'forwardPERatio': 9.3633, 'stockRating': '4', 'economicMoat': 'Wide  ', 'sector': 'Healthcare', 'sectorCode': 'healthcare', 'holdingTrend': {'trend': [1093180.0, 1206424.0, 1179935.0, 871108.0]}, 'holdingType': 'Equity', 'isin': 'FR0000120578', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 22.3299, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '4', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Iberdrola SA', 'secId': '0P0000A4Z3', 'performanceId': '0P0000A4Z3', 'holdingTypeId': 'E', 'weighting': 1.89533, 'numberOfShare': 83839.0, 'marketValue': 870668.0, 'shareChange': 2233.0, 'country': 'Spain', 'ticker': None, 'totalReturn1Year': 14.5289, 'forwardPERatio': 12.87, 'stockRating': '3', 'economicMoat': 'None  ', 'sector': 'Utilities', 'sectorCode': 'utilities', 'holdingTrend': {'trend': [690614.0, 685513.0, 851151.0, 870668.0]}, 'holdingType': 'Equity', 'isin': 'ES0144580Y14', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 20.4847, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '3', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Zurich Insurance Group AG', 'secId': '0P0000A5GW', 'performanceId': '0P0000A5GW', 'holdingTypeId': 'E', 'weighting': 1.88544, 'numberOfShare': 1956.0, 'marketValue': 866128.0, 'shareChange': 0.0, 'country': 'Switzerland', 'ticker': None, 'totalReturn1Year': 6.8502, 'forwardPERatio': 10.2881, 'stockRating': '4', 'economicMoat': 'Narrow', 'sector': 'Financial Services', 'sectorCode': 'financialService', 'holdingTrend': {'trend': [767363.0, 818043.0, 835773.0, 866128.0]}, 'holdingType': 'Equity', 'isin': 'CH0011075394', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Swiss Franc', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 18.0607, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '4', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Airbus SE', 'secId': '0P00009WFE', 'performanceId': '0P00009WFE', 'holdingTypeId': 'E', 'weighting': 1.87245, 'numberOfShare': 
            8787.0, 'marketValue': 860159.0, 'shareChange': 0.0, 'country': 'Netherlands', 'ticker': None, 'totalReturn1Year': -21.4683, 'forwardPERatio': 14.5985, 'stockRating': '4', 'economicMoat': 'Wide  ', 'sector': 'Industrials', 'sectorCode': 'industrials', 'holdingTrend': {'trend': [866324.0, 798354.0, 921581.0, 860159.0]}, 'holdingType': 'Equity', 'isin': 'NL0000235190', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 26.782, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '4', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Air Liquide SA', 'secId': '0P00009WA4', 'performanceId': '0P00009WA4', 'holdingTypeId': 'E', 'weighting': 1.83967, 'numberOfShare': 6750.0, 'marketValue': 845100.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -4.5923, 'forwardPERatio': 18.4162, 'stockRating': '4', 'economicMoat': 'Narrow', 'sector': 'Basic Materials', 'sectorCode': 'basicMaterials', 'holdingTrend': {'trend': [905716.0, 877001.0, 905310.0, 845100.0]}, 'holdingType': 'Equity', 'isin': 'FR0000120073', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 13.6225, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '4', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Vinci SA', 'secId': '0P00009WSC', 'performanceId': '0P00009WSC', 'holdingTypeId': 'E', 'weighting': 1.83445, 'numberOfShare': 9135.0, 'marketValue': 842704.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -4.5258, 'forwardPERatio': 10.7991, 'stockRating': '4', 'economicMoat': 'Narrow', 'sector': 'Industrials', 'sectorCode': 'industrials', 'holdingTrend': {'trend': [657892.0, 689997.0, 853026.0, 842704.0]}, 'holdingType': 'Equity', 'isin': 'FR0000125486', 'cusip': 
            None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 27.05, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '4', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'AXA SA', 'secId': '0P00009WBE', 'performanceId': '0P00009WBE', 'holdingTypeId': 'E', 'weighting': 1.82402, 'numberOfShare': 35618.0, 'marketValue': 837913.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -0.2906, 'forwardPERatio': 7.0671, 'stockRating': '4', 'economicMoat': 'None  ', 'sector': 'Financial Services', 'sectorCode': 'financialService', 'holdingTrend': {'trend': [758856.0, 772024.0, 799624.0, 837913.0]}, 'holdingType': 'Equity', 'isin': 'FR0000120628', 'cusip': None, 'secondarySectorId': 
            None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 16.9831, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '4', 'quantRating': 
            '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'BNP Paribas Act. Cat.A', 'secId': '0P00009WC0', 'performanceId': '0P00009WC0', 'holdingTypeId': 'E', 'weighting': 1.80182, 'numberOfShare': 17806.0, 'marketValue': 827712.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -14.7276, 'forwardPERatio': 5.4496, 'stockRating': '4', 'economicMoat': 'None  ', 'sector': 'Financial Services', 'sectorCode': 'financialService', 'holdingTrend': {'trend': [979136.0, 943624.0, 819076.0, 827712.0]}, 'holdingType': 'Equity', 'isin': 'FR0000131104', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 25.049, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '4', 'quantRating': '4', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'SAP SE', 'secId': '0P00009QRW', 'performanceId': '0P00009QRW', 'holdingTypeId': 'E', 'weighting': 1.78302, 'numberOfShare': 9643.0, 'marketValue': 819076.0, 'shareChange': 0.0, 'country': 'Germany', 'ticker': None, 'totalReturn1Year': -26.4854, 'forwardPERatio': 13.6612, 'stockRating': '5', 'economicMoat': 'Narrow', 'sector': 'Technology', 'sectorCode': 'technology', 'holdingTrend': {'trend': [810892.0, 856705.0, 874427.0, 819076.0]}, 'holdingType': 'Equity', 'isin': 'DE0007164600', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 
            'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 10.7574, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '5', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Mercedes-Benz Group AG', 'secId': '0P00009QOM', 'performanceId': '0P00009QOM', 'holdingTypeId': 'E', 'weighting': 1.63506, 'numberOfShare': 13384.0, 'marketValue': 751110.0, 'shareChange': 0.0, 'country': 'Germany', 'ticker': None, 'totalReturn1Year': -11.4165, 'forwardPERatio': 4.662, 'stockRating': '5', 'economicMoat': 'None  ', 'sector': 'Consumer Cyclical', 'sectorCode': 'consumerCyclical', 'holdingTrend': {'trend': [803006.0, 759571.0, 765832.0, 751110.0]}, 'holdingType': 'Equity', 'isin': 'DE0007100000', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': 
            None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 22.068, 'susEsgRiskGlobes': 3, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Medium', 'qualRating': '5', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': "L'Oreal SA", 'secId': '0P00009WL0', 'performanceId': '0P00009WL0', 'holdingTypeId': 'E', 'weighting': 1.55569, 'numberOfShare': 2082.0, 'marketValue': 714646.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -6.109, 'forwardPERatio': 27.4725, 'stockRating': '3', 'economicMoat': 'Wide  ', 'sector': 'Consumer Defensive', 'sectorCode': 'consumerDefensive', 'holdingTrend': {'trend': [620302.0, 678699.0, 766384.0, 714646.0]}, 'holdingType': 'Equity', 'isin': 'FR0000120321', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 18.8705, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '3', 'quantRating': '3', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Allianz SE', 'secId': '0P00009QNO', 'performanceId': '0P00009QNO', 'holdingTypeId': 'E', 'weighting': 1.53689, 'numberOfShare': 4188.0, 'marketValue': 706013.0, 'shareChange': 657.0, 'country': 'Germany', 'ticker': None, 'totalReturn1Year': -12.8765, 'forwardPERatio': 6.9348, 'stockRating': '4', 'economicMoat': 'None  ', 'sector': 'Financial Services', 'sectorCode': 'financialService', 'holdingTrend': {'trend': [624064.0, 639162.0, 626117.0, 706013.0]}, 'holdingType': 'Equity', 'isin': 'DE0008404005', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 16.7195, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '4', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Essilorluxottica', 'secId': '0P00009WFV', 'performanceId': '0P00009WFV', 'holdingTypeId': 'E', 'weighting': 1.42695, 'numberOfShare': 4392.0, 'marketValue': 655506.0, 'shareChange': 0.0, 'country': 'France', 'ticker': None, 'totalReturn1Year': -13.6798, 'forwardPERatio': 20.4082, 'stockRating': '3', 'economicMoat': 'Wide  ', 'sector': 'Healthcare', 'sectorCode': 'healthcare', 'holdingTrend': {'trend': [719340.0, 757105.0, 669560.0, 655506.0]}, 'holdingType': 'Equity', 'isin': 'FR0000121667', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 
            'lastTurnoverRatio': None, 'susEsgRiskScore': 19.6763, 'susEsgRiskGlobes': 4, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'Low', 'qualRating': '3', 'quantRating': '5', 'bestRatingType': 'Qual', 'securityType': 'ST'}, {'securityName': 'Siemens AG', 'secId': '0P00009QS2', 'performanceId': '0P00009QS2', 'holdingTypeId': 'E', 'weighting': 1.42408, 'numberOfShare': 6472.0, 'marketValue': 654190.0, 'shareChange': 0.0, 'country': 'Germany', 'ticker': None, 'totalReturn1Year': -26.6171, 'forwardPERatio': 11.655, 'stockRating': '4', 'economicMoat': 'Narrow', 'sector': 'Industrials', 'sectorCode': 'industrials', 'holdingTrend': {'trend': [718233.0, 646628.0, 702471.0, 654190.0]}, 'holdingType': 'Equity', 'isin': 'DE0007236101', 'cusip': None, 'secondarySectorId': None, 'superSectorName': None, 'primarySectorName': None, 'secondarySectorName': None, 'firstBoughtDate': '2022-03-31T05:00:00.000', 'maturityDate': None, 'coupon': None, 'currency': 'Euro', 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': None, 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': 30.0804, 'susEsgRiskGlobes': 2, 'esgAsOfDate': '2022-09-07T05:00:00.000', 'susEsgRiskCategory': 'High', 'qualRating': '4', 'quantRating': '3', 'bestRatingType': 'Qual', 'securityType': 'ST'}], 'previousPeriodsDate': '2022-07-31T05:00:00.000'}, 'boldHoldingPage': {'pageSize': 25, 'pageNumber': 1, 'totalPage': 0, 'numberOfCurPageHolding': 0, 'numberOfAllHolding': 0, 'holdingList': [], 'previousPeriodsDate': None}, 'otherHoldingPage': {'pageSize': 25, 'pageNumber': 1, 'totalPage': 1, 'numberOfCurPageHolding': 1, 'numberOfAllHolding': 1, 'holdingList': [{'securityName': 'CACEIS Bank', 'secId': None, 'performanceId': None, 'holdingTypeId': 'C', 'weighting': 1.70728, 'numberOfShare': 784285.0, 'marketValue': 784285.0, 'shareChange': 200081.0, 'country': None, 'ticker': None, 'totalReturn1Year': None, 'forwardPERatio': None, 'stockRating': None, 'economicMoat': None, 'sector': None, 'sectorCode': None, 'holdingTrend': None, 'holdingType': 'Other', 'isin': None, 'cusip': None, 'secondarySectorId': '501011', 'superSectorName': 'cashAndEquivalents', 'primarySectorName': 'cashAndEquivalents', 'secondarySectorName': 'Cash', 'firstBoughtDate': None, 'maturityDate': None, 'coupon': None, 'currency': None, 'prospectusNetExpenseRatio': None, 'oneYearReturn': None, 'morningstarRating': None, 'ePUsedForOverallRating': 0, 'analystRating': '_PO_', 'totalAssets': None, 'ttmYield': None, 'epUsedFor1YearReturn': 0, 'morningstarCategory': None, 'totalAssetsMagnitude': None, 'lastTurnoverRatio': None, 'susEsgRiskScore': None, 'susEsgRiskGlobes': None, 'esgAsOfDate': None, 'susEsgRiskCategory': None, 'qualRating': None, 'quantRating': None, 'bestRatingType': None, 'securityType': None}], 'previousPeriodsDate': None}, 'userType': 'Free', 'portfolioLastestDateFooter': '2022-08-31T05:00:00.000', 'noPremiumChinaFund': False, 'numberOfEquityHoldingPer': 84.416, 'numberOfBondHoldingPer': 0.0, 'numberOfOtherHoldingPer': 15.584000000000001}
                    
        """

        return self.GetFundsData("portfolio/holding/v2", params = {"premiumNum" : 10000, "freeNum" : 10000})

    def proxyVotingManagement(self):
        """
        This function retrieves the vote of management.
  
        Returns:
            dict vote

        Examples:
            >>> Funds("rmagx", "us").proxyVotingManagement()

            {'template': 'US', 'managementList': []}

        """
        return self.GetFundsData("people/proxyVoting/management")
    

    def proxyVotingShareHolder(self):
        """
        This function retrieves the vote of shareholders.
  
        Returns:
            dict vote

        Examples:
            >>> Funds("rmagx", "us").proxyVotingShareHolder()

            {'template': 'US', 'shareholderList': []}

        """
        return self.GetFundsData("people/proxyVoting/shareHolder")

    def productInvolvement(self):
        """
        This function retrieves the involvement of the funds
  
        Returns:
            dict involvement

        Examples:
            >>> Funds("myria", "fr").proxyVotingShareHolder()

            {'fundEffectiveDate': '2022-07-31T05:00:00.000', 'categoryEffectiveDate': '2019-08-31T05:00:00.000', 'excludesEffectiveDate': '2021-11-01T05:00:00.000', 'portfolioDate': '2022-07-31T05:00:00.000', 'categoryName': 'Intermediate Government', 'categoryAsOfDate': '2022-06-30T05:00:00.000', 'businessPractices': [{'label': 'animalTesting', 'fundPercent': '0.00000', 'categoryPercent': '0.90000', 'employsExclusions': '0'}, {'label': 'furAndSpecialityLeather', 'fundPercent': '0.00000', 'categoryPercent': '0.00000', 'employsExclusions': '0'}], 'defenceAndMilitary': [{'label': 'controversialWeapons', 'fundPercent': '0.00000', 'categoryPercent': '0.14000', 'employsExclusions': '0'}, {'label': 'militaryContracting', 'fundPercent': '0.00000', 'categoryPercent': '0.16000', 'employsExclusions': '0'}, {'label': 'smallArms', 'fundPercent': '0.00000', 'categoryPercent': '0.01000', 'employsExclusions': '0'}], 'energy': [{'label': 'nuclear', 'fundPercent': '0.00000', 'categoryPercent': '0.22000', 'employsExclusions': '0'}, {'label': 'thermalCoal', 'fundPercent': '0.00000', 'categoryPercent': '0.37000', 'employsExclusions': '0'}], 'environment': [{'label': 'gmo', 'fundPercent': '0.00000', 'categoryPercent': '0.00000', 'employsExclusions': '0'}, {'label': 'palmOil', 'fundPercent': '0.00000', 'categoryPercent': '0.00000', 'employsExclusions': '0'}, {'label': 'pesticides', 'fundPercent': '0.00000', 'categoryPercent': '0.02000', 'employsExclusions': '0'}], 'healthAndLife': [{'label': 'alcohol', 'fundPercent': '0.00000', 'categoryPercent': '0.04000', 'employsExclusions': '0'}, {'label': 'tobacco', 'fundPercent': '0.00000', 'categoryPercent': '0.18000', 'employsExclusions': '0'}, {'label': 'lifeEthics', 'fundPercent': '0.00000', 'categoryPercent': '0.49000', 'employsExclusions': '0'}], 'valueBased': [{'label': 'adultEntertainment', 'fundPercent': '0.00000', 'categoryPercent': '0.00000', 'employsExclusions': '0'}, {'label': 'gambling', 'fundPercent': '0.00000', 'categoryPercent': '0.03000', 'employsExclusions': '0'}]}

        """

        return self.GetFundsData("esg/productInvolvement")


    def referenceIndex(self, index):
        """
        This function retrieves the name of the category or the benchmark

        Args:
            index (str) : possible values are benchmark, category     

        Returns:
            str category or benchmark

        Raises:
            ValueErrror whenever the index parameter is not category of benchmark

        Examples:
            >>> Funds("myria", "fr").referenceIndex("category")
            >>> Funds("myria", "fr").referenceIndex("benchmark")

            MSCI Europe NR EUR
            STOXX Europe Ex UK Large NR EUR
        
        """
        no_site_error(self.code,self.name,self.country,self.site)

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
        
        not_200_response(url,response)

        #html page as soup
        soup = BeautifulSoup(response.text, 'html.parser')
        benchmark_soup = soup.find(id='overviewBenchmarkDiv2Cols').find_all('td', {"class": "value text"})
        return benchmark_soup[index_row[index]].text

    def regionalSector(self):
        """
        This function retrieves the breakdown of the funds, category and index by region
  
        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria", "fr").regionalSector()

            {'fundPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'masterPortfolioId': '2852268', 'northAmerica': 1.156, 'unitedKingdom': 3.89123, 'europeDeveloped': 94.899, 'europeEmerging': 0.0, 'africaMiddleEast': 0.0, 'japan': 0.0, 'australasia': 0.0, 'asiaDeveloped': 0.0, 'asiaEmerging': 0.037, 'latinAmerica': 0.018}, 'categoryPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'masterPortfolioId': '204249', 'northAmerica': 1.86, 'unitedKingdom': 21.81407, 'europeDeveloped': 75.741, 'europeEmerging': 0.058, 'africaMiddleEast': 0.001, 'japan': 0.027, 'australasia': 0.017, 'asiaDeveloped': 0.381, 'asiaEmerging': 0.018, 'latinAmerica': 0.085}, 'indexPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'masterPortfolioId': '2593297', 'northAmerica': 1.476, 'unitedKingdom': 23.80484, 'europeDeveloped': 73.341, 'europeEmerging': 0.937, 'africaMiddleEast': 0.0, 'japan': 0.0, 'australasia': 0.0, 'asiaDeveloped': 0.26, 'asiaEmerging': 0.0, 'latinAmerica': 0.182}, 'categoryName': 'Europe Large-Cap Blend Equity', 'indexName': 'Morningstar Eur TME GR EUR', 'fundName': 'Myria Actions Durables Europe', 'assetType': 'EQUITY'}

        """
        return self.GetFundsData("portfolio/regionalSector")

    def regionalSectorIncludeCountries(self):
        """
        This function retrieves the breakdown of the funds, category and index by region and country
  
        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria", "fr").regionalSectorIncludeCountries()

            {'fundPortfolio': {'countries': [{'name': 'france', 'percent': 32.17199}, {'name': 'switzerland', 'percent': 20.13421}, {'name': 'germany', 'percent': 15.54962}, {'name': 'netherlands', 'percent': 13.02451}, {'name': 'spain', 'percent': 6.99548}, {'name': 'unitedKingdom', 'percent': 3.89123}, {'name': 'denmark', 'percent': 3.55594}, {'name': 'italy', 'percent': 3.45533}, {'name': 'unitedStates', 'percent': 1.15552}, {'name': 'china', 'percent': 0.03717}, {'name': 'brazil', 'percent': 0.01753}, {'name': 'sweden', 'percent': 0.01147}, {'name': 'argentina', 'percent': 0.0}, {'name': 'australia', 'percent': 0.0}, {'name': 'austria', 'percent': 0.0}, {'name': 'belgium', 'percent': 0.0}, {'name': 'canada', 'percent': 0.0}, {'name': 'chile', 'percent': 0.0}, {'name': 'colombia', 'percent': 0.0}, {'name': 'czechRepublic', 'percent': 0.0}, {'name': 'estonia', 'percent': 0.0}, {'name': 'finland', 'percent': 0.0}, {'name': 'greece', 'percent': 0.0}, {'name': 'hongKong', 'percent': 0.0}, {'name': 'hungary', 'percent': 0.0}, {'name': 'india', 'percent': 0.0}, {'name': 'indonesia', 'percent': 0.0}, {'name': 'ireland', 'percent': 0.0}, {'name': 'israel', 'percent': 0.0}, {'name': 'japan', 'percent': 0.0}, {'name': 'latvia', 'percent': 0.0}, {'name': 'lithuania', 'percent': 0.0}, {'name': 'malaysia', 'percent': 0.0}, {'name': 'mexico', 'percent': 0.0}, {'name': 'newZealand', 'percent': 0.0}, {'name': 'norway', 'percent': 0.0}, {'name': 'pakistan', 'percent': 0.0}, {'name': 'peru', 'percent': 0.0}, {'name': 'philippines', 'percent': 0.0}, {'name': 'poland', 'percent': 0.0}, {'name': 'portugal', 'percent': 0.0}, {'name': 'russia', 'percent': 0.0}, {'name': 'singapore', 'percent': 0.0}, {'name': 'slovakia', 'percent': 0.0}, {'name': 'southAfrica', 'percent': 0.0}, {'name': 'southKorea', 'percent': 0.0}, {'name': 'taiwan', 'percent': 0.0}, {'name': 'thailand', 'percent': 0.0}, {'name': 'turkey', 'percent': 0.0}, {'name': 'venezuela', 'percent': 0.0}, {'name': 'vietnam', 'percent': 0.0}], 'regions': [{'name': 'europeDeveloped', 'percent': 94.899}, {'name': 'unitedKingdom', 'percent': 3.89123}, {'name': 'northAmerica', 'percent': 1.156}, {'name': 'asiaEmerging', 'percent': 0.037}, {'name': 'latinAmerica', 'percent': 0.018}, {'name': 'asiaDeveloped', 'percent': 0.0}, {'name': 'australasia', 'percent': 0.0}, {'name': 'europeEmerging', 'percent': 0.0}, {'name': 'japan', 'percent': 0.0}, {'name': 'other Countries', 'percent': 0.0}], 'portfolioDate': '2022-08-31T05:00:00.000'}, 'categoryPortfolio': {'countries': [{'name': 'unitedKingdom', 'percent': 21.81407}, {'name': 'france', 'percent': 19.23783}, {'name': 'switzerland', 'percent': 13.89761}, {'name': 'germany', 'percent': 11.93784}, {'name': 'netherlands', 'percent': 8.36958}, {'name': 'denmark', 'percent': 5.23338}, {'name': 'sweden', 'percent': 4.37311}, {'name': 'spain', 'percent': 3.82678}, {'name': 'italy', 'percent': 2.7155}, {'name': 'unitedStates', 'percent': 1.85551}, {'name': 'finland', 'percent': 1.71156}, {'name': 'norway', 'percent': 1.52106}, {'name': 'belgium', 'percent': 1.13785}, {'name': 'ireland', 'percent': 0.9936}, {'name': 'portugal', 'percent': 0.42586}, {'name': 'singapore', 'percent': 0.37621}, {'name': 'austria', 'percent': 0.33051}, {'name': 'brazil', 'percent': 0.08415}, {'name': 'russia', 'percent': 0.05696}, {'name': 'japan', 'percent': 0.027}, {'name': 'australia', 'percent': 0.0167}, {'name': 'china', 'percent': 0.01453}, {'name': 'canada', 'percent': 0.0035}, {'name': 'taiwan', 'percent': 0.0022}, {'name': 'india', 'percent': 0.00206}, {'name': 'southKorea', 'percent': 0.00189}, {'name': 'poland', 'percent': 0.00057}, {'name': 'southAfrica', 'percent': 0.00054}, {'name': 'mexico', 'percent': 0.00052}, {'name': 'indonesia', 'percent': 0.00047}, {'name': 'thailand', 'percent': 0.00039}, {'name': 'hongKong', 'percent': 0.00037}, {'name': 'turkey', 'percent': 0.00027}, {'name': 'hungary', 'percent': 0.00023}, {'name': 'malaysia', 'percent': 0.00018}, {'name': 'greece', 'percent': 0.00013}, {'name': 'chile', 'percent': 0.0001}, {'name': 'israel', 'percent': 1e-05}, {'name': 'argentina', 'percent': 0.0}, {'name': 'colombia', 'percent': 0.0}, {'name': 'czechRepublic', 'percent': 0.0}, {'name': 'estonia', 'percent': 0.0}, {'name': 'latvia', 'percent': 0.0}, {'name': 'lithuania', 'percent': 0.0}, {'name': 'newZealand', 'percent': 0.0}, {'name': 'pakistan', 'percent': 0.0}, {'name': 'peru', 'percent': 0.0}, {'name': 'philippines', 'percent': 0.0}, {'name': 'slovakia', 'percent': 0.0}, {'name': 'venezuela', 'percent': 0.0}, {'name': 'vietnam', 'percent': 0.0}], 'regions': [{'name': 'europeDeveloped', 'percent': 75.741}, {'name': 'unitedKingdom', 'percent': 21.81407}, {'name': 'northAmerica', 'percent': 1.86}, {'name': 'asiaDeveloped', 'percent': 0.381}, {'name': 'latinAmerica', 'percent': 0.085}, {'name': 'europeEmerging', 'percent': 0.058}, {'name': 'other Countries', 'percent': 0.02958}, {'name': 'japan', 'percent': 0.027}, {'name': 'asiaEmerging', 'percent': 0.018}, {'name': 'australasia', 'percent': 0.017}], 'portfolioDate': '2022-08-31T05:00:00.000'}, 'indexPortfolio': {'countries': [{'name': 'unitedKingdom', 'percent': 23.80484}, {'name': 'switzerland', 'percent': 16.48783}, {'name': 'france', 
            'percent': 15.69505}, {'name': 'germany', 'percent': 11.1745}, {'name': 'netherlands', 'percent': 7.38964}, {'name': 'sweden', 'percent': 5.59513}, {'name': 'denmark', 'percent': 4.13353}, {'name': 'spain', 'percent': 3.79743}, {'name': 'italy', 'percent': 3.13256}, {'name': 'finland', 'percent': 1.75564}, {'name': 'norway', 'percent': 1.60206}, {'name': 'unitedStates', 'percent': 1.47578}, {'name': 'belgium', 'percent': 1.3521}, {'name': 'ireland', 'percent': 0.38065}, {'name': 'austria', 'percent': 0.38044}, {'name': 'turkey', 'percent': 0.35875}, {'name': 'poland', 'percent': 0.33953}, {'name': 'portugal', 'percent': 0.28577}, {'name': 'singapore', 'percent': 0.26032}, {'name': 'brazil', 'percent': 0.16549}, {'name': 'greece', 'percent': 0.15367}, {'name': 'hungary', 'percent': 0.12807}, {'name': 'czechRepublic', 'percent': 0.11031}, {'name': 'mexico', 'percent': 0.01678}, {'name': 'argentina', 'percent': 0.0}, {'name': 'australia', 'percent': 0.0}, {'name': 'canada', 'percent': 0.0}, {'name': 'chile', 'percent': 0.0}, {'name': 'china', 'percent': 0.0}, {'name': 'colombia', 'percent': 0.0}, {'name': 'estonia', 'percent': 0.0}, {'name': 'hongKong', 'percent': 0.0}, {'name': 'india', 'percent': 0.0}, {'name': 'indonesia', 'percent': 0.0}, {'name': 'israel', 'percent': 0.0}, {'name': 'japan', 'percent': 0.0}, {'name': 'latvia', 'percent': 0.0}, {'name': 'lithuania', 'percent': 0.0}, {'name': 'malaysia', 'percent': 0.0}, {'name': 'newZealand', 'percent': 0.0}, {'name': 'pakistan', 'percent': 0.0}, {'name': 'peru', 'percent': 0.0}, {'name': 'philippines', 'percent': 0.0}, {'name': 'russia', 'percent': 0.0}, {'name': 'slovakia', 'percent': 0.0}, {'name': 'southAfrica', 'percent': 0.0}, {'name': 'southKorea', 'percent': 0.0}, {'name': 'taiwan', 'percent': 0.0}, {'name': 'thailand', 'percent': 0.0}, {'name': 'venezuela', 'percent': 0.0}, {'name': 'vietnam', 'percent': 0.0}], 'regions': [{'name': 'europeDeveloped', 'percent': 73.341}, {'name': 'unitedKingdom', 'percent': 23.80484}, {'name': 'northAmerica', 'percent': 1.476}, {'name': 'europeEmerging', 'percent': 0.937}, {'name': 'asiaDeveloped', 'percent': 0.26}, {'name': 'latinAmerica', 'percent': 0.182}, {'name': 'other Countries', 'percent': 0.02412}, {'name': 'asiaEmerging', 'percent': 0.0}, {'name': 'australasia', 'percent': 0.0}, {'name': 'japan', 'percent': 0.0}], 'portfolioDate': '2022-08-31T05:00:00.000'}, 'categoryName': 'Europe Large-Cap Blend Equity', 'indexName': 'Morningstar Eur TME GR EUR', 'fundName': 'Myria Actions Durables Europe', 'assetType': 'EQUITY'}
        """
        return self.GetFundsData("portfolio/regionalSectorIncludeCountries")



    def riskReturnScatterplot(self):
        """
        This function retrieves the return and standard deviation of the funds and category
  
        Returns:
            dict risk return

        Examples:
            >>> Funds("rmagx", "us").riskReturnScatterplot()

            {'fundName': 'American Funds Mortgage R6', 'categoryName': 'Intermediate Government', 'indexName': 'Morningstar US Trsy Bd TR USD', 'cur': 'USD', 'isUKCefTemplateAvailable': False, 'extendedPerformanceData': {'ePUsedFor1YearFlag': False, 'ePUsedFor3YearFlag': False, 'ePUsedFor5YearFlag': False, 'ePUsedFor10YearFlag': False, 'ePUsedFor15YearFlag': False}, 'fundScatterplot': {'standardDeviationEndDate': '2022-09-30T05:00:00.000', 'trailingReturnEndDate': '2022-09-30T05:00:00.000', 'trailingReturnPriceEndDate': '2022-09-30T05:00:00.000', 'for1Year': {'trailingReturn': -11.47318, 'trailingReturnPrice': None, 'standardDeviation': 6.535}, 'for3Year': {'trailingReturn': -1.77699, 'trailingReturnPrice': None, 'standardDeviation': 4.53}, 'for5Year': {'trailingReturn': -0.05352, 'trailingReturnPrice': None, 'standardDeviation': 3.847}, 'for10Year': {'trailingReturn': 1.00022, 'trailingReturnPrice': None, 'standardDeviation': 3.14}, 'for15Year': {'trailingReturn': None, 'trailingReturnPrice': None, 'standardDeviation': None}, 'forLongestTenure': None}, 'categoryScatterplot': {'standardDeviationEndDate': '2022-09-30T05:00:00.000', 'trailingReturnEndDate': '2022-09-30T05:00:00.000', 'trailingReturnPriceEndDate': None, 'for1Year': {'trailingReturn': -12.79164, 'trailingReturnPrice': None, 'standardDeviation': 6.297}, 'for3Year': {'trailingReturn': -3.19848, 'trailingReturnPrice': None, 'standardDeviation': 4.687}, 'for5Year': {'trailingReturn': -0.73062, 'trailingReturnPrice': None, 'standardDeviation': 4.127}, 'for10Year': {'trailingReturn': 0.14931, 'trailingReturnPrice': None, 'standardDeviation': 3.508}, 'for15Year': {'trailingReturn': 2.08912, 'trailingReturnPrice': None, 'standardDeviation': 3.732}, 'forLongestTenure': None}, 'indexScatterplot': {'standardDeviationEndDate': '2022-09-30T05:00:00.000', 'trailingReturnEndDate': '2022-09-30T05:00:00.000', 'trailingReturnPriceEndDate': None, 'for1Year': {'trailingReturn': -12.81863, 'trailingReturnPrice': None, 'standardDeviation': 5.753}, 'for3Year': {'trailingReturn': -3.08081, 'trailingReturnPrice': None, 'standardDeviation': 5.312}, 'for5Year': {'trailingReturn': -0.21542, 'trailingReturnPrice': None, 'standardDeviation': 4.929}, 'for10Year': {'trailingReturn': 0.49974, 'trailingReturnPrice': None, 'standardDeviation': 4.092}, 'for15Year': {'trailingReturn': 2.33825, 'trailingReturnPrice': None, 'standardDeviation': 4.389}, 'forLongestTenure': None}}
        
        """
        return self.GetFundsData("performance/riskReturnScatterplot")

    def riskReturnSummary(self):
        """
        This function retrieves the return and risk summary of the funds compare to the category
  
        Returns:
            dict risk return

        Examples:
            >>> Funds("rmagx", "us").riskReturnSummary()

            {'endDate': '2022-08-31T05:00:00.000', 'categoryName': 'Intermediate Government', 'for3Year': {'epUsedFlag': False, 'riskVsCategory': 2, 'returnVsCategory': 5, 'numberOfFunds': 226}, 'for5Year': {'epUsedFlag': False, 'riskVsCategory': 2, 'returnVsCategory': 5, 'numberOfFunds': 215}, 'for10Year': {'epUsedFlag': False, 'riskVsCategory': 2, 'returnVsCategory': 5, 'numberOfFunds': 178}}
        
        """

        return self.GetFundsData("performance/riskReturnSummary")

    def riskVolatility(self):
        """
        This function retrieves the alpha, beta, R², volatility and Sharpe ratio of the funds, category and index.

        Returns:
            dict econometrics

        Examples:
            >>> Funds("rmagx", "us").riskVolatility()

            {'fundName': 'American Funds Mortgage R6', 'categoryName': 'Intermediate Government', 'indexName': 'Morningstar US Trsy Bd TR USD', 'calculationBenchmark': 'Bloomberg US Agg Bond TR USD', 'extendedPerformanceData': {'ePUsedFor1YearFlag': False, 'ePUsedFor3YearFlag': False, 'ePUsedFor5YearFlag': False, 'ePUsedFor10YearFlag': False, 'ePUsedFor15YearFlag': False}, 'fundRiskVolatility': {'primaryIndexNameNew': 'Bloomberg US Agg Bond TR USD', 'bestFitIndexName': None, 'bestFitAlphaFor3Year': None, 'bestFitBetaFor3Year': None, 'bestFitRSquaredFor3Year': None, 'endDate': '2022-09-30T05:00:00.000', 'for1Year': {'alpha': 2.264, 'beta': 0.923, 'rSquared': 94.037, 'standardDeviation': 6.535, 'sharpeRatio': -1.95}, 'for3Year': {'alpha': 0.574, 'beta': 0.763, 'rSquared': 80.231, 'standardDeviation': 4.53, 'sharpeRatio': -0.503}, 'for5Year': {'alpha': -0.187, 'beta': 0.729, 'rSquared': 80.472, 'standardDeviation': 3.847, 'sharpeRatio': -0.302}, 'for10Year': {'alpha': 0.152, 'beta': 0.72, 'rSquared': 79.803, 'standardDeviation': 3.14, 'sharpeRatio': 0.106}, 'for15Year': {'alpha': None, 'beta': None, 'rSquared': None, 'standardDeviation': None, 'sharpeRatio': None}, 'forLongestTenure': None}, 'categoryRiskVolatility': {'endDate': '2022-09-30T05:00:00.000', 'for1Year': {'alpha': None, 'beta': None, 'rSquared': None, 'standardDeviation': 6.297, 'sharpeRatio': -2.305}, 'for3Year': {'alpha': None, 'beta': None, 'rSquared': None, 'standardDeviation': 4.687, 'sharpeRatio': -0.795}, 'for5Year': {'alpha': None, 'beta': None, 'rSquared': None, 'standardDeviation': 4.127, 'sharpeRatio': -0.449}, 'for10Year': {'alpha': None, 'beta': None, 'rSquared': None, 'standardDeviation': 3.508, 'sharpeRatio': -0.15}, 'for15Year': {'alpha': None, 'beta': None, 'rSquared': None, 'standardDeviation': 3.732, 'sharpeRatio': 0.392}, 'forLongestTenure': None}, 'indexRiskVolatility': {'endDate': '2022-09-30T05:00:00.000', 'for1Year': {'alpha': -1.124, 'beta': 0.813, 'rSquared': 94.48, 'standardDeviation': 5.753, 'sharpeRatio': -2.487}, 'for3Year': {'alpha': -0.395, 'beta': 0.85, 'rSquared': 74.013, 'standardDeviation': 5.312, 'sharpeRatio': -0.676}, 'for5Year': {'alpha': -0.056, 'beta': 0.912, 'rSquared': 78.417, 'standardDeviation': 4.929, 'sharpeRatio': -0.262}, 'for10Year': {'alpha': -0.367, 'beta': 0.94, 'rSquared': 81.737, 'standardDeviation': 4.092, 'sharpeRatio': -0.031}, 'for15Year': {'alpha': -0.299, 'beta': 0.967, 'rSquared': 73.717, 'standardDeviation': 4.389, 'sharpeRatio': 0.399}, 'forLongestTenure': None}, 'cur': 'USD'}
        
        """
        return self.GetFundsData("performance/riskVolatility")

    def salesFees(self):
        """
        This function retrieves the sales fees of the funds

        Returns:
            dict fees

        Examples:
            >>> Funds("myria", "fr").salesFees()

            {'salesFees': {'frontloadFee': [5.0, None, None, None, None, None, None, None, None], 'frontloadFeeLowBreakpoint': [0, None, None, None, None, None, None, None, None], 'deferredloadFee': [0.0, None, None, None, None, None, None], 'redemptionFeeLowBreakpoint': [0, None, None, None, None, None], 'redemptionFee': [0.0, 
            None, None, None, None, None], 'deferredloadFeeLowBreakpoint': [0, None, None, None, None, None, None]}, 'minInitialInvestment': 1000000, 'currencyId': 'EUR', 
            'minInvestmentCurrency': 'EUR', 'frontloadFeeBreakpointUnit': None, 'frontloadFeeUnit': None, 'redemptionFeeBreakpointUnit': 'Months', 'redemptionFeeUnit': 'Percentage', 'deferredloadFeeBreakpointUnit': 'Months', 'deferredloadFeeUnit': 'Percentage', 'minimumInitialInvestmentUnit': 'Monetary'}
                    
        """
        if self.asset_type == 'etf':
            return {}
        return self.GetFundsData("price/salesFees")

    def sector(self):
        """
        This function retrieves the sector breakdown of the funds, category and index
  
        Returns:
            dict sector breakdown

        Examples:
            >>> Funds("myria", "fr").sector()

            {'FIXEDINCOME': {'fundPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'government': 0.0, 'municipal': 0.0, 'corporate': 0.0, 'securitized': 0.0, 'cashAndEquivalents': 66.74815, 'derivative': 33.25185}, 'categoryPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'government': 1.95911, 'municipal': 0.0, 
'           corporate': 0.70065, 'securitized': 0.83335, 'cashAndEquivalents': 79.15027, 'derivative': 17.35662}, 'indexPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'government': 0.0, 'municipal': 0.0, 'corporate': 88.33522, 'securitized': 0.0, 'cashAndEquivalents': 11.66478, 'derivative': 0.0}, 'categoryName': 'Europe Large-Cap Blend Equity', 'indexName': 'Morningstar Eur TME GR EUR', 'fundName': 'Myria Actions Durables Europe', 'assetType': 'FIXEDINCOME'}, 'EQUITY': {'fundPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'basicMaterials': 7.98386, 'consumerCyclical': 12.17881, 'financialServices': 15.12426, 'realEstate': 0.0, 'communicationServices': 4.19609, 'energy': 4.47861, 'industrials': 13.33409, 'technology': 7.88651, 'consumerDefensive': 12.00854, 'healthcare': 18.35617, 'utilities': 4.45305}, 'categoryPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'basicMaterials': 7.40798, 'consumerCyclical': 9.50899, 'financialServices': 15.54632, 'realEstate': 1.522, 'communicationServices': 5.60033, 'energy': 5.00095, 'industrials': 13.70374, 'technology': 7.92333, 'consumerDefensive': 13.26291, 'healthcare': 16.69305, 'utilities': 3.8304}, 'indexPortfolio': {'portfolioDate': '2022-08-31T05:00:00.000', 'basicMaterials': 6.97774, 'consumerCyclical': 9.42487, 'financialServices': 16.12159, 'realEstate': 1.26235, 'communicationServices': 4.99965, 'energy': 6.76732, 'industrials': 13.78767, 'technology': 6.55932, 'consumerDefensive': 13.96182, 'healthcare': 15.84156, 'utilities': 4.29611}, 'categoryName': 'Europe Large-Cap Blend Equity', 'indexName': 'Morningstar Eur TME GR EUR', 'fundName': 'Myria Actions Durables Europe', 'assetType': 'EQUITY'}, 'assetType': 'EQUITY'}
        
        """
        return self.GetFundsData("portfolio/v2/sector")

    def starRatingFundAsc(self):
        """
        This function retrieves the MorningStar rating of the funds of the company by ascending order
  
        Returns:
            dict rating

        Examples:
            >>> Funds("myria", "fr").starRatingFundAsc()

            {'StarRatingFund': [{'calendarYearFlow': -22230505.0, 'netAsset': 166636000.0, 'fundShareClassId': 'F00000PO9H', 'mstarRating': '1', 'overallMorningstarRating': None, 'name': 'Myria Actions Durables France', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': -0.05624, 'trailing3YearReturnRank': '61', 'secId': 'F00000PO9H', 'securityType': 'FO'}, {'calendarYearFlow': 320988.0, 'netAsset': 4800000.0, 'fundShareClassId': 'F000010CKF', 'mstarRating': '1', 'overallMorningstarRating': None, 'name': 'Myria+River 31 Global Opportunities I', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': -5.37891, 'trailing3YearReturnRank': '94', 'secId': 'F000010CKF', 'securityType': 'FO'}, {'calendarYearFlow': -361.0, 'netAsset': 20815.0, 'fundShareClassId': 'F00000XL7O', 'mstarRating': '1', 'overallMorningstarRating': None, 'name': 'Myria Concept Europe Alpha E', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': -3.46989, 'trailing3YearReturnRank': '88', 'secId': 'F00000XL7O', 'securityType': 'FO'}, {'calendarYearFlow': 39884896.0, 'netAsset': 138132300.0, 'fundShareClassId': 'F0GBR04QXU', 'mstarRating': '2', 'overallMorningstarRating': 
            None, 'name': 'UFF Allocation Diversifiée A', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': -4.42882, 'trailing3YearReturnRank': '90', 'secId': 'F0GBR04QXU', 'securityType': 'FO'}, {'calendarYearFlow': 3900307.0, 'netAsset': 133952637.0, 'fundShareClassId': 'F00000SELA', 'mstarRating': '2', 'overallMorningstarRating': None, 'name': 'Grandes Marques ISR M', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 
            0.0, 'trailing3YearReturn': 6.84493, 'trailing3YearReturnRank': '33', 'secId': 'F00000SELA', 'securityType': 'FO'}], 'footerFundFlowDate': '2022-08-31T05:00:00.000', 'footerReturnDate': '2022-09-30T05:00:00.000', 'currency': 'EUR', 'secId': None, 'securityType': None, 'userType': 'Free'}
                    
        """
        
        return self.GetFundsData("parent/mstarRating/StarRatingFundAsc")

    def starRatingFundDesc(self):
        """
        This function retrieves the MorningStar rating of the funds of the company by descending order
  
        Returns:
            dict rating

        Examples:
            >>> Funds("myria", "fr").starRatingFundDesc()

            {'StarRatingFund': [{'calendarYearFlow': -15110174.0, 'netAsset': 213914553.0, 'fundShareClassId': 'F00000T11Z', 'mstarRating': '4', 'overallMorningstarRating': None, 'name': 'UFF Valeurs PME A', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': -1.42846, 'trailing3YearReturnRank': '65', 'secId': 'F00000T11Z', 'securityType': 'FO'}, {'calendarYearFlow': -149285593.0, 'netAsset': 407440000.0, 'fundShareClassId': 'F0GBR04QY4', 'mstarRating': '3', 'overallMorningstarRating': None, 'name': 'Euro Valeur ISR M', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': -1.7233, 'trailing3YearReturnRank': '74', 'secId': 'F0GBR04QY4', 'securityType': 'FO'}, {'calendarYearFlow': 45065351.0, 'netAsset': 196497827.0, 'fundShareClassId': 'F00000U4DZ', 'mstarRating': '3', 'overallMorningstarRating': None, 'name': 'Europe Evolutif M', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': 3.14084, 'trailing3YearReturnRank': '11', 'secId': 'F00000U4DZ', 'securityType': 'FO'}, {'calendarYearFlow': -18927978.0, 'netAsset': 152360311.0, 'fundShareClassId': 'F00000SEHW', 'mstarRating': '3', 'overallMorningstarRating': None, 'name': 'Myria Concept Multistars M', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': 0.43495, 'trailing3YearReturnRank': '44', 'secId': 'F00000SEHW', 'securityType': 'FO'}, {'calendarYearFlow': 39884896.0, 'netAsset': 138132300.0, 'fundShareClassId': 'F0GBR04QXU', 'mstarRating': '2', 'overallMorningstarRating': None, 'name': 'UFF Allocation Diversifiée A', 'returnEndDate': '2022-09-30T05:00:00.000', 'ePUsedFor3YearReturn': 0.0, 'trailing3YearReturn': -4.42882, 'trailing3YearReturnRank': '90', 'secId': 'F0GBR04QXU', 'securityType': 'FO'}], 'footerFundFlowDate': '2022-08-31T05:00:00.000', 'footerReturnDate': '2022-09-30T05:00:00.000', 'currency': 'EUR', 'secId': None, 'securityType': None, 'userType': 'Free'}
        
        """
        
        return self.GetFundsData("parent/mstarRating/StarRatingFundDesc")

    def taxes(self):
        """
        This function retrieves the other fee of the etf

        Returns:
            dict taxes

        Examples:
            >>> Funds("American Century Foc Dynmc Gr ETF").taxes()

            {'categoryEndDate': None, 'returnEndDate': '2023-01-31T06:00:00.000', 'trailing1YearTaxCostRatio': None, 'trailing3YearTaxCostRatio': None, 
            'trailing5YearTaxCostRatio': None, 'trailing10YearTaxCostRatio': None, 'trailing15YearTaxCostRatio': None, 'sinceInceptionTaxCostRatio': None, 
            'potentialCapitalGain': -0.15581910000000002, 'trailing1YearTaxCostRatioCategory': None, 'trailing3YearTaxCostRatioCategory': None, 'trailing5YearTaxCostRatioCategory': None, 
            'trailing10YearTaxCostRatioCategory': None, 'trailing15YearTaxCostRatioCategory': None, 'sinceInceptionTaxCostRatioCategory': None, 'priceTemplate': 'USA_ETF'}

        """
        return self.GetFundsData("price/taxes")

    def trailingReturn(self, duration ='daily'):
        """
        This function retrieves the trailing return of the funds of the company.

        Args:
        duration (str) : frequency of return can be daily, monthly or quarterly
        
        Returns:
            dict trailing return

        Raises:
            ValueError whenever the parameter duration is not daily, monthly or quarterly

        Example:
            >>> Funds("myria", "fr").trailingReturn("daily")
            

        """

        duration_choice = ["daily", "monthly", "quarterly"]
        if duration not in duration_choice:
            raise ValueError(f'duration parameter can only take one of the values: {", ".join(duration_choice)}')


        return self.GetFundsData("trailingReturn/v2",{"duration" : duration})