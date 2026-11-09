
from mstarpy import Funds, Stock

import datetime
from mstarpy.search import MorningstarSession
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import traceback



def send_email(subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587


    sender = os.environ["EMAIL"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ["EMAIL"]


    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject


    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(message)


def test_all_functions():
    """Test all selected mstarpy functions and send an email if any fail."""

    session = MorningstarSession()
    fund = Funds("VTSAX", session=session)
    fund_2 = Funds("IE00B04GQT48", session=session)
    stock = Stock(
        "US8334451098",
        language="en-gb",
        filters={"exchange": "XNYS"},
        session=session,
    )

    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=30)


    stock = Stock("US8334451098",
                    language="en-gb",
                    filters={"exchange" : "XNYS"}
                    
                    )
    # Registry of functions to test
    tests = {
        "fund.allocationMap": lambda: fund.allocationMap(),
        "fund.allocationWeighting": lambda: fund.allocationWeighting(),
        "fund.analystRating": lambda: fund.analystRating(),
        "fund.analystRatingTopFunds" : lambda: fund.analystRatingTopFunds(),
        "fund.analystRatingTopFundsUpDown" : lambda: fund.analystRatingTopFundsUpDown(),
        "fund.carbonMetrics" : lambda: fund.carbonMetrics(),
        "fund.costIllustration": lambda: fund.costIllustration(),
        "fund.costProjection": lambda: fund.costProjection(),
        "fund.couponRange"  : lambda: fund_2.couponRange(),
        "fund.creditQuality": lambda: fund_2.creditQuality(),
        "fund.distribution": lambda: fund.distribution("annual"),
        "fund.downloadDocument": lambda: fund_2.downloadDocument("fr","PRIIP KID","en"),
        "fund.equityStyle": lambda: fund.equityStyle(),
        "fund.equityStyleBoxHistory": lambda: fund.equityStyleBoxHistory(),
        "fund.esgData": lambda: fund.esgData(),
        "fund.esgRisk": lambda: fund.esgRisk(),
        "fund.factorProfile": lambda: fund.factorProfile(),
        "fund.feeLevel": lambda: fund.feeLevel(),
        "fund.feeMifid": lambda: fund_2.feeMifid(),
        "fund.financialMetrics": lambda: fund.financialMetrics(),
        "fund.fixedIncomeStyle": lambda: fund_2.fixedIncomeStyle(),
        "fund.fixedincomeStyleBoxHistory": lambda: fund_2.fixedincomeStyleBoxHistory(),
        "fund.getDocumentInformation": lambda: fund_2.getDocumentInformation("fr"),
        "fund.graphData": lambda: fund.graphData(),
        "fund.historicalData": lambda: fund.historicalData(),
        "fund.historicalExpenses": lambda: fund.historicalExpenses(),
        "fund.historicalRating": lambda: fund.historicalRating(),
        "fund.holdings": lambda: fund.holdings(),
        "fund.investmentFee": lambda: fund_2.investmentFee(),
        "fund.investmentLookup": lambda: fund_2.investmentLookup(),
        "fund.investmentStrategy": lambda: fund.investmentStrategy(),
        "fund.marketCapitalization": lambda: fund.marketCapitalization(),
        "fund.maturitySchedule": lambda: fund_2.maturitySchedule(),
        "fund.maxDrawDown": lambda: fund.maxDrawDown(),
        "fund.medaListComparables": lambda: fund.medaListComparables(),
        "fund.metaData": lambda: fund.metaData(),
        "fund.morningstarAnalyst": lambda: fund.morningstarAnalyst(),
        "fund.morningstarOpinion": lambda: fund.morningstarOpinion(),
        "fund.multiLevelFixedIncomeData": lambda: fund_2.multiLevelFixedIncomeData(),
        "fund.nav": lambda: fund.nav(start_date, end_date),
        "fund.otherFee": lambda: fund.otherFee(),
        "fund.ownershipZone": lambda: fund.ownershipZone(),
        "fund.parentMedal": lambda: fund.parentMedal(),
        "fund.parentMedaListRating": lambda: fund.parentMedaListRating(),
        "fund.parentMstarRating": lambda: fund.parentMstarRating(),
        "fund.parentRatingRecentChange": lambda: fund.parentRatingRecentChange(),
        "fund.parentSummary": lambda: fund.parentSummary(),
        "fund.people": lambda: fund.people(),
        "fund.performanceTable": lambda: fund.performanceTable(),
        "fund.position": lambda: fund.position(),
        "fund.productInvolvement": lambda: fund.productInvolvement(),
        "fund.proxyVotingManagement": lambda: fund.proxyVotingManagement(),
        "fund.proxyVotingShareHolder": lambda: fund.proxyVotingShareHolder(),
        "fund.quote": lambda: fund.quote(),
        "fund.regionalSector": lambda: fund.regionalSector(),
        "fund.regionalSectorIncludeCountries": lambda: fund.regionalSectorIncludeCountries(),
        "fund.riskReturnScatterplot": lambda: fund.riskReturnScatterplot(),
        "fund.riskReturnSummary": lambda: fund.riskReturnSummary(),
        "fund.riskScore": lambda: fund.riskScore(),
        "fund.riskVolatility": lambda: fund.riskVolatility(),
        "fund.salesFees": lambda: fund.salesFees(),
        "fund.sector": lambda: fund.sector(),
        "fund.snapshot": lambda: fund.snapshot(),
        "fund.starRatingFundAsc": lambda: fund.starRatingFundAsc(),
        "fund.starRatingFundDesc": lambda: fund.starRatingFundDesc(),
        "fund.strategyPreview": lambda: fund.strategyPreview(),
        "fund.sustainability": lambda: fund.sustainability(),
        "fund.taxes": lambda: fund.taxes(),
        "fund.trailingReturn": lambda: fund.trailingReturn(),
        "stock.analysisData": lambda: stock.analysisData(),
        "stock.analysisReport": lambda: stock.analysisReport(),
        "stock.balanceSheet": lambda: stock.balanceSheet(),
        "stock.balanceSheetQuarterlyRestatedExport": lambda: stock.balanceSheet(
            period="quarterly", reportType="restated", export=True
        ),
        "stock.boardOfDirectors": lambda: stock.boardOfDirectors(),
        "stock.cashFlow": lambda: stock.cashFlow(),
        "stock.cashFlowAnnualRestatedExport": lambda: stock.cashFlow(
            period="annual", reportType="restated", export=True
        ),
        "stock.companyProfile": lambda: stock.companyProfile(),
        "stock.dividends": lambda: stock.dividends(),
        "stock.esgRisk": lambda: stock.esgRisk(),
        "stock.financialHealth": lambda: stock.financialHealth(),
        "stock.financialStatement": lambda: stock.financialStatement(),
        "stock.financialSummary": lambda: stock.financialSummary(),
        "stock.freeCashFlow": lambda: stock.freeCashFlow(),
        "stock.historical": lambda: stock.historical(start_date, end_date),
        "stock.incomeStatement": lambda: stock.incomeStatement(),
        "stock.incomeStatementQuarterlyOriginalExport": lambda: stock.incomeStatement(
            period="quarterly", reportType="original", export=True
        ),
        "stock.institutionBuyers": lambda: stock.institutionBuyers(),
        "stock.institutionConcentratedOwners": lambda: stock.institutionConcentratedOwners(),
        "stock.institutionOwnership": lambda: stock.institutionOwnership(),
        "stock.institutionSellers": lambda: stock.institutionSellers(),
        "stock.keyExecutives": lambda: stock.keyExecutives(),
        "stock.keyMetricsSummary": lambda: stock.keyMetricsSummary(),
        "stock.mutualFundBuyers": lambda: stock.mutualFundBuyers(),
        "stock.mutualFundConcentratedOwners": lambda: stock.mutualFundConcentratedOwners(),
        "stock.mutualFundOwnership": lambda: stock.mutualFundOwnership(),
        "stock.mutualFundSellers": lambda: stock.mutualFundSellers(),
        "stock.operatingGrowth": lambda: stock.operatingGrowth(),
        "stock.overview": lambda: stock.overview(),
        "stock.profitability": lambda: stock.profitability(),
        "stock.split": lambda: stock.split(),
        "stock.sustainability": lambda: stock.sustainability(),
        "stock.tradingInformation": lambda: stock.tradingInformation(),
        "stock.trailingTotalReturn": lambda: stock.trailingTotalReturn(),
        "stock.transactionHistory": lambda: stock.transactionHistory(),
        "stock.transactionSummary": lambda: stock.transactionSummary(),
        "stock.valuation": lambda: stock.valuation(),

    }

    errors = []

    for name, test in tests.items():
        try:
            test()

        except Exception:
            errors.append(
                f"❌ {name}\n{traceback.format_exc()}"
            )


    if errors:
        subject = "❌ Error in mstarpy test_all_functions"
        body = f"Errors:\n{chr(10).join(errors)}"
        send_email(subject, body)
    else:
        subject = "✅ mstarpy test_all_functions passed"
        body = "All tests passed!"
        send_email(subject, body)
    return {
        "total": len(tests),
        "successful": len(tests) - len(errors),
        "failed": len(errors),
        "errors": errors,
    }



if __name__ == "__main__":

    test_all_functions()






















