""" class funds """
import pandas as pd
import datetime
import requests
import warnings

from .search import screener_universe
from .security import Security
from .utils import random_user_agent


class Funds(Security):
    """
    Main class to access data about funds and etf, inherit from Security class

    Args:
        term (str): text to find a fund, can be a name, part of a name or the isin of the funds
        language (str): language of the data, default is "en-gb"
        filters (dict) : filter, use the method search_filter() to find the different possible filter keys
        itemRange (int) : index of stocks to return (must be inferior to PageSize)
        pageSize (int): number of securities to return
        page (int): page to return
        sortby (str) : sort by a field
        ascending (bool) : True sort by ascending order, False sort by descending order
        proxies (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}

    Examples:
        >>> Funds("myria",page=2, pageSize=15,itemRange=3,sortby="name", ascending=True)
        >>> Funds('bond', 25, 2)

    Raises:
        TypeError: raised whenever the parameter type is not the type expected
        ValueError : raised whenever the parameter is not valid or no fund found

    """

    def __init__(
        self,
        term:str,
        language:str="en-gb",
        filters:dict=None,
        itemRange:int=0,
        pageSize:int=10,
        page:int=1,
        sortby:str=None,
        ascending:bool=True,
        proxies:dict=None,
    ) -> None:
        
        fund_filter = {"investmentType" : ['FE', 'FO', 'FC']}
        if filters:
            fund_filter = fund_filter | filters
        
        super().__init__(
            term=term,
            asset_type="fund",
            language=language,
            filters=fund_filter,
            itemRange=itemRange,
            pageSize=pageSize,
            page=page,
            sortby=sortby,
            ascending=ascending,
            proxies=proxies,
        )

    def allocationMap(self, 
                       version:int=3) -> dict:
        """
        This function retrieves the asset allocation of the funds, index and category.
        Args:
            version (int) : version of the api of allocation map 2 or 3
        Returns:
            dict with allocation map

        Examples:
            >>> Funds("myria").allocationMap()

        """
        if not isinstance(version,int):
            raise TypeError("version paramater should be an integer")
        
        if version not in range(2,4):
            raise ValueError("version paramater should be 2 or 3")

        return self.GetData(f"process/asset/v{version}").json()
    

    def allocationWeighting(self) -> dict:
        """
        This function retrieves the Growth/Blend/Value and
        market capitalizaton allocation size of the funds.

        Returns:
            dict with allocation

        Examples:
            >>> Funds("myria").allocationWeighting()

        """
        return self.GetData("process/weighting").json()

    def analystRating(self) -> list[dict]:
        """
        This function retrieves the rating of the funds

        Returns:
            list of dict with ratings

            >>> Funds("myria").analystRating()

        """

        return self.GetData("parent/analystRating").json()

    def analystRatingTopFunds(self) -> dict:
        """
        This function retrieves the rating Top funds

        Returns:
            dict with ratings

            >>> Funds("myria").analystRatingTopFunds()

        """

        return self.GetData("parent/analystRating/topfunds").json()

    def analystRatingTopFundsUpDown(self) -> dict:
        """
        This function retrieves the rating funds Up Down

        Returns:
            dict with ratings

            >>> Funds("myria").analystRatingTopFundsUpDown()

        """

        return self.GetData("parent/analystRating/topfundsUpDown").json()


    def carbonMetrics(self) -> dict:
        """
        This function retrieves the carbon metrics of the funds.

        Returns:
            dict with carbon metrics

        Examples:
            >>> Funds("myria").carbonMetrics()

        """

        return self.GetData("esg/carbonMetrics").json()

    def costIllustration(self) -> dict:
        """
        This function retrieves the cost of the funds.

        Returns:
            dict cost of funds

        Examples:
            >>> Funds("FOUSA00E5P").costIllustration()

        """
        return self.GetData("price/costIllustration").json()
    
    def costProjection(self) -> dict:
        """
        This function retrieves performance with the cost projection.

        Returns:
            dict performance with cost projection

        Examples:
            >>> Funds("FOUSA00E5P").costProjection()

        """
        return self.GetData("price/costProjection").json()

    def couponRange(self)  :
        """
        This function retrieves the coupon of the funds, index and category.

        Returns:
            dict coupon

        Examples:
            >>> Funds("myria").couponRange()

        """
        return self.GetData("process/couponRange").json()

    def creditQuality(self) -> dict:
        """
        This function retrieves the credit notation of the funds, index and category.

        Returns:
            dict credit notation

        Examples:
            >>> Funds("myria").creditQuality()

        """
        return self.GetData("portfolio/creditQuality").json()

    def distribution(self, 
                     period:str="annual") -> dict:
        """
        This function retrieves the coupon distributed by the funds.

        Args:
            period (str) : annual or latest

        Raises:
            ValueError whenever the pariod parameter is not annual or latest

        Returns:
            dict distribution of coupon

        Example:
            >>> Funds("myria").distribution("annual")

        """

        period_choice = ["annual", "latest"]
        if period not in period_choice:
            raise ValueError(
                f"""period parameter can only take one of
                             the values: {", ".join(period_choice)}"""
            )

        return self.GetData(f"distribution/{period}").json()

    def downloadDocument(self,
                         marketId:str,
                         documentType:str,
                         languageId:str,
                         folderPath:str=".") -> dict:
        
        """
        This function download documents.

        Args:
            marketId (str) : country available for the document, represented using two-letter codes
            documentType (str) : document to download
            languageId (str) : languages available for the document, represented using two-letter codes
            folderPath (str) : folder path where to save the file 
        Raises:
            TypeError raised whenever the fund is not available in the marketId

        Returns:
            dict with documents information

        Examples:
            >>> Funds("myria").getDocumentInformation("fr")

        """

        if not isinstance(marketId, str):
            raise TypeError("marketId parameter should be a string")
        
        if not isinstance(documentType, str):
            raise TypeError("marketId parameter should be a string")
        
        if not isinstance(languageId, str):
            raise TypeError("marketId parameter should be a string")

        docInfo = self.getDocumentInformation(marketId)

        if "documents" not in docInfo["components"]:
            raise FileNotFoundError(f"There are no documents available for the {self.asset_type} {self.name} ({self.code})") 
        docFound = False
        docType = []
        foundLanguage = False
        languageAvailable = []
        if docInfo["components"]["documents"]["status"] != 200:
            raise FileNotFoundError(f"There are no documents available for the {self.asset_type} {self.name} ({self.code}) on market {marketId}") 

        for document in docInfo["components"]["documents"]["payload"]:
            docType.append(document["name"])
            if document["name"] == documentType:
                docFound = True
                docId = document["id"]
                for documents in document["documents"]:
                    docExtension =documents["mimeType"]
                    docDate = documents["effectiveDate"]
                    for language in documents["languages"]:
                        documentLanguage = language
                        languageAvailable.append(documentLanguage)
                        if language == languageId:
                            foundLanguage = True
                            break
                    if foundLanguage == True:
                        break
                break
                    
        if docFound == False:
            raise FileNotFoundError(f"""The document type {documentType} 
                                  does not exist for the {self.asset_type}
                                    {self.name} ({self.code}).
                                    Documents type available are {', '.join(docType)}""")
        
        if docExtension != "application/pdf":
            raise FileExistsError(f"""The document type {documentType} 
                                  exists for the {self.asset_type}
                                    {self.name} ({self.code}), but it's extension is {docExtension}.
                                    This type of file is not yet supported  is not by MStarpy.""")
        if foundLanguage == False:
            warnings.warn(f"""Document language {languageId} is not found, 
                          available language are {', '.join(languageAvailable)}.
                          The document in {languageAvailable[-1]} is downloaded.""")
            
        url = f"https://global.morningstar.com/api/v1/{marketId}/investments/{self.asset_type}s/{self.code}/documents/_document"

        params = { "documentId" : docId,
                  "languageId" : documentLanguage}
        
        headers = {"user-agent": random_user_agent()}

        response = requests.get(
            url, params=params, headers=headers, proxies=self.proxies
        )

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fileName = f"{documentType}-{self.code}-{docDate}-{timestamp}.pdf"
        with open(f"{folderPath}/{fileName}", "wb") as f:
            f.write(response.content)


        return {"status" : response.status_code, 
                "mesage" : "File downloaded", 
                "filename" : fileName,
                "folder" : folderPath}
    def equityStyle(self) -> dict:
        """
        This function retrieves the equity style of the funds and category.

        Returns:
            dict equity style

        Examples:
            >>> Funds("myria").equityStyle()

        """
        return self.GetData("process/stockStyle/v2").json()

    def equityStyleBoxHistory(self) -> dict:
        """
        This function retrieves the equity style history of the funds

        Returns:
            dict equity style history

        Examples:
            >>> Funds("myria").equityStyleBoxHistory()

        """
        return self.GetData("process/equityStyleBoxHistory").json()

    def esgData(self) -> dict:
        """
        This function retrieves ESG data of the funds and category

        Returns:
            dict ESG data

        Examples:
            >>> Funds("myria").esgData()

        """

        return self.GetData("esg/v1").json()
    
    def esgRisk(self) -> dict:
        """
        This function retrieves ESG drisk of the funds and category

        Returns:
            dict ESG risk

        Examples:
            >>> Funds("myria").esgRisk()

        """

        return self.GetData("esgRisk").json()

    def factorProfile(self) -> dict:
        """
        This function retrieves the factor profile of the funds, index and category

        Returns:
            dict factor profile

        Examples:
            >>> Funds("myria").factorProfile()

        """
        return self.GetData("factorProfile").json()

    def feeLevel(self)  :
        """
        This function retrieves the fees of the fund compare to its category.

        Returns:
            dict fees

        Examples:
            >>> Funds("myria").feeLevel()

        """
        return self.GetData("price/feeLevel/v1").json()

    def feeMifid(self, 
                 currency:str="EUR") -> dict:
        """
        This function retrieves the fees of the fund.

        Returns:
            dict fees

        Examples:
            >>> Funds("myria").feeMifid()

        """
        return self.ltData("Mifid", currency=currency)

    def financialMetrics(self) -> dict:
        """
        This function retrieves the final metrics of the funds and category.

        Returns:
            dict financial metrics

        Examples:
            >>> Funds("myria").financialMetrics()

        """
        return self.GetData("process/financialMetrics").json()

    def fixedIncomeStyle(self) -> dict:
        """
        This function retrieves the fixed income style of the funds and category.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("myria").fixedIncomeStyle()

        """

        return self.GetData("process/fixedIncomeStyle").json()

    def fixedincomeStyleBoxHistory(self) -> dict:
        """
        This function retrieves the fixed income style history of the funds.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("myria").fixedincomeStyleBoxHistory()

        """
        return self.GetData("process/fixedincomeStyleBoxHistory").json()

    def graphData(self) -> dict:
        """
        This function retrieves historical Total Assets and Net Flow of the funds.

        Returns:
            dict historical data

        Examples:
            >>> Funds("myria").graphData()

        """

        return self.GetData("parent/graphData").json()

    def getDocumentInformation(self, 
                    marketId:str
                    ) -> dict:
        """
        This function retrieves information about documents.
        Args:
            marketId (str) : country in two letters from where the document is available

        Raises:
            TypeError raised whenever the fund is not available in the marketId

        Returns:
            dict with documents information

        Examples:
            >>> Funds("myria").getDocumentInformation("fr")

        """

        if not isinstance(marketId, str):
            raise TypeError("marketId parameter should be a string")

        
        # url of API
        url = f"""https://global.morningstar.com/api/v1/{marketId}/investments/{self.asset_type}s/{self.code}/documents"""

        params = { "marketId" : marketId}
        headers = {"user-agent": random_user_agent()}

        response = requests.get(
            url, params=params, headers=headers, proxies=self.proxies
        )

        response_json = response.json()
        print(response_json)
        if "message" in response_json and response.status_code == 404:
            if response_json["message"] == 'Security Market Access Error':
                raise ValueError(f"marketId paramater can only take one of these values {', '.join(response_json['allowedMarketIds'])} ")

        return response_json

    def historicalData(self, 
                       version:int=4) -> dict:
        """
        This function retrieves the historical price of the funds, index and category

        Args:
            version (int) : version of the api of historical data from 2 to 5
        
        Returns:
            dict with historical data

        Examples:
            >>> Funds("myria").historicalData()

        """
        if not isinstance(version,int):
            raise TypeError("version paramater should be an integer")
        
        if version not in range(2,5):
            raise ValueError("version paramater should be between 2 and 5")

        return self.GetData(f"performance/v{version}", url_suffix="").json()

    def historicalExpenses(self) -> dict:
        """
        This function retrieves historical expenses of the funds.

        Returns:
            dict historical expenses

        Examples:
            >>> Funds("myria").historicalExpenses()

        """
        if self.asset_type == "etf":
            return {}
        return self.GetData("price/historicalExpenses").json()
    
    def historicalRating(self) -> dict:
        """
        This function retrieves MorningStar historical rating of the fund.

        Returns:
            dict historical rating

        Examples:
            >>> Funds("myria").historicalRating()

        """

        return self.GetData("morningstarTake/historicalRating").json()

    def holdings(self, 
                 holdingType: str = "all") -> pd.DataFrame:
        """
        This function retrieves holdings of the funds.

        Args:
            holdingType (str) : paramater to select the kind of holdings; all, bond, equity or other

        Returns:
            pandas DataFrame holdings

        Raises:
            ValueError whenever the parameter is not all, bond, equity or other

        Examples:
            >>> Funds("myria").holdings("all")
            >>> Funds("myria").holdings("bond")
            >>> Funds("myria").holdings("equity")
            >>> Funds("myria").holdings("other")

        """
        holdingType_to_holdingPage = {
            "all": "all",
            "bond": "boldHoldingPage",
            "equity": "equityHoldingPage",
            "other": "otherHoldingPage",
        }
        if holdingType not in holdingType_to_holdingPage:
            raise ValueError(
                f"""parameter holdingType must take one of the following values
                : {", ".join(holdingType_to_holdingPage.keys())}"""
            )

        if holdingType == "all":
            return pd.DataFrame(
                self.position()["equityHoldingPage"]["holdingList"]
                + self.position()["boldHoldingPage"]["holdingList"]
                + self.position()["otherHoldingPage"]["holdingList"]
            )
        else:
            return pd.DataFrame(
                self.position()[holdingType_to_holdingPage[holdingType]]["holdingList"]
            )

    def investmentFee(self) -> dict:
        """
        This function retrieves the investment fees.

        Returns:
            dict investment fees

        Examples:
            >>> Funds("LU0823421689").investmentFee()

        """
        return self.GetData("price/investmentFee").json()
    
    def investmentLookup(self, 
                         currency:str="EUR") -> dict:
        """
        This function gives details about fund investment.

        Returns:
            dict fund investment

        Examples:
            >>> Funds("myria").investmentLookup()

        """
        return self.ltData("investmentTypeLookup", currency=currency)

    def investmentStrategy(self) -> dict:
        """
        This function retrieves the investment strategy.

        Returns:
            dict investment strategy

        Examples:
            >>> Funds("LU0823421689").investmentStrategy()

        """
        return self.GetData("morningstarTake/investmentStrategy").json()

    def marketCapitalization(self) -> dict:
        """
        This function retrieves the marketCapitalization breakdown of the funds,
        category and index.

        Returns:
            dict market capitalization

        Examples:
            >>> Funds("myria").marketCapitalization()

        """
        return self.GetData("process/marketCap").json()

    def maturitySchedule(self) -> dict:
        """
        This function retrieves the maturity breakdown of the funds and category.

        Returns:
            dict maturity

        Examples:
            >>> Funds("myria").maturitySchedule()

        """
        return self.GetData("process/maturitySchedule").json()

    def maxDrawDown(self, 
                    year:int=3) -> dict:
        """
        This function retrieves the max drawdown of the funds, index and category.

        Args:
            year (int) : period of calculation in year

        Returns:
            dict max drawdown

        Raises:
            TypeError whenever the parameter year is not an integer

        Examples:
            >>> Funds("myria").maxDrawDown()

        """

        if not isinstance(year, int):
            raise TypeError("year parameter should be an integer")

        return self.GetData(
            "performance/marketVolatilityMeasure", params={"year": year}
        ).json()

    def medaListComparables(self) -> dict:
        """
        This function retrieves comparable funds.

        Returns:
            dict comparable funds

        Examples:
            >>> Funds("myria").medaListComparables()

        """

        return self.GetData("medaListComparables").json()
    


    def metaData(self) -> dict:
        """
        This function retrieves meta Data about the funds.

        Returns:
            dict meta Data

        Examples:
            >>> Funds("myria").metaData()

        """

        return self.GetData("securityMetaData",url_suffix="").json()
    
    def morningstarAnalyst(self) -> dict:
        """
        This function retrieves the raiting of MorningStar analyst.

        Returns:
            dict rating

        Examples:
            >>> Funds("myria").morningstarAnalyst()

        """

        return self.GetData("morningstarAnalyst").json()
    
    def morningstarOpinion(self,
                           version:int=3) -> dict:
        """
        This function retrieves the opinion of MorningStar analyst.

        Args:
            version (int) : version of the api of morningstarOpinion shoulb be 2 or 3

        Returns:
            dict opinion

        Examples:
            >>> Funds("myria").morningstarOpinion()

        """

        if not isinstance(version,int):
            raise TypeError("version paramater should be an integer")
        
        if version not in range(2,4):
            raise ValueError("version paramater should be 2 or 3")

        return self.GetData(f"morningstarTake/v{version}",url_suffix="").json()

    def multiLevelFixedIncomeData(self, 
                                  primary:str="superEffectiveDuration", 
                                  secondary:str="superSector.weight") -> dict:
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
            >>> Funds("myria").multiLevelFixedIncomeData()

        """

        primary_choice = [
            "superEffectiveDuration",
            "superYieldToWorst",
            "creditQuality",
        ]
        secondary_choice = [
            "superSector.weight",
            "region.weight",
            "creditQuality.weight",
        ]

        if primary not in primary_choice:
            raise ValueError(
                f"""primary parameter can only take one of the 
                values : {", ".join(primary_choice)}"""
            )

        if secondary not in secondary_choice:
            raise ValueError(
                f"""secondary parameter can only take one of the values 
                : {", ".join(secondary_choice)}"""
            )

        if primary == "creditQuality" and secondary == "creditQuality.weight":
            raise ValueError(
                f"primary and secondary parameters cannot be both credit quality"
            )

        return self.GetData(
            "multiLevelFixedIncomeData",
            params={"primary": primary, "secondary": secondary},
        ).json()

    def nav(self, 
            start_date:datetime.datetime,
            end_date: datetime.datetime, 
            frequency:str="daily") -> list[dict]:
        """
        This function retrieves the NAV of the funds

        Args:
            start_date (datetime) : start date to get nav
            end_date (datetime) : end date to get nav
            frequency (str) : can be daily, weekly, monthly

        Returns:
            list of dict with nav

            >>> Funds("myria").nav(datetime.datetime.today() 
            - datetime.timedelta(30),datetime.datetime.today())

        Raises:
            TypeError: raised whenever the parameter type is not the type expected
            ValueError : raised whenever the parameter is not valid or no funds found

        """

        return self.TimeSeries(
            ["nav", "totalReturn"],
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
        )

    def otherFee(self) -> dict:
        """
        This function retrieves the other fee of the etf

        Returns:
            dict fees

        Examples:
            >>> Funds("American Century Foc Dynmc Gr ETF").otherFee()

            {'expenseWaiver': False, 'expenseReimbursement': None, 
            'expirationDate': None, 'expenseWaivers': None}

        """
        return self.GetData("price/otherFee").json()

    def ownershipZone(self) -> dict:
        """
        This function retrieves ownershipZone of the funds, index and category.

        Returns:
            dict ownershipZone

        Examples:
            >>> Funds("myria").ownershipZone()

        """

        return self.GetData("process/ownershipZone").json()

    def parentMedal(self) -> list[dict]:
        """
        This function retrieves medal funds from the asset manager.

        Returns:
            list of dict rating parent medal funds

        Examples:
            >>> Funds("myria").parentMedal()

        """

        return self.GetData("parent/medalistRating/topfunds").json()
    
    def parentMedaListRating(self) -> list[dict]:
        """
        This function retrieves summary medal funds from the asset manager.

        Returns:
            list of dict rating parent funds

        Examples:
            >>> Funds("myria").parentmedaListRating()

        """

        return self.GetData("parent/medalistRating").json()
    
    def parentMstarRating(self,
                          ) -> list[dict]:
        """
        This function retrieves the rating of asset manager funds.

        Returns:
            list of dict rating

        Examples:
            >>> Funds("myria").parentMstarRating()

        """

        return self.GetData("parent/parentMstarRating").json()
    
    def parentRatingRecentChange(self) -> list[dict]:
        """
        This function retrieves recent change in funds rating from the asset manager.

        Returns:
            list of dict rating parent funds

        Examples:
            >>> Funds("myria").parentRatingRecentChange()

        """

        return self.GetData("parent/medalistRating/topfundsUpDown").json()

    def parentSummary(self) -> dict:
        """
        This function retrieves info about the parent.

        Returns:
            dict parent info

        Examples:
            >>> Funds("myria").parentSummary()

        """
        return self.GetData("parent/parentSummary").json()

    def people(self) -> dict:
        """
        This function retrieves info about people who works in the company.

        Returns:
            dict people info

        Examples:
            >>> Funds("myria").people()

        """
        return self.GetData("people").json()
    
    def performanceTable(self) -> dict:
        """
        This function retrieves the performance of fund, catgory and index

        Returns:
            dict performance

        Examples:
            >>> Funds("myria").performanceTable()

        """
        return self.GetData("performance/table", url_suffix="").json()
    
    def position(self) -> dict:
        """
        This function retrieves the hodings of the funds.

        Returns:
            dict holdings

        Examples:
            >>> Funds("myria").position()

        """

        return self.GetData(
            "portfolio/holding/v2", params={"premiumNum": 10000, "freeNum": 10000}
        ).json()

    def proxyVotingManagement(self) :
        """
        This function retrieves the vote of management.

        Returns:
            dict vote

        Examples:
            >>> Funds("myria").proxyVotingManagement()

        """
        return self.GetData("people/proxyVoting/management").json()

    def proxyVotingShareHolder(self) -> dict:
        """
        This function retrieves the vote of shareholders.

        Returns:
            dict vote

        Examples:
            >>> Funds("myria").proxyVotingShareHolder()

        """
        return self.GetData("people/proxyVoting/shareHolder").json()

    def productInvolvement(self) -> dict:
        """
        This function retrieves the involvement of the funds

        Returns:
            dict involvement

        Examples:
            >>> Funds("myria").proxyVotingShareHolder()

        """

        return self.GetData("esg/productInvolvement").json()



    def quote(self, 
                version:int=7) -> dict:
        """
        This function retrieves general information about the funds.

        Args:
            version (int) : version of the api of historical data from 2 to 7
        
        Returns:
            dict with general information

        Examples:
            >>> Funds("myria").quote()

        """
        if not isinstance(version,int):
            raise TypeError("version paramater should be an integer")
        
        if version not in range(1,8):
            raise ValueError("version paramater should be between 2 and 7")

        return self.GetData(f"quote/v{version}").json()
    
    def regionalSector(self) -> dict:
        """
        This function retrieves the breakdown of the funds, category and index by region

        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria").regionalSector()

        """
        return self.GetData("portfolio/regionalSector").json()

    def regionalSectorIncludeCountries(self) -> dict:
        """
        This function retrieves the breakdown of the funds,
        category and index by region and country

        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria").regionalSectorIncludeCountries()

        """
        return self.GetData("portfolio/regionalSectorIncludeCountries").json()


    def repurchase(self) -> dict:
        """
        This function retrieves the repurchases 
        date and fees for a closed fund
        """
        if self.asset_type != "cef":
            return {}
        return self.GetData("repurchase").json()
    
    def riskReturnScatterplot(self) -> dict:
        """
        This function retrieves the return and standard
        deviation of the funds and category

        Returns:
            dict risk return

        Examples:
            >>> Funds("myria").riskReturnScatterplot()

        """
        return self.GetData("performance/riskReturnScatterplot").json()

    def riskReturnSummary(self) -> dict:
        """
        This function retrieves the return and risk summary 
        of the funds compare to the category

        Returns:
            dict risk return

        Examples:
            >>> Funds("myria").riskReturnSummary()

        """

        return self.GetData("performance/riskReturnSummary").json()
    
    def riskScore(self) -> dict:
        """
        This function retrieves the risk score of the fund.

        Returns:
            dict risk Score

        Examples:
            >>> Funds("myria").riskScore()

        """
        return self.GetData("performance/riskScore").json()

    def riskVolatility(self) -> dict:
        """
        This function retrieves the alpha, beta, R², 
        volatility and Sharpe ratio of the funds, category and index.

        Returns:
            dict econometrics

        Examples:
            >>> Funds("myria").riskVolatility()

        """
        return self.GetData("performance/riskVolatility").json()

    def salesFees(self) -> dict:
        """
        This function retrieves the sales fees of the funds

        Returns:
            dict fees

        Examples:
            >>> Funds("myria").salesFees()

        """
        if self.asset_type == "etf":
            return {}
        return self.GetData("price/salesFees").json()


    def sector(self, 
                version:int=2) -> dict:
        """
        This function retrieves the sector breakdown of the funds, category and index
        Args:
            version (int) : version of the api of allocation map, 1 or 2

        Returns:
            dict sector breakdown

        Examples:
            >>> Funds("myria").sector()

        """
        if not isinstance(version,int):
            raise TypeError("version paramater should be an integer")
        
        if version not in range(1,3):
            raise ValueError("version paramater should be 1 or 2")

        return self.GetData(f"portfolio/v{version}/sector").json()

    def snapshot(self, 
                 currency:str="EUR"):
        """
        This function returns a snapshot of the fund and asset manager.

        Returns:
            dict snapshot fund and asset manager

        Examples:
            >>> Funds("myria").snapshot()

        """
        return self.ltData("MFsnapshot", currency=currency)

    def starRatingFundAsc(self) -> dict:
        """
        This function retrieves the MorningStar rating of the funds
        of the company by ascending order

        Returns:
            dict rating

        Examples:
            >>> Funds("myria").starRatingFundAsc()

        """

        return self.GetData("parent/mstarRating/StarRatingFundAsc").json()

    def starRatingFundDesc(self) -> dict:
        """
        This function retrieves the MorningStar rating of the funds
        of the company by descending order

        Returns:
            dict rating

        Examples:
            >>> Funds("myria").starRatingFundDesc()

        """

        return self.GetData("parent/mstarRating/StarRatingFundDesc").json()


    def strategyPreview(self) -> dict:
        """
        This function retrieves general information and return on funds

        Returns:
            dict returns and general information

        Examples:
            >>> Funds("myria").strategyPreview()

        """
        return self.GetData("strategyPreview").json()
    
    def sustainability(self, 
                       currency:str="EUR") -> dict:
        """
        This function retrieves the sustainability data of the fund.

        Returns:
            dict sustanability data

        Examples:
            >>> Funds("myria").sustainability()

        """
        return self.ltData("sustainability", currency=currency)

    def taxes(self) -> dict:
        """
        This function retrieves the other fee of the etf

        Returns:
            dict taxes

        Examples:
            >>> Funds("American Century Foc Dynmc Gr ETF").taxes()

        """
        return self.GetData("price/taxes").json()


    def trailingReturn(self, 
                       duration:str="daily", 
                       version:int=3) -> dict:
        """
                This function retrieves the trailing return of the funds of the company.

        Args:
        duration (str) : frequency of return can be daily, monthly or quarterly
        version (int) : version of the api of historical data from 1 to 3

        Returns:
            dict trailing return

        Raises:
            ValueError whenever the parameter duration is not daily, monthly or quarterly

        Example:
            >>> Funds("myria").trailingReturn("daily")

        """

        if not isinstance(duration,str):
            raise TypeError("duration paramater should be a string")
        
        if not isinstance(version,int):
            raise TypeError("version paramater should be an integer")
        
        if version not in range(1,4):
            raise ValueError("version paramater should be between 1 and 3")
        
        duration_choice = ["daily", "monthly", "quarterly"]
        if duration not in duration_choice:
            raise ValueError(
                f'duration parameter can only take one of the values: {", ".join(duration_choice)}'
            )

        return self.GetData(f"trailingReturn/v{version}", {"duration": duration}).json()

