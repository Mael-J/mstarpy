import datetime
import pytest
import time

from mstarpy import Funds, search_field, Stock

@pytest.fixture
def funds_collection(): 
    test_fund_details =  [
        {
            "isin": "GB00B784NS11",
            "name": "AXA Framlington Biotech Fund GBP Z Acc",
            "id": "F00000P77J",
            "country": "gb",
            "url": "https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F00000P77J"
        },
        {
            "isin": "LU1148874552",
            "name": "New Millennium - Balanced World Conservative L",
            "id": "F00000VE3V",
            "country": "it",
            "url": "https://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id=F00000VE3V"
        },
        {
            "isin": "LU0816332745",
            "name": "LGT (Lux) I Cat Bond Fund B USD",
            "id": "F00000OVML",
            "country": "IT",
            "url": "https://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id=F00000OVML"
        }
    ]
    return test_fund_details 

def test_fund_details(funds_collection):
    for item in funds_collection:
        fund = Funds(item["id"], country=item["country"])
        assert fund.name == item["name"]
        assert fund.isin == item["isin"]

def test_key_stats(funds_collection):
    for item in funds_collection:
        fund = Funds(item["id"], country=item["country"])
        values = fund.keyStats()
        values[4].get("ISIN") == item["isin"]
        time.sleep(1)

def test_carbon_metrics(funds_collection):
    for item in funds_collection:
        fund = Funds(item["id"], country=item["country"])
        data_dict = fund.carbonMetrics()
        assert "categoryName" in data_dict
        assert "fossilFuelInvolvementPct" in data_dict
        assert "portfolioCarbonRiskScore" in data_dict

@pytest.fixture
def funds_nav():
    nav ={
        "id": "F00000TW95",
        "start_date": datetime.date(2022,4,11),
        "end_date": datetime.date(2022,4,25),
        "history": [
            {'nav': 12.46, 'totalReturn': 14.93951, 'date': '2022-04-11'},
            {'nav': 12.47, 'totalReturn': 14.9515, 'date': '2022-04-12'},
            {'nav': 12.53, 'totalReturn': 15.02344, 'date': '2022-04-13'},
            {'nav': 12.59, 'totalReturn': 15.09538, 'date': '2022-04-14'},
            {'totalReturn': 15.09538, 'date': '2022-04-15'},
            {'nav': 12.54, 'totalReturn': 15.03543, 'date': '2022-04-19'},
            {'nav': 12.49, 'totalReturn': 14.97548, 'date': '2022-04-20'},
            {'nav': 12.47, 'totalReturn': 14.9515, 'date': '2022-04-21'},
            {'nav': 12.53, 'totalReturn': 15.02344, 'date': '2022-04-22'},
            {'nav': 12.61, 'totalReturn': 15.11936, 'date': '2022-04-25'},
        ]
    }
    return nav

def test_fund_nav(funds_nav):
    fund = Funds(funds_nav["id"])
    start_date = funds_nav["start_date"] 
    end_date = funds_nav["end_date"]
    history = fund.nav(start_date, end_date)
    assert history == funds_nav["history"]


def test_fund_invetment_look_up():
    funds_details = Funds("myria").investmentLookup()
    keys = [
        "Id", "InceptionDate", "Isin", "InvestmentType",
        "Type", "Name", "Domicile", "Currency", "RiskAndRating",
        "LastPrice", "Benchmark"
        ]
    assert len(set(keys) - set(funds_details.keys())) == 0


def test_fund_multiple_request_method():
    funds = Funds("LU1085283973", country="fr")
    funds.code
    funds.isin
    funds.name
    funds.asset_type
    funds.allocationMap()
    funds.allocationWeighting()
    funds.analystRating()
    funds.analystRatingTopFunds()
    funds.analystRatingTopFundsUpDown()
    funds.benchmark()
    funds.carbonMetrics()
    funds.category()
    funds.categoryAnnualPerformance()
    funds.categoryCumulativePerformance()
    funds.costIllustration()
    funds.couponRange()
    funds.creditQuality()
    funds.dataPoint("TenforeId")
    funds.distribution()
    funds.equityStyle()
    funds.equityStyleBoxHistory()
    funds.esgData()
    funds.factorProfile()
    funds.feeLevel()
    funds.financialMetrics()
    funds.fixedIncomeStyle()
    funds.fixedincomeStyleBoxHistory()
    funds.fundsAnnualPerformance()
    funds.fundsAnnualRank()
    funds.fundsCumulativePerformance()
    funds.graphData()
    funds.historicalData()
    funds.holdings()
    funds.indexAnnualPerformance()
    funds.indexCumulativePerformance()
    funds.investmentStrategy()
    funds.marketCapitalization()
    funds.maturitySchedule()
    funds.maxDrawDown()
    funds.morningstarAnalyst()
    funds.multiLevelFixedIncomeData()
    funds.otherFee()
    funds.ownershipZone()
    funds.parentMstarRating()
    funds.parentSummary()
    funds.people()
    funds.position()
    funds.productInvolvement()
    funds.proxyVotingManagement()
    funds.proxyVotingShareHolder()
    funds.regionalSector()
    funds.regionalSectorIncludeCountries()
    funds.riskReturnScatterplot()
    funds.riskReturnSummary()
    funds.riskVolatility()
    # Only support fundType="FO" and countryId = "USA"
    # funds.salesFees()
    funds.sector()
    funds.starRatingFundAsc()
    funds.starRatingFundDesc()
    funds.taxes()
    funds.trailingReturn()

def test_fund_web_requests():
    funds = Funds("LU1085283973", country="fr")
    funds.AnnualPerformance(cat="funds")
    time.sleep(1)
    funds.contact()
    time.sleep(1)
    funds.CumulativePerformance(cat="funds")
    time.sleep(1)
    funds.fees() 
    time.sleep(1)
    funds.fundsQuarterlyPerformance()
    time.sleep(1)
    funds.objectiveInvestment()
    time.sleep(1)
    funds.referenceIndex('category')


def test_fund_retrieve_data_point():
    funds = Funds("LU1085283973", country="fr")
    fields = [
        'FeeLevel',
        'fundshareClassId'
        ]
    response_list = funds.dataPoint(field=fields)
    diff = set(fields) - set(response_list[0].keys())
    assert len(diff) == 0






