""" class funds """

import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime

from .error import no_site_error, not_200_response
from .search import screener_universe, token_investment_strategy
from .utils import random_user_agent

from .security import Security


class Funds(Security):
    """
    Main class to access data about funds and etf, inherit from Security class

    Args:
        term (str): text to find a fund, can be a name, part of a name or the isin of the funds
        country (str) : text for code ISO 3166-1 alpha-2 of country, should be '' for etf
        pageSize (int): number of funds to return
        itemRange (int) : index of funds to return (must be inferior to PageSize)
        proxies = (dict) : set the proxy if needed ,
        example : {"http": "http://host:port","https": "https://host:port"}

    Examples:
        >>> Funds('0P0000712R', "ca", 9, 0)
        >>> Funds('bond', "uk", 25, 2)

    Raises:
        TypeError: raised whenever the parameter type is not the type expected
        ValueError : raised whenever the parameter is not valid or no fund found

    """

    def __init__(
        self,
        term=None,
        country:str="",
        pageSize:int=1,
        itemRange:int=0,
        filters:dict=None,
        proxies:dict=None,
    ) -> None:
        
        fund_filter = {"investmentType" : ['FE', 'FO']}
        if filters:
            fund_filter = fund_filter | filters
        
        super().__init__(
            term=term,
            asset_type="fund",
            country=country,
            pageSize=pageSize,
            itemRange=itemRange,
            filters=fund_filter,
            proxies=proxies,
        )

    def allocationMap(self) -> dict:
        """
        This function retrieves the asset allocation of the funds, index and category.

        Returns:
            dict with allocation map

        Examples:
            >>> Funds("myria", "fr").allocationMap()

        """
        return self.GetData("process/asset/v2")

    def allocationWeighting(self) -> dict:
        """
        This function retrieves the Growth/Blend/Value and
        market capitalizaton allocation size of the funds.

        Returns:
            dict with allocation

        Examples:
            >>> Funds("myria", "fr").allocationWeighting()

        """
        return self.GetData("process/weighting")

    def analystRating(self) -> list[dict]:
        """
        This function retrieves the rating of the funds

        Returns:
            list of dict with ratings

            >>> Funds("RMAGX", "us").analystRating()

        """

        return self.GetData("parent/analystRating")

    def analystRatingTopFunds(self) -> dict:
        """
        This function retrieves the rating Top funds

        Returns:
            dict with ratings

            >>> Funds("RMAGX", "us").analystRatingTopFunds()

        """

        return self.GetData("parent/analystRating/topfunds")

    def analystRatingTopFundsUpDown(self) -> dict:
        """
        This function retrieves the rating funds Up Down

        Returns:
            dict with ratings

            >>> Funds("RMAGX", "us").analystRatingTopFundsUpDown()

        """

        return self.GetData("parent/analystRating/topfundsUpDown")



    def AnnualPerformance(self, 
                          cat:str) -> dict:
        """
        This function retrieves the annual performance of the funds,
        index, category or the annual rank of the funds.

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

        """

        if not isinstance(cat, str):
            raise TypeError("cat parameter should be a string")
        
        no_site_error(self.code, self.name, self.country, self.site)

        cat_row = {"funds": 0, "category": 1, "index": 2, "rank": 3}
        if cat not in cat_row:
            raise ValueError(
                f"cat parameter must take one of the following value : { ', '.join(cat_row.keys())}"
            )

        result = {}
        # headers random agent
        headers = {"user-agent": random_user_agent()}
        # page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx"
        #params of the request
        params = {
                    "id": self.code,
                    "tab": "1"
                  }
        
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        not_200_response(url, response)
        soup = BeautifulSoup(response.text, "html.parser")
        # label are dates
        regex = re.compile(".*heading number")
        label_list = soup.find(id="returnsCalenderYearDiv").find_all(
            "td", {"class": regex}
        )
        # funds performance, category performance, index performance, rank in category
        regex = re.compile(".*value number")
        # values
        value_list = soup.find(id="returnsCalenderYearDiv").find_all(
            "td", {"class": regex}
        )

        regex = re.compile("-|\/")
        # first col is nothing
        for i in range(1, len(label_list)):
            label = label_list[i].text
            # if today

            if regex.search(label):
                label = "current"
            # add category to label
            if label:

                result[f"{cat}_annual_performance_{label}"] = value_list[
                    i + (cat_row[cat]) * (len(label_list) - 1) - 1
                ].text

        return result

    def benchmark(self) -> str:
        """
        This function retrieves the benchmark name of the funds.

        Returns:
            str benchmark name

        Examples:
            >>> Funds("myria", "fr").benchmark()

        """
        return self.referenceIndex("benchmark")

    def carbonMetrics(self) -> dict:
        """
        This function retrieves the carbon metrics of the funds.

        Returns:
            dict with carbon metrics

        Examples:
            >>> Funds("myria", "fr").carbonMetrics()

        """

        return self.GetData("esg/carbonMetrics")

    def category(self) -> str:
        """
        This function retrieves the category name of the funds.

        Returns:
            str category name

        Examples:
            >>> Funds("myria", "fr").category()

        """
        return self.referenceIndex("category")

    def categoryAnnualPerformance(self) -> dict:
        """
        This function retrieves the annual performance of the category.

        Returns:
            dict annual performance of the category


        Examples:
            >>> Funds("myria", "fr").categoryAnnualPerformance()

        """

        return self.AnnualPerformance("category")

    def categoryCumulativePerformance(self) -> dict:
        """
        This function retrieves the cumulative performance of the category.

        Returns:
            dict cumulative performance of the category

        Examples:
            >>> Funds("myria", "fr").categoryCumulativePerformance()

        """

        return self.CumulativePerformance("category")

    def contact(self) -> dict:
        """
        This function retrieves information about the asset manager.

        Returns:
            dict contact

        Examples:
            >>> Funds("myria", "fr").contact()

        """
        no_site_error(self.code, self.name, self.country, self.site)
        result = {}
        # headers random agent
        headers = {"user-agent": random_user_agent()}
        # page 1 - performance
        # page 4 - info about found
        url = f"{self.site}funds/snapshot/snapshot.aspx"
        #params of the request
        params = {
                    "id": self.code,
                    "tab": "4"
                  }
        
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        not_200_response(url, response)
        soup = BeautifulSoup(response.text, "html.parser")
        # label
        label_list = soup.find(id="managementManagementDiv").find_all(
            "td", {"class": "col1 label"}
        )
        # value
        value_list = soup.find(id="managementManagementDiv").find_all(
            "td", {"class": "col2 value number"}
        )
        for i in range(0, len(value_list)):
            label = label_list[i].text

            result[label] = value_list[i].text

        return result

    def costIllustration(self) -> dict:
        """
        This function retrieves the cost of the funds.

        Returns:
            dict cost of funds

        Examples:
            >>> Funds("FOUSA00E5P", "us").costIllustration()

        """
        return self.GetData("price/costIllustration")

    def couponRange(self)  :
        """
        This function retrieves the coupon of the funds, index and category.

        Returns:
            dict coupon

        Examples:
            >>> Funds("rmagx", "us").couponRange()

        """
        return self.GetData("process/couponRange")

    def creditQuality(self) -> dict:
        """
        This function retrieves the credit notation of the funds, index and category.

        Returns:
            dict credit notation

        Examples:
            >>> Funds("rmagx", "us").creditQuality()

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
            >>> Funds("myria", "fr").dataPoint(['largestSector', 'Name', 'ongoingCharge'])
            >>> Funds("myria", "fr").dataPoint('SharpeM36')

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
            >>> Funds("rmagx", "us").distribution("annual")

        """

        period_choice = ["annual", "latest"]
        if period not in period_choice:
            raise ValueError(
                f"""period parameter can only take one of
                             the values: {", ".join(period_choice)}"""
            )

        return self.GetData(f"distribution/{period}")

    def CumulativePerformance(self, 
                              cat:str) -> dict:
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

        """
        if not isinstance(cat, str):
            raise TypeError("cat parameter should be a string")
        
        no_site_error(self.code, self.name, self.country, self.site)

        cat_row = {"funds": 2, "category": 3, "index": 4}

        if cat not in cat_row:
            raise ValueError(
                f"""cat parameter must take
                             one of the following value : { ', '.join(cat_row.keys())}"""
            )
        result = {}

        # headers random agent
        headers = {"user-agent": random_user_agent()}
        # page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx"

        #params of the request
        params = {
                    "id": self.code,
                    "tab": "1"
                  }
        
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        not_200_response(url, response)
        soup = BeautifulSoup(response.text, "html.parser")
        cumulative_performance_date = (
            soup.find(id="returnsTrailingDiv")
            .find("td", {"class": "titleBarNote"})
            .text
        )
        result["cumulative_performance_date"] = cumulative_performance_date
        # days
        regex = re.compile(".*label")
        label_list = soup.find(id="returnsTrailingDiv").find_all("td", {"class": regex})

        # cumulative performance cat
        regex = re.compile(f".*col{str(cat_row[cat])} value number")
        value_list = soup.find(id="returnsTrailingDiv").find_all("td", {"class": regex})
        # loop on label
        for i in range(0, len(label_list)):
            # label
            label = label_list[i].text
            # perf funds
            result[f"{cat}_cumulative_performance_{label}"] = re.sub(
                "[^0-9,-\.]", "", value_list[i].text
            )

        return result

    def equityStyle(self) -> dict:
        """
        This function retrieves the equity style of the funds and category.

        Returns:
            dict equity style

        Examples:
            >>> Funds("myria", "fr").equityStyle()

        """
        return self.GetData("process/stockStyle/v2")

    def equityStyleBoxHistory(self) -> dict:
        """
        This function retrieves the equity style history of the funds

        Returns:
            dict equity style history

        Examples:
            >>> Funds("myria", "fr").equityStyleBoxHistory()

        """
        return self.GetData("process/equityStyleBoxHistory")

    def esgData(self) -> dict:
        """
        This function retrieves ESG data of the funds and category

        Returns:
            dict ESG data

        Examples:
            >>> Funds("myria", "fr").esgData()

        """

        return self.GetData("esg/v1")
    
    def esgRisk(self) -> dict:
        """
        This function retrieves ESG drisk of the funds and category

        Returns:
            dict ESG risk

        Examples:
            >>> Funds("myria", "fr").esgRisk()

        """

        return self.GetData("esgRisk")

    def factorProfile(self) -> dict:
        """
        This function retrieves the factor profile of the funds, index and category

        Returns:
            dict factor profile

        Examples:
            >>> Funds("myria", "fr").factorProfile()

        """
        return self.GetData("factorProfile")

    def feeLevel(self)  :
        """
        This function retrieves the fees of the fund compare to its category.

        Returns:
            dict fees

        Examples:
            >>> Funds("rmagx", "us").feeLevel()

        """
        return self.GetData("price/feeLevel")

    def feeMifid(self, 
                 currency:str="EUR") -> dict:
        """
        This function retrieves the fees of the fund.

        Returns:
            dict fees

        Examples:
            >>> Funds("myria", "fr").feeMifid()

        """
        return self.ltData("Mifid", currency=currency)

    def fees(self) :
        """
        This function retrieves the fees of the fund (by scraping pages);

        Returns:
            dict fees

        Examples:
            >>> Funds("myria", "fr").fees()

        """
        no_site_error(self.code, self.name, self.country, self.site)
        result = {}
        # headers random agent
        headers = {"user-agent": random_user_agent()}
        url = f"{self.site}funds/snapshot/snapshot.aspx"
                #params of the request
        params = {
                    "id": self.code,
                    "tab": "5"
                  }
        
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        not_200_response(url, response)
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find(id="managementFeesDiv") == None:
            return {}
        # label
        label_list = soup.find(id="managementFeesDiv").find_all(
            "td", {"class": "label"}
        )
        # value
        value_list = soup.find(id="managementFeesDiv").find_all(
            "td", {"class": "value number"}
        ) + soup.find(id="managementFeesDiv").find_all(
            "td", {"class": "value number jdpa"}
        )
        for i in range(0, len(value_list)):
            label = label_list[i].text
            result[label] = re.sub("(\\n +)|(\\n)", "", value_list[i].text)

        return result

    def financialMetrics(self) -> dict:
        """
        This function retrieves the final metrics of the funds and category.

        Returns:
            dict financial metrics

        Examples:
            >>> Funds("rmagx", "us").financialMetrics()

        """
        return self.GetData("process/financialMetrics")

    def fixedIncomeStyle(self) -> dict:
        """
        This function retrieves the fixed income style of the funds and category.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("rmagx", "us").fixedIncomeStyle()

        """

        return self.GetData("process/fixedIncomeStyle")

    def fixedincomeStyleBoxHistory(self) -> dict:
        """
        This function retrieves the fixed income style history of the funds.

        Returns:
            dict fixed income style

        Examples:
            >>> Funds("rmagx", "us").fixedincomeStyleBoxHistory()

        """
        return self.GetData("process/fixedincomeStyleBoxHistory")

    def fundsAnnualPerformance(self) -> dict:
        """
        This function retrieves the annual performance of the funds.

        Returns:
            dict funds annual performance

        Examples:
            >>> Funds("myria", "fr").fundsAnnualPerformance()

        """
        return self.AnnualPerformance("funds")

    def fundsAnnualRank(self) -> dict:
        """
        This function retrieves the annual rank of the funds in percentile.

        Returns:
            dict funds annual rank

        Examples:
            >>> Funds("myria", "fr").fundsAnnualRank()

        """
        return self.AnnualPerformance("rank")

    def fundsCumulativePerformance(self) -> dict:
        """
        This function retrieves the cumulative performance of the funds.

        Returns:
            dict funds cumulative performance

        Examples:
            >>> Funds("myria", "fr").fundsCumulativePerformance()

        """
        return self.CumulativePerformance("funds")

    def fundsQuarterlyPerformance(self) -> dict:
        """
        This function retrieves the quarterly performance of the funds.

        Returns:
            dict funds quarterly performance

        Examples:
            >>> Funds("myria", "fr").fundsCumulativePerformance()

        """
        no_site_error(self.code, self.name, self.country, self.site)
        result = {}
        # headers random agent
        headers = {"user-agent": random_user_agent()}
        # page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx"
        #params of the request
        params = {
                    "id": self.code,
                    "tab": "1"
                  }
        
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        not_200_response(url, response)
        soup = BeautifulSoup(response.text, "html.parser")
        quarterly_performance_date = (
            soup.find(id="returnsTrailingDiv")
            .find("td", {"class": "titleBarNote"})
            .text
        )
        result["quarterly_performance_date"] = quarterly_performance_date

        # quarter label
        regex = re.compile(".*heading number")
        quarter_list = soup.find(id="returnsQuarterlyDiv").find_all(
            "td", {"class": regex}
        )
        # year label
        regex = re.compile(".*label")
        year_list = soup.find(id="returnsQuarterlyDiv").find_all("td", {"class": regex})
        # 1st Quarter
        regex = re.compile(".*col2 value number")
        quarter_1_list = soup.find(id="returnsQuarterlyDiv").find_all(
            "td", {"class": regex}
        )
        # 2nd Quarter
        regex = re.compile(".*col3 value number")
        quarter_2_list = soup.find(id="returnsQuarterlyDiv").find_all(
            "td", {"class": regex}
        )
        # 3rd Quarter
        regex = re.compile(".*col4 value number")
        quarter_3_list = soup.find(id="returnsQuarterlyDiv").find_all(
            "td", {"class": regex}
        )
        # 4th Quarter
        regex = re.compile(".*col5 value number")
        quarter_4_list = soup.find(id="returnsQuarterlyDiv").find_all(
            "td", {"class": regex}
        )
        # loop on year
        for i in range(0, len(year_list)):
            label = "performance_%s_" % (year_list[i].text)
            result[label + "quarter_1"] = quarter_1_list[i].text
            result[label + "quarter_2"] = quarter_2_list[i].text
            result[label + "quarter_3"] = quarter_3_list[i].text
            result[label + "quarter_4"] = quarter_4_list[i].text
        return result

    def graphData(self) -> dict:
        """
        This function retrieves historical data of the funds.

        Returns:
            dict historical data

        Examples:
            >>> Funds("myria", "fr").graphData()

        """

        return self.GetData("parent/graphData")

    def historicalData(self) -> dict:
        """
        This function retrieves the historical price of the funds, index and category

        Returns:
            dict with historical data

        Examples:
            >>> Funds("myria", "fr").historicalData()

        """
        return self.GetData("performance/v3", url_suffix="")

    def historicalExpenses(self) -> dict:
        """
        This function retrieves historical expenses of the funds.

        Returns:
            dict historical expenses

        Examples:
            >>> Funds("rmagx", "us").historicalExpenses()

        """
        if self.asset_type == "etf":
            return {}
        return self.GetData("price/historicalExpenses")

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
            >>> Funds("myria", "fr").holdings("all")
            >>> Funds("myria", "fr").holdings("bond")
            >>> Funds("myria", "fr").holdings("equity")
            >>> Funds("myria", "fr").holdings("other")

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

    def indexAnnualPerformance(self) -> dict:
        """
        This function retrieves the annual performance of the index.

        Returns:
            dict annual performance of the index


        Examples:
            >>> Funds("myria", "fr").indexAnnualPerformance()

        """
        return self.AnnualPerformance("index")

    def indexCumulativePerformance(self) -> dict:
        """
        This function retrieves the cumulative performance of the index.

        Returns:
            dict cumulative performance of the index


        Examples:
            >>> Funds("myria", "fr").indexCumulativePerformance()

        """

        return self.CumulativePerformance("index")

    def investmentStrategy(self) -> dict:
        """
        This function retrieves the investment strategy.

        Returns:
            dict investment strategy

        Examples:
            >>> Funds("LU0823421689").investmentStrategy()

        """
        return self.GetData("morningstarTake/investmentStrategy")

    def investmentLookup(self, 
                         currency:str="EUR") -> dict:
        """
        This function gives details about fund investment.

        Returns:
            dict fund investment

        Examples:
            >>> Funds("myria", "fr").investmentLookup()

        """
        return self.ltData("investmentTypeLookup", currency=currency)

    def keyStats(self) -> list[dict]:
        """
        This function retrieves the key status information of the fund,
        index, category or the annual rank of the funds.

        Returns:
            list of dict information on the fund


        Examples:
            >>> Funds("myria", "fr").keyStats()

        """
        # headers random agent
        headers = {"user-agent": random_user_agent()}
        # page 1 - performance
        url = f"{self.site}funds/snapshot/snapshot.aspx"

        #params of the request
        params = {
                    "id": self.code,
                  }
        
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        not_200_response(url, response)
        soup = BeautifulSoup(response.text, "html.parser")

        table_rows = soup.find(id="overviewQuickstatsDiv").find_all("tr")
        details = []
        for row in table_rows:
            key, value, date_stamp = None, None, None
            for cell in row.find_all("td"):
                if cell.has_attr("class"):
                    if "line" in cell["class"]:
                        if "heading" in cell["class"]:
                            key = cell.get_text(separator="\n", strip=True)
                            if "\n" in key:
                                key, date_stamp = key.split("\n")
                        if "text" in cell["class"]:
                            value = cell.text
            if key and value and date_stamp:
                details.append({key: value, "date": date_stamp})
            elif key and value:
                details.append({key: value})

        return details
    def marketCapitalization(self) -> dict:
        """
        This function retrieves the marketCapitalization breakdown of the funds,
        category and index.

        Returns:
            dict market capitalization

        Examples:
            >>> Funds("myria", "fr").marketCapitalization()

        """
        return self.GetData("process/marketCap")

    def maturitySchedule(self) -> dict:
        """
        This function retrieves the maturity breakdown of the funds and category.

        Returns:
            dict maturity

        Examples:
            >>> Funds("rmagx", "us").maturitySchedule()

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
            >>> Funds("myria", "fr").maxDrawDown()

        """

        if not isinstance(year, int):
            raise TypeError("year parameter should be an integer")

        return self.GetData(
            "performance/marketVolatilityMeasure", params={"year": year}
        )

    def morningstarAnalyst(self) -> dict:
        """
        This function retrieves the raiting of MorningStar analyst.

        Returns:
            dict rating

        Examples:
            >>> Funds("rmagx", "us").morningstarAnalyst()

        """

        return self.GetData("morningstarAnalyst")

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
            >>> Funds("rmagx", "us").multiLevelFixedIncomeData()

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

            >>> Funds("RMAGX", "us").nav(datetime.datetime.today() 
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

    def objectiveInvestment(self) -> str:
        """
        This function retrieves the objective of investment of the fund (by scraping pages);

        Returns:
            str objective investment

        Examples:
            >>> Funds("myria", "fr").objectiveInvestment()

        """

        no_site_error(self.code, self.name, self.country, self.site)
        # headers random agent
        headers = {"user-agent": random_user_agent()}
        # Page 1 - overview
        # url page overview
        url = f"{self.site}funds/snapshot/snapshot.aspx"
                #params of the request
        params = {
                    "id": self.code,
                  }
        
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        
        # if page not found
        not_200_response(url, response)
        # html page as soup
        soup = BeautifulSoup(response.text, "html.parser")
        # investment objective funds
        return (
            soup.find(id="overviewObjectiveDiv")
            .find("td", {"class": "value text"})
            .text
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
            >>> Funds("myria", "fr").ownershipZone()

        """

        return self.GetData("process/ownershipZone")

    def parentMstarRating(self) -> list[dict]:
        """
        This function retrieves the raiting of parent by MorningStar analyst.

        Returns:
            list of dict rating

        Examples:
            >>> Funds("rmagx", "us").parentMstarRating()

        """

        return self.GetData("parent/parentMstarRating")

    def parentSummary(self) -> dict:
        """
        This function retrieves info about the parent.

        Returns:
            dict parent info

        Examples:
            >>> Funds("rmagx", "us").parentSummary()

        """
        return self.GetData("parent/parentSummary")

    def people(self) -> dict:
        """
        This function retrieves info about people who works in the company.

        Returns:
            dict people info

        Examples:
            >>> Funds("rmagx", "us").people()

        """
        return self.GetData("people")

    def position(self) -> dict:
        """
        This function retrieves the hodings of the funds.

        Returns:
            dict holdings

        Examples:
            >>> Funds("myria", "fr").position()

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
            >>> Funds("rmagx", "us").proxyVotingManagement()

        """
        return self.GetData("people/proxyVoting/management")

    def proxyVotingShareHolder(self) -> dict:
        """
        This function retrieves the vote of shareholders.

        Returns:
            dict vote

        Examples:
            >>> Funds("rmagx", "us").proxyVotingShareHolder()

        """
        return self.GetData("people/proxyVoting/shareHolder")

    def productInvolvement(self) -> dict:
        """
        This function retrieves the involvement of the funds

        Returns:
            dict involvement

        Examples:
            >>> Funds("myria", "fr").proxyVotingShareHolder()

        """

        return self.GetData("esg/productInvolvement")

    def referenceIndex(self, index) -> str:
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

        """
        no_site_error(self.code, self.name, self.country, self.site)

        index_row = {"benchmark": 0, "category": 1}
        if index not in index_row:
            raise ValueError(
                f"""index parameter must take one of the following value
                : { ', '.join(index_row.keys())}"""
            )

            # headers random agent
        headers = {"user-agent": random_user_agent()}
        # Page 1 - overview
        # url page overview
        url = f"{self.site}funds/snapshot/snapshot.aspx"
        #params of the request
        params = {
                    "id": self.code
                }   
        # get HTML page overview
        response = requests.get(url,
                                params=params,
                                headers=headers, 
                                proxies=self.proxies)
        # if page not found
        not_200_response(url, response)

        # html page as soup
        soup = BeautifulSoup(response.text, "html.parser")
        benchmark_soup = soup.find(id="overviewBenchmarkDiv2Cols").find_all(
            "td", {"class": "value text"}
        )
        return benchmark_soup[index_row[index]].text

    def regionalSector(self) -> dict:
        """
        This function retrieves the breakdown of the funds, category and index by region

        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria", "fr").regionalSector()

        """
        return self.GetData("portfolio/regionalSector")

    def regionalSectorIncludeCountries(self) -> dict:
        """
        This function retrieves the breakdown of the funds,
        category and index by region and country

        Returns:
            dict regional breakdown

        Examples:
            >>> Funds("myria", "fr").regionalSectorIncludeCountries()

        """
        return self.GetData("portfolio/regionalSectorIncludeCountries")

    def riskReturnScatterplot(self) -> dict:
        """
        This function retrieves the return and standard
        deviation of the funds and category

        Returns:
            dict risk return

        Examples:
            >>> Funds("rmagx", "us").riskReturnScatterplot()

        """
        return self.GetData("performance/riskReturnScatterplot")

    def riskReturnSummary(self) -> dict:
        """
        This function retrieves the return and risk summary 
        of the funds compare to the category

        Returns:
            dict risk return

        Examples:
            >>> Funds("rmagx", "us").riskReturnSummary()

        """

        return self.GetData("performance/riskReturnSummary")

    def riskVolatility(self) -> dict:
        """
        This function retrieves the alpha, beta, R², 
        volatility and Sharpe ratio of the funds, category and index.

        Returns:
            dict econometrics

        Examples:
            >>> Funds("rmagx", "us").riskVolatility()

        """
        return self.GetData("performance/riskVolatility")

    def salesFees(self) -> dict:
        """
        This function retrieves the sales fees of the funds

        Returns:
            dict fees

        Examples:
            >>> Funds("myria", "fr").salesFees()

        """
        if self.asset_type == "etf":
            return {}
        return self.GetData("price/salesFees")

    def sector(self) -> dict:
        """
        This function retrieves the sector breakdown of the funds, category and index

        Returns:
            dict sector breakdown

        Examples:
            >>> Funds("myria", "fr").sector()

        """
        return self.GetData("portfolio/v2/sector")

    def snapshot(self, 
                 currency:str="EUR"):
        """
        This function returns a snapshot of the fund and asset manager.

        Returns:
            dict snapshot fund and asset manager

        Examples:
            >>> Funds("myria", "fr").snapshot()

        """
        return self.ltData("MFsnapshot", currency=currency)

    def starRatingFundAsc(self) -> dict:
        """
        This function retrieves the MorningStar rating of the funds
        of the company by ascending order

        Returns:
            dict rating

        Examples:
            >>> Funds("myria", "fr").starRatingFundAsc()

        """

        return self.GetData("parent/mstarRating/StarRatingFundAsc")

    def starRatingFundDesc(self) -> dict:
        """
        This function retrieves the MorningStar rating of the funds
        of the company by descending order

        Returns:
            dict rating

        Examples:
            >>> Funds("myria", "fr").starRatingFundDesc()

        """

        return self.GetData("parent/mstarRating/StarRatingFundDesc")

    def sustainability(self, 
                       currency:str="EUR") -> dict:
        """
        This function retrieves the sustainability data of the fund.

        Returns:
            dict sustanability data

        Examples:
            >>> Funds("myria", "fr").sustainability()

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
                       duration:str="daily") -> dict:
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
            raise ValueError(
                f'duration parameter can only take one of the values: {", ".join(duration_choice)}'
            )

        return self.GetData("trailingReturn/v2", {"duration": duration})
