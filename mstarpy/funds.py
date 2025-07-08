""" class funds """
import pandas as pd
import datetime

from .search import screener_universe
from .security import Security


class Funds(Security):
    """
    Main class to access data about funds and etf, inherit from Security class

    Args:
        term (str): text to find a fund, can be a name, part of a name or the isin of the funds
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
        term=None,
        filters:dict=None,
        itemRange:int=0,
        pageSize:int=10,
        page:int=1,
        sortby:str=None,
        ascending:bool=True,
        proxies:dict=None,
    ) -> None:
        
        fund_filter = {"investmentType" : ['FE', 'FO']}
        if filters:
            fund_filter = fund_filter | filters
        
        super().__init__(
            term=term,
            asset_type="fund",
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

        return self.GetData(f"process/asset/v{version}")
    

    def allocationWeighting(self) -> dict:
        """
        This function retrieves the Growth/Blend/Value and
        market capitalizaton allocation size of the funds.

        Returns:
            dict with allocation

        Examples:
            >>> Funds("myria").allocationWeighting()

        """
        return self.GetData("process/weighting")

    def analystRating(self) -> list[dict]:
        """
        This function retrieves the rating of the funds

        Returns:
            list of dict with ratings

            >>> Funds("myria").analystRating()

        """

        return self.GetData("parent/analystRating")

    def analystRatingTopFunds(self) -> dict:
        """
        This function retrieves the rating Top funds

        Returns:
            dict with ratings

            >>> Funds("myria").analystRatingTopFunds()

        """

        return self.GetData("parent/analystRating/topfunds")

    def analystRatingTopFundsUpDown(self) -> dict:
        """
        This function retrieves the rating funds Up Down

        Returns:
            dict with ratings

            >>> Funds("myria").analystRatingTopFundsUpDown()

        """

        return self.GetData("parent/analystRating/topfundsUpDown")

    def benchmark(self) -> str:
        """
        This function retrieves the benchmark name of the funds.

        Returns:
            str benchmark name

        Examples:
            >>> Funds("myria").benchmark()

        """
        return self.referenceIndex("benchmark")

    def carbonMetrics(self) -> dict:
        """
        This function retrieves the carbon metrics of the funds.

        Returns:
            dict with carbon metrics

        Examples:
            >>> Funds("myria").carbonMetrics()

        """

        return self.GetData("esg/carbonMetrics")

    def category(self) -> str:
        """
        This function retrieves the category name of the funds.

        Returns:
            str category name

        Examples:
            >>> Funds("myria").category()

        """
        return self.referenceIndex("category")

    def costIllustration(self) -> dict:
        """
        This function retrieves the cost of the funds.

        Returns:
            dict cost of funds

        Examples:
            >>> Funds("FOUSA00E5P").costIllustration()

        """
        return self.GetData("price/costIllustration")
    
    def costProjection(self) -> dict:
        """
        This function retrieves performance with the cost projection.

        Returns:
            dict performance with cost projection

        Examples:
            >>> Funds("FOUSA00E5P").costProjection()

        """
        return self.GetData("price/costProjection")

    def couponRange(self)  :
        """
        This function retrieves the coupon of the funds, index and category.

        Returns:
            dict coupon

        Examples:
            >>> Funds("myria").couponRange()

        """
        return self.GetData("process/couponRange")

    def creditQuality(self) -> dict:
        """
        This function retrieves the credit notation of the funds, index and category.

        Returns:
            dict credit notation

        Examples:
            >>> Funds("myria").creditQuality()

        """
        return self.GetData("portfolio/creditQuality")

    def dataPoint(self, 
                  field:str|list, 
                  currency:str="EUR") -> list[dict]:
        """
        This function retrieves infos about funds such as name,
        performance, risk metrics...

        Args:
        field (str or list) : field to find
        currency (str) : currency in 3 letters

        Returns:
            list of dict funds infos

        Example:
            >>> Funds("myria").dataPoint(['largestSector', 'Name', 'ongoingCharge'])
            >>> Funds("myria").dataPoint('SharpeM36')

        """
        return screener_universe(
            self.code, field, proxies=self.proxies
        )

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

        return self.GetData(f"distribution/{period}")

    def equityStyle(self) -> dict:
        """
        This function retrieves the equity style of the funds and category.

        Returns:
            dict equity style

        Examples:
            >>> Funds("myria").equityStyle()

        """
        return self.GetData("process/stockStyle/v2")

    def equityStyleBoxHistory(self) -> dict:
        """
        This function retrieves the equity style history of the funds

        Returns:
            dict equity style history

        Examples:
            >>> Funds("myria").equityStyleBoxHistory()

        """
        return self.GetData("process/equityStyleBoxHistory")

    def esgData(self) -> dict:
        """
        This function retrieves ESG data of the funds and category

        Returns:
            dict ESG data

        Examples:
            >>> Funds("myria").esgData()

        """

        return self.GetData("esg/v1")
    
    def esgRisk(self) -> dict:
        """
        This function retrieves ESG drisk of the funds and category

        Returns:
            dict ESG risk

        Examples:
            >>> Funds("myria").esgRisk()

        """

        return self.GetData("esgRisk")

    def factorProfile(self) -> dict:
        """
        This function retrieves the factor profile of the funds, index and category

        Returns:
            dict factor profile

        Examples:
            >>> Funds("myria").factorProfile()

        """
        return self.GetData("factorProfile")

    def feeLevel(self)  :
        """
        This function retrieves the fees of the fund compare to its category.

        Returns:
            dict fees

        Examples:
            >>> Funds("myria").feeLevel()

        """
        return self.GetData("price/feeLevel/v1")

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
        return self.GetData("process/financialMetrics")

    def fixedIncomeStyle(self) -> dict:
        """
        This function retrieves the fixed income style of the funds and category.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("myria").fixedIncomeStyle()

        """

        return self.GetData("process/fixedIncomeStyle")

    def fixedincomeStyleBoxHistory(self) -> dict:
        """
        This function retrieves the fixed income style history of the funds.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("myria").fixedincomeStyleBoxHistory()

        """
        return self.GetData("process/fixedincomeStyleBoxHistory")

    def graphData(self) -> dict:
        """
        This function retrieves historical data of the funds.

        Returns:
            dict historical data

        Examples:
            >>> Funds("myria").graphData()

        """

        return self.GetData("parent/graphData")

    def historicalData(self, 
                       version:int=5) -> dict:
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
        
        if version not in range(2,6):
            raise ValueError("version paramater should be between 2 and 5")

        return self.GetData(f"performance/v{version}", url_suffix="")

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
        return self.GetData("price/historicalExpenses")
    
    def historicalRating(self) -> dict:
        """
        This function retrieves MorningStar historical rating of the fund.

        Returns:
            dict historical rating

        Examples:
            >>> Funds("myria").historicalRating()

        """

        return self.GetData("morningstarTake/historicalRating")

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
                f"""parameter holdingType must take one of the following value
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
        return self.GetData("price/investmentFee")
    
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
        return self.GetData("morningstarTake/investmentStrategy")

    def marketCapitalization(self) -> dict:
        """
        This function retrieves the marketCapitalization breakdown of the funds,
        category and index.

        Returns:
            dict market capitalization

        Examples:
            >>> Funds("myria").marketCapitalization()

        """
        return self.GetData("process/marketCap")

    def maturitySchedule(self) -> dict:
        """
        This function retrieves the maturity breakdown of the funds and category.

        Returns:
            dict maturity

        Examples:
            >>> Funds("myria").maturitySchedule()

        """
        return self.GetData("process/maturitySchedule")

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
        )

    def medaListComparables(self) -> dict:
        """
        This function retrieves comparable funds.

        Returns:
            dict comparable funds

        Examples:
            >>> Funds("myria").medaListComparables()

        """

        return self.GetData("medaListComparables")
    


    def metaData(self) -> dict:
        """
        This function retrieves meta Data about the funds.

        Returns:
            dict meta Data

        Examples:
            >>> Funds("myria").metaData()

        """

        return self.GetData("securityMetaData",url_suffix="")
    
    def morningstarAnalyst(self) -> dict:
        """
        This function retrieves the raiting of MorningStar analyst.

        Returns:
            dict rating

        Examples:
            >>> Funds("myria").morningstarAnalyst()

        """

        return self.GetData("morningstarAnalyst")
    
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

        return self.GetData(f"morningstarTake/v{version}",url_suffix="")

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
        )

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
        return self.GetData("price/otherFee")

    def ownershipZone(self) -> dict:
        """
        This function retrieves ownershipZone of the funds, index and category.

        Returns:
            dict ownershipZone

        Examples:
            >>> Funds("myria").ownershipZone()

        """

        return self.GetData("process/ownershipZone")

    def parentMedal(self) -> list[dict]:
        """
        This function retrieves medal funds from the asset manager.

        Returns:
            list of dict rating parent medal funds

        Examples:
            >>> Funds("myria").parentMedal()

        """

        return self.GetData("parent/medalistRating/topfunds")
    
    def parentMedaListRating(self) -> list[dict]:
        """
        This function retrieves summary medal funds from the asset manager.

        Returns:
            list of dict rating parent funds

        Examples:
            >>> Funds("myria").parentmedaListRating()

        """

        return self.GetData("parent/medalistRating")
    
    def parentMstarRating(self,
                          ) -> list[dict]:
        """
        This function retrieves the rating of asset manager funds.

        Returns:
            list of dict rating

        Examples:
            >>> Funds("myria").parentMstarRating()

        """

        return self.GetData("parent/parentMstarRating")
    
    def parentRatingRecentChange(self) -> list[dict]:
        """
        This function retrieves recent change in funds rating from the asset manager.

        Returns:
            list of dict rating parent funds

        Examples:
            >>> Funds("myria").parentRatingRecentChange()

        """

        return self.GetData("parent/medalistRating/topfundsUpDown")

    def parentSummary(self) -> dict:
        """
        This function retrieves info about the parent.

        Returns:
            dict parent info

        Examples:
            >>> Funds("myria").parentSummary()

        """
        return self.GetData("parent/parentSummary")

    def people(self) -> dict:
        """
        This function retrieves info about people who works in the company.

        Returns:
            dict people info

        Examples:
            >>> Funds("myria").people()

        """
        return self.GetData("people")
    
    def performanceTable(self) -> dict:
        """
        This function retrieves the performance of fund, catgory and index

        Returns:
            dict performance

        Examples:
            >>> Funds("myria").performanceTable()

        """
        return self.GetData("performance/table", url_suffix="")
    
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
        )

    def proxyVotingManagement(self) :
        """
        This function retrieves the vote of management.

        Returns:
            dict vote

        Examples:
            >>> Funds("myria").proxyVotingManagement()

        """
        return self.GetData("people/proxyVoting/management")

    def proxyVotingShareHolder(self) -> dict:
        """
        This function retrieves the vote of shareholders.

        Returns:
            dict vote

        Examples:
            >>> Funds("myria").proxyVotingShareHolder()

        """
        return self.GetData("people/proxyVoting/shareHolder")

    def productInvolvement(self) -> dict:
        """
        This function retrieves the involvement of the funds

        Returns:
            dict involvement

        Examples:
            >>> Funds("myria").proxyVotingShareHolder()

        """

        return self.GetData("esg/productInvolvement")



    def quote(self, 
                version:int=7) -> dict:
        """
        This function retrieves general information about the funds.

        Args:
            version (int) : version of the api of historical data from 2 to 7
        
        Returns:
            dict with general information

        Examples:
            >>> Funds("myria").historicalData()

        """
        if not isinstance(version,int):
            raise TypeError("version paramater should be an integer")
        
        if version not in range(1,8):
            raise ValueError("version paramater should be between 2 and 7")

        return self.GetData(f"quote/v{version}")
    
    def regionalSector(self) -> dict:
        """
        This function retrieves the breakdown of the funds, category and index by region

        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria").regionalSector()

        """
        return self.GetData("portfolio/regionalSector")

    def regionalSectorIncludeCountries(self) -> dict:
        """
        This function retrieves the breakdown of the funds,
        category and index by region and country

        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria").regionalSectorIncludeCountries()

        """
        return self.GetData("portfolio/regionalSectorIncludeCountries")

    def riskReturnScatterplot(self) -> dict:
        """
        This function retrieves the return and standard
        deviation of the funds and category

        Returns:
            dict risk return

        Examples:
            >>> Funds("myria").riskReturnScatterplot()

        """
        return self.GetData("performance/riskReturnScatterplot")

    def riskReturnSummary(self) -> dict:
        """
        This function retrieves the return and risk summary 
        of the funds compare to the category

        Returns:
            dict risk return

        Examples:
            >>> Funds("myria").riskReturnSummary()

        """

        return self.GetData("performance/riskReturnSummary")
    
    def riskScore(self) -> dict:
        """
        This function retrieves the risk score of the fund.

        Returns:
            dict risk Score

        Examples:
            >>> Funds("myria").riskScore()

        """
        return self.GetData("performance/riskScore")

    def riskVolatility(self) -> dict:
        """
        This function retrieves the alpha, beta, R², 
        volatility and Sharpe ratio of the funds, category and index.

        Returns:
            dict econometrics

        Examples:
            >>> Funds("myria").riskVolatility()

        """
        return self.GetData("performance/riskVolatility")

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
        return self.GetData("price/salesFees")


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

        return self.GetData(f"portfolio/v{version}/sector")

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

        return self.GetData("parent/mstarRating/StarRatingFundAsc")

    def starRatingFundDesc(self) -> dict:
        """
        This function retrieves the MorningStar rating of the funds
        of the company by descending order

        Returns:
            dict rating

        Examples:
            >>> Funds("myria").starRatingFundDesc()

        """

        return self.GetData("parent/mstarRating/StarRatingFundDesc")


    def strategyPreview(self) -> dict:
        """
        This function retrieves general information and return on funds

        Returns:
            dict returns and general information

        Examples:
            >>> Funds("myria").strategyPreview()

        """
        return self.GetData("strategyPreview")
    
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
        return self.GetData("price/taxes")


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

        return self.GetData(f"trailingReturn/v{version}", {"duration": duration})

