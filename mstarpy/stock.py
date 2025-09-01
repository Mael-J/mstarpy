from .security import Security
import datetime

class Stock(Security):
    """
    Main class to access data about stocks, inherit from Security class
    Args:
        term (str): text to find a stock, can be a name, part of a name or the isin of the stocks
        language (str): language of the data, default is "en-gb"
        filters (dict) : filter, use the method search_filter() to find the different possible filter keys
        itemRange (int) : index of stocks to return (must be inferior to PageSize)
        pageSize (int): number of securities to return
        page (int): page to return
        sortby (str) : sort by a field
        ascending (bool) : True sort by ascending order, False sort by descending order
        proxies (dict) : set the proxy if needed , example : {"http": "http://host:port","https": "https://host:port"}

    Examples:
        >>> Stock("ab",page=5, pageSize=5,itemRange=0,sortby="name", ascending=False)
        >>> Stock('US0378331005')

    Raises:
        TypeError: raised whenever the parameter type is not the type expected
        ValueError : raised whenever the parameter is not valid or no stock found

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
        
        stock_filter = {"investmentType" : 'EQ'}
        if filters:
            stock_filter = stock_filter | filters

        super().__init__(
            term=term,
            asset_type="stock",
            language=language,
            filters=stock_filter,
            itemRange=itemRange,
            pageSize=pageSize,
            page=page,
            sortby=sortby,
            ascending=ascending,
            proxies=proxies,
        )

    def analysisData(self) -> dict:
        """
        This function retrieves general data about the stock.

        Returns:
            dict with general data about stock

        Examples:
            >>> Stock("US0378331005").analysisData()

        """
        return self.GetData("morningstarTake/v3", url_suffix="analysisData").json()

    def analysisReport(self) -> dict:
        """
        This function retrieves the analysis of the stock.

        Returns:
            dict with analyst overview

        Examples:
            >>> Stock("US0378331005").analysisReport()

        """
        return self.GetData("morningstarTake/v4", url_suffix="analysisReport").json()

    def balanceSheet(self, 
                     period:str="annual",
                     reportType:str="original",
                     export:bool=False,
                     folderPath:str="."
                     ) -> dict:
        """
        This function retrieves the balance sheet.

        Args:
            period (str) : possible values are annual, quarterly
            reportType (str) : possible values are original, restated
            export (bool) : if True, the file is downloaded in the folderPath
            folderPath (str) : path to save the file if export is True

        Returns:
            dict with balance sheet

        Examples:
            >>> Stock("US0378331005").balanceSheet('quarterly', 'original')
            >>> Stock("US0378331005").balanceSheet('annual', 'restated')

        """

        return self.financialStatement(
            "balancesheet", 
            period=period, 
            reportType=reportType,
            export=export,
            folderPath=folderPath
        )

    def boardOfDirectors(self) -> dict:
        """
        This function retrieves information about the board of directors.

        Returns:
            dict with board of directors information

        Examples:
            >>> Stock("Alphabet Inc Class A").boardOfDirectors()

        """
        return self.GetData("insiders/boardOfDirectors").json()

    def cashFlow(self, 
                 period:str="annual",
                 reportType:str="original",
                 export:bool=False,
                 folderPath:str="."
                 ) -> dict:
        """
        This function retrieves the cash flow.

        Args:
            period (str) : possible values are annual, quarterly
            reportType (str) : possible values are original, restated
            export (bool) : if True, the file is downloaded in the folderPath
            folderPath (str) : path to save the file if export is True

        Returns:
            dict with cash flow

        Examples:
            >>> Stock("US0378331005").cashFlow('annual', 'restated')
            >>> Stock("US0378331005").cashFlow('quarterly', 'restated')

        """

        return self.financialStatement("cashflow", 
                                       period=period, 
                                       reportType=reportType,
                                       export=export,
                                       folderPath=folderPath)


    def companyProfile(self) -> dict:
        """
        This function retrieves the company profile

        Returns:
            dict with company information

        Examples:
            >>> Stock("US0378331005").companyProfile()

        """
        return self.GetData("companyProfile", url_suffix="").json()

    def dividends(self) -> dict:
        """
        This function retrieves the dividends of the stock.

        Returns:
            dict with dividends

        Examples:
            >>> Stock("US0378331005").dividends()

        """
        return self.GetData("dividends/v4").json()

    def esgRisk(self) -> dict:
        """
        This function retrieves the esg risk of the stock.

        Returns:
            dict with esg risk

        Examples:
            >>> Stock("US0378331005").esgRisk()

        """
        return self.GetData("esgRisk").json()
    
    def financialHealth(self) -> dict:
        """
        This function retrieves the financial health of the stock.

        Returns:
            dict with financial health

        Examples:
            >>> Stock("US0378331005").financialHealth()

        """
        return self.GetData("keyMetrics/financialHealth", url_suffix="").json()

    def financialStatement(
        self, 
        statement:str="summary",
        period:str="annual",
        reportType:str="original",
        export:bool=False,
        folderPath:str="."
    ) -> dict:
        """
        This function retrieves the financial statement or downloads it as a xls file.

        Args:
            statement (str) : possible values are balancesheet, cashflow, incomestatement, summary
            period (str) : possible values are annual, quarterly
            reportType (str) : possible values are original, restated
            export (bool) : if True, the file is downloaded in the folderPath
            folderPath (str) : path to save the file if export is True

        Returns:
            dict with financial statement

        Examples:
            >>> Stock("US0378331005").financialStatement('summary', 'quarterly', 'original')
            >>> Stock("US0378331005").financialStatement('cashflow', 'annual', 'restated')
            >>> Stock("US0378331005").financialStatement('balancesheet', 'annual', 'restated')
            >>> Stock("US0378331005").financialStatement('incomestatement', 'annual', 'restated')

        """

        if not isinstance(statement, str):
            raise TypeError("statement parameter should be a string")

        if not isinstance(period, str):
            raise TypeError("period parameter should be a string")

        if not isinstance(reportType, str):
            raise TypeError("reportType parameter should be a string")
        
        if not isinstance(export, bool):
            raise TypeError("export parameter should be a boolean")
        
        if not isinstance(folderPath, str):
            raise TypeError("folderPath parameter should be a string")

        statement_choice = {
            "balancesheet": "balanceSheet",
            "cashflow": "cashFlow",
            "incomestatement": "incomeStatement",
            "summary": "summary",
        }

        period_choice = {"annual": "A", "quarterly": "Q"}

        reportType_choice = {"original": "A", "restated": "R"}

        if statement not in statement_choice:
            raise ValueError(
                f"statement parameter must take one of the following value : { ', '.join(statement_choice)}"
            )

        if period not in period_choice:
            raise ValueError(
                f"period parameter must take one of the following value : { ', '.join(period_choice)}"
            )

        if reportType not in reportType_choice:
            raise ValueError(
                f"reportType parameter must take one of the following value : { ', '.join(reportType_choice.keys())}"
            )
        


        params = {"reportType": reportType_choice[reportType]}

        if export:
            params["operation"] = "export"

        if statement == "summary":
            response = self.GetData(
                "newfinancials", params=params, url_suffix=f"{period}/summary"
            )

        params["dataType"] = period_choice[period]

        response = self.GetData(
            "newfinancials",
            params=params,
            url_suffix=f"{statement_choice[statement]}/detail",
        )

        if not export:
            return response.json()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fileName = f"{statement_choice[statement]}-{self.code}-{timestamp}.xls"
        with open(f"{folderPath}/{fileName}", "wb") as f:
            f.write(response.content)

        return {"status" : response.status_code, 
                "mesage" : "File downloaded", 
                "filename" : fileName,
                "folder" : folderPath}

    def financialSummary(self, 
                         period:str="annual", 
                         reportType:str="original",
                        ) -> dict:
        """
        This function retrieves the financial statement summary.

        Args:
            period (str) : possible values are annual, quarterly
            reportType (str) : possible values are original, restated
            export (bool) : if True, the file is downloaded in the folderPath
            folderPath (str) : path to save the file if export is True

        Returns:
            dict with financial statement summary

        Examples:
            >>> Stock("US0378331005").financialSummary('quarterly', 'original')
            >>> Stock("US0378331005").financialSummary('annual', 'restated')

        """

        return self.financialStatement("summary", 
                                       period=period, 
                                       reportType=reportType)

    def freeCashFlow(self) -> dict:
        """
        This function retrieves the free cash flow.

        Returns:
            dict with free cash flow

        Examples:
            >>> Stock("US0378331005").freeCashFlow()

        """
        return self.GetData("keyMetrics/cashFlow", url_suffix="").json()

    def historical(self,
                   start_date:datetime.datetime, 
                   end_date:datetime.datetime, 
                   frequency:str="daily") -> list:
        """
        This function retrieves the historical price, volume and dividends of the stock.

        Args:
            start_date (datetime) : start date to get history
            end_date (datetime) : end date to get history
            frequency (str) : can be daily, weekly, monthly

        Returns:
            list of dict with price, volume and dividend

        Examples:
            >>> Stock("US0378331005").history(datetime.datetime.today()- datetime.timedelta(30),datetime.datetime.today())

        """
        return self.TimeSeries(
            ["open", "high", "low", "close", "volume", "previousClose", "dividend"],
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
        )

    def incomeStatement(self, 
                        period:str="annual", 
                        reportType:str="original",
                        export:bool=False,
                        folderPath:str="."
                        ) -> dict:
        """
        This function retrieves the income statement.

        Args:
            period (str) : possible values are annual, quarterly
            reportType (str) : possible values are original, restated
            export (bool) : if True, the file is downloaded in the folderPath
            folderPath (str) : path to save the file if export is True

        Returns:
            dict with income statement

        Examples:
            >>> Stock("US0378331005").incomeStatement('quarterly', 'original')
            >>> Stock("US0378331005").incomeStatement('annual', 'restated')

        """

        return self.financialStatement(
            "incomestatement", 
            period=period, 
            reportType=reportType,
            export=export,
            folderPath=folderPath
            )

    def institutionBuyers(self,
                          top:int=20) -> dict:
        """
        This function retrieves the institutions which buy the stock.

        Args:
            top (int) : number of institutions to return
        Returns:
            dict with the buyers

        Examples:
            >>> Stock("US0378331005").institutionBuyers(top=50)

        """

        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData(
            "ownership/v1", url_suffix=f"Buyers/institution/{top}/data"
        ).json()

    def institutionConcentratedOwners(self, 
                                      top:int=20) -> dict:
        """
        This function retrieves the institutions which are concentrated on the stock.

        Args:
            top (int) : number of institutions to return
        Returns:
            dict with the concentarted owners

        Examples:
            >>> Stock("US0378331005").institutionConcentratedOwners(top=50)

        """

        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData(
            "ownership/v1", url_suffix=f"ConcentratedOwners/institution/{top}/data"
        ).json()

    def institutionOwnership(self, 
                             top:int=20) -> dict:
        """
        This function retrieves the main institutions which own the stock.

        Args:
            top (int) : number of institutions to return
        Returns:
            dict with the main owners

        Examples:
            >>> Stock("US0378331005").institutionOwnership(top=50)

        """

        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData(
            "ownership/v1", url_suffix=f"OwnershipData/institution/{top}/data"
        ).json()

    def institutionSellers(self, 
                           top:str=20) -> dict:
        """
        This function retrieves the institutions which sell on the stock.

        Args:
            top (int) : number of institutions to return
        Returns:
            dict with sellers

        Examples:
            >>> Stock("US0378331005").institutionSellers(top=50)

        """
        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData(
            "ownership/v1", url_suffix=f"Sellers/institution/{top}/data"
        ).json()

    def keyExecutives(self) -> dict:
        """
        This function retrieves information oabout key excutives of the company.

        Returns:
            dict with key executives information

        Examples:
            >>> Stock("US0378331005").keyExecutives()

        """
        return self.GetData("insiders/keyExecutives").json()

    def keyMetricsSummary(self, 
                          reportType:str="original") -> dict:
        """
        This function retrieves the key metrics summary

        Args:
            reportType (str) : possible values are original, restated

        Returns:
            dict with key metrics summary

        Examples:
            >>> Stock("US0378331005").keyMetricsSummary()

        """
        if not isinstance(reportType, str):
            raise TypeError("reportType parameter should be a string")
        
        reportType_choice = {"original": "A", "restated": "R"}

        if reportType not in reportType_choice:
            raise ValueError(
                f"reportType parameter must take one of the following value : { ', '.join(reportType_choice.keys())}"
            )

        params = {"reportType": reportType_choice[reportType]}

        return self.GetData("keyMetrics/summary",
                             params=params,
                            url_suffix="").json()

    def keyRatio(self) -> dict:
        """
        This function retrieves the key ratio of the stock.

        Returns:
            dict with key ratio

        Examples:
            >>> Stock("US0378331005").keyRatio()

        """
        return self.GetData("keyratios").json()

    def mutualFundBuyers(self,
                         top:int=20) -> dict:
        """
        This function retrieves the mutual funds which buy the stock.

        Args:
            top (int) : number of mutual funds to return
        Returns:
            dict with the buyers

        Examples:
            >>> Stock("US0378331005").mutualFundBuyers(top=50)

        """

        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData("ownership/v1", url_suffix=f"Buyers/mutualfund/{top}/data").json()

    def mutualFundConcentratedOwners(self, 
                                     top:int=20) -> dict:
        """
        This function retrieves the mutual funds which are concentrated on the stock.

        Args:
            top (int) : number of mutual funds to return
        Returns:
            dict with the concentarted owners

        Examples:
            >>> Stock("US0378331005").mutualFundConcentratedOwners(top=50)

        """

        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData(
            "ownership/v1", url_suffix=f"ConcentratedOwners/mutualfund/{top}/data"
        ).json()

    def mutualFundOwnership(self, 
                            top:int=20) -> dict:
        """
        This function retrieves the main mutual funds which own the stock.

        Args:
            top (int) : number of mutual funds to return
        Returns:
            dict with the main owners

        Examples:
            >>> Stock("US0378331005").mutualFundOwnership(top=50)

        """

        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData(
            "ownership/v1", url_suffix=f"OwnershipData/mutualfund/{top}/data"
        ).json()

    def mutualFundSellers(self,
                          top:int=20) -> dict:
        """
        This function retrieves the mutual funds which sell on the stock.

        Args:
            top (int) : number of mutual funds to return
        Returns:
            dict with sellers

        Examples:
            >>> Stock("US0378331005").mutualFundSellers(top=50)

        """

        if not isinstance(top, int):
            raise TypeError("top parameter should be an integer")

        return self.GetData(
            "ownership/v1", url_suffix=f"Sellers/mutualfund/{top}/data"
        ).json()

    def operatingGrowth(self) -> dict:
        """
        This function retrieves the operating growth of the stock.

        Returns:
            dict with operating growth

        Examples:
            >>> Stock("US0378331005").operatingGrowth()

        """
        return self.GetData("keyStats/growthTable", url_suffix="").json()
    
    def overview(self) -> dict:
        """
        This function retrieves stock overview.

        Returns:
            dict with stock overview

        Examples:
            >>> Stock("US0378331005").overview()

        """
        return self.GetData("equityOverview").json()


    def profitability(self) -> dict:
        """
        This function retrieves the profitability of the stock.

        Returns:
            dict with profitability ratios

        Examples:
            >>> Stock("US0378331005").profitability()

        """
        return self.GetData("keyMetrics/profitabilityAndEfficiency", url_suffix="").json()

    def sustainability(self) -> dict:
        """
        This function retrieves the sustainability of the stock.

        Returns:
            dict with sustainability

        Examples:
            >>> Stock("US0378331005").sustainability()

        """
        return self.GetData("esgRisk/sustainability").json()
    
    def split(self) -> dict:
        """
        This function retrieves the split history of the stock.

        Returns:
            dict with split history

        Examples:
            >>> Stock("US0378331005").split()

        """
        return self.GetData("split/v1").json()

    def tradingInformation(self) -> dict:
        """
        This function retrieves the trading information of the stock
        such as Previous Close Price, Day Range, 52-Week Range, Bid/Ask,
        Market Cap, Volume/Avg
        Returns:
            dict with performance
        Examples:
            >>> Stock("US0378331005").tradingInformation()

        """
        return self.RealtimeData("quotes")
    
    def trailingTotalReturn(self) -> dict:
        """
        This function retrieves the performance of the stock and its index.

        Returns:
            dict with performance

        Examples:
            >>> Stock("US0378331005").trailingTotalReturn()

        """
        return self.GetData("trailingTotalReturns").json()

    def transactionHistory(self) -> list:
        """
        This function retrieves the transaction of key people.

        Returns:
            list o dict of transaction of key people

        Examples:
            >>> Stock("US0378331005").transactionHistory()

        """
        return self.GetData("insiders/transactionHistory").json()

    def transactionSummary(self) -> list:
        """
        This function retrieves the summuary of transactions of key people.

        Returns:
            list of dict with transactions

        Examples:
            >>> Stock("US0378331005").transactionSummary()

        """
        return self.GetData("insiders/transactionChart").json()

    def valuation(self) -> dict:
        """
        This function retrieves the valution of the stock.

        Returns:
            dict with valuation

        Examples:
            >>> Stock("US0378331005").valuation()

        """
        return self.GetData("valuation/v3", url_suffix="").json()
    
