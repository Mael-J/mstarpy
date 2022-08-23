<h2 align="center">Mutual funds data extraction from MorningStar with Python</h2>

mstarpy is a Python package to get mutual funds data from MorningStar.

##  Installation

To get this package working you will need to install it via pip (with a Python 3.10 version or higher) on the terminal by typing:

``$ pip install mstarpy``

##  Usage

### Carbon footprint

Understand the carbon footprint of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.carbonMetrics())

```

```{r, engine='python', count_lines}
{'carbonPortfolioCoveragePct': '97.70', 'carbonRiskScore': '3.24', 'carbonRiskScoreCategoryAverage': '4.42', 'carbonRiskScoreCategoryHigh': '20.60', 'carbonRiskScoreCategoryLow': '0.11', 'carbonRiskScoreCategoryAverageDate': '2022-06-30T05:00:00.000', 'carbonRiskScoreCategoryRankPct': '44', 'carbonRiskScoreDate': '2022-06-30T05:00:00.000', 'categoryDate': '2022-06-30T05:00:00.000', 'categoryName': 'Sector Equity Technology', 'fossilFuelInvolvementPctCategoryAverage': '0.40', 'fossilFuelInvolvementPct': '0.00', 'fossilFuelInvolvementPctCategoryHigh': '16.12', 'fossilFuelInvolvementPctCategoryLow': '0.00', 'isLowCarbon': 'true'} 
```

### ESG commitment

Discover the ESG commotment of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.esgData())

```

```{r, engine='python', count_lines}
{'userType': 'Free', 'esgData': {'sociallyResponsibleFund': None, 'ethicalIssueStrategyFocus': None, 'portfolioDate': '2022-06-30T00:00:00.000', 'portfolioDateSustainabilityRating': '2022-06-30T05:00:00.000', 'fundESGScore': None, 'percentAUMCoveredESG': 100.0, 'fundSustainabilityScore': 18.24, 'percentAUMCoveredControversy': 100.0, 'categoryRankDate': '2022-06-30T05:00:00.000', 'sustainabilityFundQuintile': 4, 'sustainabilityPercentCategoryRank': 22.0, 'sustainabilityMandate': 'No', 'secId': 'F00000PXI1', 'performanceId': '0P0000YSYV', 'tradingSymbol': None, 'iSIN': None, 'fundId': 'FS0000A5KD', 'masterPortfolioId': '753260', 'categoryId': 'EUCA000542', 'name': 'BNP Paribas Disrpt Tech Cl C', 'controversyDeduction': None, 'categoryName': 'Sector Equity Technology', 'globalCategoryName': 'Technology Sector Equity', 'fundHistoryAvgSustainabilityScore': 18.55163, 'historicalSustainabilityScoreGlobalCategoryAverage': 20.73745, 'currentSustainabilityScoreGlobalCategoryAverage': 20.53731, 'numberofFundsAnalyzedinCategorySustainability': 1051, 'HistoryAvgSustainabilityPercentCategoryRank': None, 'sustainabilityRatingCorporateContributionPercent': 100.0, 'sustainabilityRatingSovereignContributionPercent': 0.0, 'portfolioSovereignsustainabilityscore': None, 'historicalSovereignSustainabilityScore': None, 'historicalSovereignSustainabilityCategoryAverage': 16.12813, 'sovereignSustainabilityRatingPercentOfEligiblePortfolioCovered': None}, 'esgScoreCalculation': {'basedPercentAUM': 100.0, 'portfolioESGScore': None, 'portfolioESGScoreCategory': None, 'controversyScore': None, 'controversyScoreCategory': None, 'sustainabilityScore': 18.24, 'sustainabilityScoreCategory': 20.53731, 'environmentalScore': 2.76, 'environmentalScoreCategory': None, 'socialScore': 7.86, 'socialScoreCategory': None, 'governanceScore': 6.68, 'governanceScoreCategory': None, 'portfolioDate': '2022-06-30T05:00:00.000', 'portfolioSustainabilityScore': 18.24, 'portfolioEnvironmentalRiskScore': 2.76, 'portfolioSocialRiskScore': 7.86, 'portfolioGovernanceRiskScore': 6.68, 'portfolioUnallocatedEsgRiskScore': 0.94, 'percentAUMCoveredControversy': 100.0, 'esgFundQuintile': None, 'esgPercentCategoryRank': None, 'controversyFundQuintile': None, 'controversyPercentCategoryRank': None, 'ePercentCategoryRank': None, 'sPercentCategoryRank': None, 'gPercentCategoryRank': None, 'categoryRankDate': 
'2022-06-30T05:00:00.000', 'historicalSustainabilityScoreGlobalCategoryAverage': 20.73745, 'currentSustainabilityScoreGlobalCategoryAverage': 20.53731, 'HistoryAvgSustainabilityPercentCategoryRank': 22.0, 'numberofFundsAnalyzedinCategorySustainability': 1051}, 'esgHoldingsAnalyst': '_PO_', 'esgScoreDistribution': '_PO_', 'esgLevelDistribution': '_PO_', 'sustainabilityIntentionality': {'investmentId': 'FS0000A5KD', 'eSGIncorporation': False, 'eSGEngagement': True, 'genderDiversity': False, 'lowCarbonFossilFuelFree': False, 'communityDevelopment': False, 'environmental': False, 'otherImpactThemes': False, 'renewableEnergy': False, 'waterFocused': False, 'generalEnvironmentalSector': False, 'sustainableInvestmentOverall': False, 'eSGFundOverall': False, 'impactFundOverall': False, 'environmentalSectorOverall': False, 'createdOn': '2019-02-28 04:01:00.0', 'lastUpdateDate': '2022-08-23 04:01:00.0', 'usesNormsBasedScreening': None, 'excludesAbortionStemCells': None, 'excludesAdultEntertainment': None, 'excludesAlcohol': None, 'excludesAnimalTesting': None, 'excludesControversialWeapons': None, 'excludesFurSpecialtyLeather': None, 'excludesGambling': None, 'excludesGMOs': None, 'excludesMilitaryContracting': None, 'excludesNuclear': None, 'excludesPalmOil': None, 'excludesPesticides': None, 'excludesSmallArms': None, 'excludesThermalCoal': None, 'excludesTobacco': None, 'excludesOther': None, 'employsExclusionsOverall': None}}
```

### Credit quality

Monitor the credit quality of the funds.

```python
from mstarpy import MS

ms = MS("credit")
print(ms.creditQuality())

```

```{r, engine='python', count_lines}
{'fundName': 'AB Financial Credit I2 GBP H', 'categoryName': 'Other Bond', 'indexName': None, 'fund': {'creditQualityDate': '2022-06-30T05:00:00.000', 'creditQualityAAA': '3.42000', 'creditQualityAA': '1.13000', 'creditQualityA': '5.14000', 'creditQualityBBB': '41.80000', 'creditQualityBB': '32.55000', 'creditQualityB': '6.38000', 'creditQualityBelowB': '0.00000', 'creditQualityNotRated': '9.58000'}, 'category': {'creditQualityDate': '2022-06-30T05:00:00.000', 'creditQualityAAA': '14.53919', 'creditQualityAA': '4.60652', 'creditQualityA': '11.72232', 'creditQualityBBB': '23.47180', 'creditQualityBB': '15.10036', 'creditQualityB': '14.18666', 'creditQualityBelowB': '1.99186', 'creditQualityNotRated': '14.37841'}, 'index': {'creditQualityDate': None, 'creditQualityAAA': None, 'creditQualityAA': None, 'creditQualityA': None, 'creditQualityBBB': None, 'creditQualityBB': None, 'creditQualityB': None, 'creditQualityBelowB': None, 'creditQualityNotRated': None}}
```

### Fixed income style

Get all information about funds invested in fixed income.

```python
from mstarpy import MS

ms = MS("credit")
print(ms.fixedIncomeStyle())

```

```{r, engine='python', count_lines}
{'isCan': False, 'portfolioDate': '2022-06-30T05:00:00.000', 'assetType': 'FIXEDINCOME', 'fixedIncStyleBox': 5, 'fund': {'secId': 'F000010J32', 'secName': 'AB 
Financial Credit I2 GBP H', 'portfolioDate': '2022-06-30T05:00:00.000', 'avgEffectiveDuration': 3.64, 'modifiedDuration': None, 'avgEffectiveMaturity': None, 'avgCreditQualityName': 'BBB-', 'surveyedAverageSurveyedCreditRating': 'BBB-', 'calculatedAverageCreditRating': None, 'avgCreditQualityDate': '2022-06-30T05:00:00.000', 'avgCoupon': 5.74412, 'avgPrice': 95.84698, 'yieldToMaturity': None}, 'categoryAverage': {'secId': 'EUCA000771', 'secName': 'Other Bond', 'portfolioDate': '2022-07-31T05:00:00.000', 'avgEffectiveDuration': 3.58052, 'modifiedDuration': 3.9772, 'avgEffectiveMaturity': 7.15901, 'avgCreditQualityName': None, 'surveyedAverageSurveyedCreditRating': None, 'calculatedAverageCreditRating': None, 'avgCreditQualityDate': '2022-06-30T05:00:00.000', 'avgCoupon': 3.44482, 'avgPrice': 96.53862, 'yieldToMaturity': 4.08176}}
```

### Sector

Sector breakdown of funds investments.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.sector())

```

```{r, engine='python', count_lines}
{'FIXEDINCOME': {'fundPortfolio': {'portfolioDate': '2022-06-30T05:00:00.000', 'government': 0.0, 'municipal': 0.0, 'corporate': 0.0, 'securitized': 0.0, 'cashAndEquivalents': 100.0, 'derivative': 0.0}, 'categoryPortfolio': {'portfolioDate': '2022-07-31T05:00:00.000', 'government': 3.21361, 'municipal': 0.0, 'corporate': 1.51201, 'securitized': 0.00731, 'cashAndEquivalents': 75.71447, 'derivative': 19.5526}, 'indexPortfolio': {'portfolioDate': None, 'government': None, 'municipal': None, 'corporate': None, 'securitized': None, 'cashAndEquivalents': None, 'derivative': None}, 'categoryName': 'Sector Equity Technology', 'indexName': 'Morningstar Gbl Tech TME GR USD', 'fundName': 'BNP Paribas Disrpt Tech Cl C', 'assetType': 'FIXEDINCOME'}, 'EQUITY': {'fundPortfolio': {'portfolioDate': '2022-06-30T05:00:00.000', 'basicMaterials': 0.0, 'consumerCyclical': 9.58233, 'financialServices': 7.34383, 'realEstate': 4.07224, 'communicationServices': 5.0627, 'energy': 0.0, 'industrials': 3.37488, 'technology': 66.49262, 'consumerDefensive': 0.0, 'healthcare': 4.0714, 'utilities': 0.0}, 'categoryPortfolio': {'portfolioDate': '2022-07-31T05:00:00.000', 'basicMaterials': 0.44454, 'consumerCyclical': 7.59378, 'financialServices': 3.78231, 'realEstate': 0.74965, 'communicationServices': 11.50859, 'energy': 0.1766, 'industrials': 5.14909, 'technology': 67.39924, 'consumerDefensive': 0.14448, 'healthcare': 3.01767, 'utilities': 0.03404}, 'indexPortfolio': {'portfolioDate': '2022-07-31T05:00:00.000', 'basicMaterials': 0.0, 'consumerCyclical': 0.0, 'financialServices': 0.01996, 'realEstate': 0.0, 'communicationServices': 0.0, 'energy': 0.0, 'industrials': 0.0, 'technology': 99.98003, 'consumerDefensive': 0.0, 'healthcare': 0.0, 'utilities': 0.0}, 'categoryName': 'Sector Equity Technology', 'indexName': 'Morningstar Gbl Tech TME GR USD', 'fundName': 'BNP Paribas Disrpt Tech Cl C', 'assetType': 'EQUITY'}, 'assetType': 'EQUITY'}
```

### Financial metrics

Compare funds by their financial metrics.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.financialMetrics())

```

```{r, engine='python', count_lines}
{'userType': 'Free', 'fund': {'masterPortfolioId': '753260', 'portfolioDate': '2022-06-30T05:00:00.000', 'wideMoatPercentage': '_PO_', 'narrowMoatPercentage': 
'_PO_', 'noMoatPercentage': '_PO_', 'financialHealthGradeType': '_PO_', 'profitabilityGradeType': '_PO_', 'growthGradeType': '_PO_', 'roic': '_PO_', 'cashReturn': '_PO_', 'freeCashFlowYield': '_PO_', 'debtToCapital': '_PO_', 'securityName': 'BNP Paribas Disrpt Tech Cl C'}, 'category': {'masterPortfolioId': '204272', 
'portfolioDate': '2022-07-31T05:00:00.000', 'wideMoatPercentage': '_PO_', 'narrowMoatPercentage': '_PO_', 'noMoatPercentage': '_PO_', 'financialHealthGradeType': '_PO_', 'profitabilityGradeType': '_PO_', 'growthGradeType': '_PO_', 'roic': '_PO_', 'cashReturn': '_PO_', 'freeCashFlowYield': '_PO_', 'debtToCapital': '_PO_', 'securityName': 'Sector Equity Technology'}, 'index': {'masterPortfolioId': '2595009', 'portfolioDate': '2022-07-31T05:00:00.000', 'wideMoatPercentage': '_PO_', 'narrowMoatPercentage': '_PO_', 'noMoatPercentage': '_PO_', 'financialHealthGradeType': '_PO_', 'profitabilityGradeType': '_PO_', 'growthGradeType': '_PO_', 'roic': '_PO_', 'cashReturn': '_PO_', 'freeCashFlowYield': '_PO_', 'debtToCapital': '_PO_', 'securityName': 'Morningstar Gbl Tech TME GR USD'}}
```

### Market capitalization

Market capitalization breakdown of funds investments.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.marketCapitalization())

```

```{r, engine='python', count_lines}
{'portfolioDate': '2022-06-30T05:00:00.000', 'assetType': 'EQUITY', 'currencyId': 'EUR', 'fund': {'portfolioDate': '2022-06-30T05:00:00.000', 'name': 'BNP Paribas Disrpt Tech Cl C', 'avgMarketCap': 78931.51451, 'giant': 38.47836, 'large': 28.35261, 'medium': 22.68117, 'small': 9.28113, 'micro': 0.0}, 'category': {'portfolioDate': '2022-07-31T05:00:00.000', 'name': 'Sector Equity Technology', 'avgMarketCap': 129289.22524, 'giant': 53.67279, 'large': 12.12215, 'medium': 20.91581, 'small': 7.07545, 'micro': 0.66737}, 'index': {'portfolioDate': '2022-07-31T05:00:00.000', 'name': 'Morningstar Gbl Tech TME GR USD', 'avgMarketCap': 284903.03483, 'giant': 63.17788, 'large': 26.90885, 'medium': 9.80996, 'small': 0.1033, 'micro': 0.0}}
```

### Stock style

Get all information about funds invested in stocks.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.stockStyle())

```

```{r, engine='python', count_lines}
{'portfolioDate': '2022-06-30T05:00:00.000', 'assetType': 'EQUITY', 'fund': {'prospectiveEarningsYield': 22.33371, 'prospectiveBookValueYield': 3.35888, 'prospectiveRevenueYield': 3.5807, 'prospectiveCashFlowYield': 14.15026, 'prospectiveDividendYield': 0.59518, 'forecasted5YearEarningsGrowth': 15.10913, 'forecastedEarningsGrowth': 23.57385, 'forecastedBookValueGrowth': 11.92521, 'forecastedRevenueGrowth': 11.12691, 'forecastedCashFlowGrowth': 21.08331, 'portfolioDate': '2022-06-30T05:00:00.000', 'name': 'BNP Paribas Disrpt Tech Cl C', 'secId': 'F00000PXI1', 'currencyId': 'EUR'}, 'categoryAverage': {'prospectiveEarningsYield': 20.36308, 'prospectiveBookValueYield': 4.25587, 'prospectiveRevenueYield': 3.03068, 'prospectiveCashFlowYield': 12.23865, 'prospectiveDividendYield': 1.03853, 'forecasted5YearEarningsGrowth': 13.58992, 'forecastedEarningsGrowth': 27.43487, 'forecastedBookValueGrowth': 12.13658, 'forecastedRevenueGrowth': 11.7264, 'forecastedCashFlowGrowth': 20.65426, 'portfolioDate': '2022-07-31T05:00:00.000', 'name': 'Sector Equity Technology', 'secId': 'EUCA000542', 'currencyId': ''}, 'indexAverage': {'prospectiveEarningsYield': 19.96891, 'prospectiveBookValueYield': 4.4252, 'prospectiveRevenueYield': 3.21928, 'prospectiveCashFlowYield': 11.98533, 'prospectiveDividendYield': 1.27762, 'forecasted5YearEarningsGrowth': 11.53482, 'forecastedEarningsGrowth': 24.48762, 'forecastedBookValueGrowth': 12.51472, 'forecastedRevenueGrowth': 11.00318, 'forecastedCashFlowGrowth': 20.83471, 'portfolioDate': '2022-07-31T05:00:00.000', 'name': 'Morningstar Gbl Tech TME GR USD', 'secId': 'F000016WQ2', 'currencyId': ''}}
```

### Factor profile

See funds throught their factor profile.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.factorProfile())

```

```{r, engine='python', count_lines}
{'name': 'BNP Paribas Disrpt Tech Cl C', 'categoryId': 'EUCA000542', 'categoryName': 'Sector Equity Technology', 'indexId': 'F000016WQ2', 'indexName': 'Morningstar Gbl Tech TME GR USD', 'indexEffectiveDate': '2022-06-30', 'categoryEffectiveDate': '2022-05-31', 'ticker': None, 'id': '0P0000YSYV', 'effectiveDate': '2022-05-31', 'factors': {'style': {'categoryAvg': 9.118533, 'indexAvg': 13.27911, 'percentile': 7.446323, 'historicRange': [{'year': '1', 'min': 5.979849, 'max': 
14.989949}, {'year': '3', 'min': 4.54678, 'max': 14.989949}, {'year': '5', 'min': 3.521247, 'max': 14.989949}]}, 'yield': {'categoryAvg': 79.385994, 'indexAvg': 64.95552, 'percentile': 87.375185, 'historicRange': [{'year': '1', 'min': 79.268357, 'max': 88.344966}, {'year': '3', 'min': 77.984547, 'max': 91.62376}, {'year': '5', 'min': 73.649627, 'max': 93.899166}]}, 'quality': {'categoryAvg': 8.92221, 'indexAvg': 5.441309, 'percentile': 15.569475, 'historicRange': [{'year': '1', 'min': 13.722369, 'max': 21.177328}, {'year': '3', 'min': 12.153747, 'max': 29.024136}, {'year': '5', 'min': 6.169225, 'max': 29.024136}]}, 'momentum': {'categoryAvg': 57.03058, 'indexAvg': 57.131156, 'percentile': 58.656596, 'historicRange': [{'year': '1', 'min': 22.760606, 'max': 78.978493}, {'year': '3', 'min': 11.541477, 'max': 78.978493}, {'year': '5', 'min': 5.150902, 'max': 78.978493}]}, 'volatility': {'categoryAvg': 14.994364, 'indexAvg': 45.490358, 'percentile': 15.46092, 'historicRange': [{'year': '1', 'min': 14.291359, 'max': 39.62354}, {'year': '3', 'min': 14.291359, 'max': 67.397608}, {'year': '5', 'min': 14.291359, 'max': 87.19611}]}, 'liquidity': {'categoryAvg': 25.641999, 'indexAvg': 54.618222, 'percentile': 19.521341, 'historicRange': [{'year': '1', 'min': 16.255203, 'max': 37.783154}, {'year': '3', 'min': 16.255203, 'max': 38.50419}, {'year': '5', 'min': 12.777605, 'max': 72.742365}]}, 'size': {'categoryAvg': 77.30959, 'indexAvg': 94.028959, 'percentile': 53.32816, 'historicRange': [{'year': '1', 'min': 52.109345, 'max': 61.723463}, {'year': '3', 'min': 50.432021, 'max': 64.86263}, {'year': '5', 'min': 50.432021, 'max': 96.006679}]}}}
```

### Ownership zone

Ownership zone of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.ownershipZone())

```

```{r, engine='python', count_lines}
{'portfolioDate': '2022-06-30T05:00:00.000', 'fund': {'portfolioDate': '2022-06-30T05:00:00.000', 'scaledSizeScore': 266.974, 'scaledStyleScore': 269.356, 'sizeVariance': 117.428, 'styleVariance': 86.836, 'rho': 0.323, 'secId': 'F00000PXI1', 'name': 'BNP Paribas Disrpt Tech Cl C', 'objectZone75Percentile': 2.349}, 'benchmark': {'portfolioDate': '2022-07-31T05:00:00.000', 'scaledSizeScore': 352.941, 'scaledStyleScore': 245.922, 'sizeVariance': 83.159, 'styleVariance': 104.01, 'rho': 0.153, 'secId': 'F000016WQ2', 'name': 'Morningstar Gbl Tech TME GR USD', 'objectZone75Percentile': 3.444}, 'category': {'portfolioDate': '2022-07-31T05:00:00.000', 'scaledSizeScore': 315.811, 'scaledStyleScore': 250.8, 'sizeVariance': 115.564, 'styleVariance': 95.037, 'rho': 0.133, 'secId': 'EUCA000542', 'name': 'Sector Equity Technology', 'objectZone75Percentile': 2.372}}
```

### Asset allocation

Asset allocation breakdown.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.assetAllocation())

```

```{r, engine='python', count_lines}
{'assetType': 'EQUITY', 'portfolioDate': '2022-06-30T05:00:00.000', 'portfolioDateCategory': '2022-07-31T05:00:00.000', 'portfolioDateIndex': '2022-07-31T05:00:00.000', 'portfolioDateGlobal': '2022-06-30T05:00:00.000', 'portfolioDateCategoryGlobal': '2022-07-31T05:00:00.000', 'portfolioDateIndexGlobal': '2022-07-31T05:00:00.000', 'fundName': 'BNP Paribas Disrpt Tech Cl C', 'categoryName': 'Sector Equity Technology', 'indexName': 'Morningstar Gbl Tech TME GR USD', 'allocationMap': {'AssetAllocCash': {'netAllocation': '1.20673', 'shortAllocation': None, 'longAllocation': '1.20673', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '5.08025', 'targetAllocation': None}, 'AssetAllocNotClassified': {'netAllocation': '0.0', 'shortAllocation': None, 'longAllocation': '0.0', 'longAllocationIndex': '0.0', 'longAllocationCategory': '0.058410000000000004', 'targetAllocation': None}, 'AssetAllocNonUSEquity': {'netAllocation': '12.71682', 'shortAllocation': None, 'longAllocation': '12.71682', 'longAllocationIndex': '21.99999', 'longAllocationCategory': '31.07350', 'targetAllocation': None}, 'AssetAllocOther': {'netAllocation': '0.00000', 'shortAllocation': None, 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '2.11402', 'targetAllocation': None}, 'AssetAllocUSEquity': {'netAllocation': '86.07645', 'shortAllocation': None, 'longAllocation': '86.07645', 'longAllocationIndex': '78.00000', 'longAllocationCategory': '63.95990', 'targetAllocation': None}, 'AssetAllocBond': {'netAllocation': '0.00000', 'shortAllocation': None, 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '0.19399', 'targetAllocation': None}}, 'countryCode': 'LUX', 'securityType': 
None, 'dualViewData': {'performanceId': '0P0000YSYV', 'marketValueStockLong': '98.79327', 'marketValueStockShort': None, 'marketValueStockNet': '98.79327', 'marketValueBondLong': None, 'marketValueBondShort': None, 'marketValueBondNet': None, 'marketValueCashLong': '1.20673', 'marketValueCashShort': '0', 'marketValueCashNet': '1.20673', 'marketValueDerivativeLong': None, 'marketValueDerivativeShort': None, 'marketValueDerivativeNet': None, 'marketValueFundLong': None, 'marketValueFundShort': None, 'marketValueFundNet': None, 'marketValueOtherLong': None, 'marketValueOtherShort': None, 'marketValueOtherNet': None, 'economicExposureCurrencyLong': '1.20673', 'economicExposureCurrencyShort': '0', 'economicExposureCurrencyNet': '1.20673', 'economicExposureFixedIncomeLong': None, 'economicExposureFixedIncomeShort': None, 'economicExposureFixedIncomeNet': None, 'economicExposureEquityLong': '98.79327', 'economicExposureEquityShort': None, 'economicExposureEquityNet': '98.79327', 'economicExposureOtherLong': None, 'economicExposureOtherShort': None, 'economicExposureOtherNet': None, 'marketValueAsOf': '2022-06-30T05:00:00.000', 'economicExposureAsOf': '2022-06-30T05:00:00.000', 'dualViewAsOf': '2022-06-30T05:00:00.000', 'marketValueTotal': {'longVal': 100.0, 'shortVal': 0.0, 'netVal': 100.0}, 'economicExposureTotal': {'longVal': 100.0, 'shortVal': 0.0, 'netVal': 100.0}}, 'targetDate': None, 'hasRegionalAssetAlloc': 
False, 'globalAllocationMap': {'assetAllocPreferred': {'netAllocation': '0.00000', 'shortAllocation': None, 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '0.04954', 'targetAllocation': None}, 'assetAllocOther': {'netAllocation': '0.00000', 'shortAllocation': None, 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '2.11402', 'targetAllocation': None}, 'assetAllocEquity': {'netAllocation': '98.79327', 'shortAllocation': None, 'longAllocation': '98.79327', 'longAllocationIndex': '99.99999', 'longAllocationCategory': '95.03340', 'targetAllocation': None}, 'assetAllocCash': {'netAllocation': '1.20673', 'shortAllocation': None, 'longAllocation': '1.20673', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '5.08025', 'targetAllocation': None}, 'assetAllocConvertible': {'netAllocation': '0.00000', 'shortAllocation': None, 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '0.00887', 'targetAllocation': None}, 'assetAllocFixedIncome': {'netAllocation': '0.00000', 'shortAllocation': None, 'longAllocation': '0.00000', 'longAllocationIndex': '0.00000', 'longAllocationCategory': '0.19399', 'targetAllocation': None}}}
```

### Holdings

Full transparency with holdings of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.holdings())

```

```{r, engine='python', count_lines}
                                     securityName       secId performanceId holdingTypeId  ...  qualRating  quantRating  bestRatingType  securityType
0                                  Microsoft Corp  0P000003MH    0P000003MH             E  ...           4            3            Qual            ST
1                                       Apple Inc  0P000000GY    0P000000GY             E  ...           2            3            Qual            ST
2                            Alphabet Inc Class A  0P000002HD    0P000002HD             E  ...           4            4            Qual            ST
3                                Visa Inc Class A  0P0000CPCP    0P0000CPCP             E  ...           3            3            Qual            ST
4                      Advanced Micro Devices Inc  0P0000006A    0P0000006A             E  ...           4            5            Qual            ST
5                                 First Solar Inc  0P00006TF8    0P00006TF8             E  ...           2            3            Qual            ST
6                                    Entegris Inc  0P000001Z2    0P000001Z2             E  ...           3            3            Quan            ST
7   Taiwan Semiconductor Manufacturing Co Ltd ADR  0P000005AR    0P000005AR             E  ...           5            4            Qual            ST
```

### objective Investment

objective of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.objectiveInvestment())

```

```{r, engine='python', count_lines}
Increase the value of its assets over the medium term by investing primarily in innovative technology companies.
```
### Benchmark

benchmark of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.benchmark())

```

```{r, engine='python', count_lines}
MSCI World NR EUR
```

### Category

category of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.category())

```

```{r, engine='python', count_lines}
MSCI World/Information Tech NR USD
```

### Funds annual performance

Annual performance of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.fundsAnnualPerformance())

```

```{r, engine='python', count_lines}
{'funds_annual_performance_2015': '13.62', 'funds_annual_performance_2016': '28.15', 'funds_annual_performance_2017': '23.64', 'funds_annual_performance_2018': '9.13', 'funds_annual_performance_2019': '32.00', 'funds_annual_performance_2020': '42.78', 'funds_annual_performance_2021': '25.35', 'funds_annual_performance_current': '-14.50'}
```
### Index annual performance

Annual performance of the index.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.indexAnnualPerformance())

```

```{r, engine='python', count_lines}
{'index_annual_performance_2015': '2.79', 'index_annual_performance_2016': '-4.80', 'index_annual_performance_2017': '-2.63', 'index_annual_performance_2018': 
'5.67', 'index_annual_performance_2019': '-9.86', 'index_annual_performance_2020': '3.44', 'index_annual_performance_2021': '-5.70', 'index_annual_performance_current': '-2.97'}
```
### Index annual performance

Annual performance of the category.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.categoryAnnualPerformance())

```

```{r, engine='python', count_lines}
{'category_annual_performance_2015': '5.05', 'category_annual_performance_2016': '0.23', 'category_annual_performance_2017': '-1.66', 'category_annual_performance_2018': '12.49', 'category_annual_performance_2019': '1.89', 'category_annual_performance_2020': '-0.93', 'category_annual_performance_2021': '10.38', 'category_annual_performance_current': '5.33'}
```

### Funds annual rank

Annual rank of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.fundsAnnualRank())

```

```{r, engine='python', count_lines}       
{'rank_annual_performance_2015': '20', 'rank_annual_performance_2016': '46', 'rank_annual_performance_2017': '60', 'rank_annual_performance_2018': '6', 'rank_annual_performance_2019': '45', 'rank_annual_performance_2020': '40', 'rank_annual_performance_2021': '24', 'rank_annual_performance_current': '23'}
```

### Funds cumulative performance

cumulative performance of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.fundsCumulativePerformance())

```

```{r, engine='python', count_lines}       
{'cumulative_performance_date': '22/08/2022', 'funds_cumulative_performance_1 Day': '-2.56', 'funds_cumulative_performance_1 Week': '-2.51', 'funds_cumulative_performance_1 Month': '7.20', 'funds_cumulative_performance_3 Months': '14.21', 'funds_cumulative_performance_6 Months': '4.85', 'funds_cumulative_performance_YTD': '-11.65', 'funds_cumulative_performance_1 Year': '-2.66', 'funds_cumulative_performance_3 Years Annualised': '17.85', 'funds_cumulative_performance_5 Years Annualised': '19.16', 'funds_cumulative_performance_10 Years Annualised*': '18.79'}
```

### Index cumulative performance

cumulative performance of the index.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.indexCumulativePerformance())

```

```{r, engine='python', count_lines}       
{'cumulative_performance_date': '22/08/2022', 'index_cumulative_performance_1 Day': '0.07', 'index_cumulative_performance_1 Week': '0.57', 'index_cumulative_performance_1 Month': '0.80', 'index_cumulative_performance_3 Months': '-0.43', 'index_cumulative_performance_6 Months': '-2.41', 'index_cumulative_performance_YTD': '-2.68', 'index_cumulative_performance_1 Year': '-2.93', 'index_cumulative_performance_3 Years Annualised': '-3.22', 'index_cumulative_performance_5 Years Annualised': '-1.70', 'index_cumulative_performance_10 Years Annualised*': '-2.10'}
```


### Category cumulative performance

cumulative performance of the category.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.categoryCumulativePerformance())

```

```{r, engine='python', count_lines}       
{'cumulative_performance_date': '22/08/2022', 'category_cumulative_performance_1 Day': '-0.66', 'category_cumulative_performance_1 Week': '-0.31', 'category_cumulative_performance_1 Month': '4.12', 'category_cumulative_performance_3 Months': '8.19', 'category_cumulative_performance_6 Months': '9.46', 'category_cumulative_performance_YTD': '6.88', 'category_cumulative_performance_1 Year': '9.95', 'category_cumulative_performance_3 Years Annualised': '3.63', 'category_cumulative_performance_5 Years Annualised': '4.72', 'category_cumulative_performance_10 Years Annualised*': '2.19'}
```

### Funds quarterly performance

quarterly performance of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.fundsQuarterlyPerformance())

```

```{r, engine='python', count_lines}         
{'quarterly_performance_date': '22/08/2022', 'performance_2022_quarter_1': '-9.47', 'performance_2022_quarter_2': '-16.62', 'performance_2022_quarter_3': '-', 
'performance_2022_quarter_4': '-', 'performance_2021_quarter_1': '-1.54', 'performance_2021_quarter_2': '9.73', 'performance_2021_quarter_3': '5.78', 'performance_2021_quarter_4': '9.69', 'performance_2020_quarter_1': '-6.43', 'performance_2020_quarter_2': '28.63', 'performance_2020_quarter_3': '8.18', 'performance_2020_quarter_4': '9.65', 'performance_2019_quarter_1': '16.87', 'performance_2019_quarter_2': '7.77', 'performance_2019_quarter_3': '1.73', 'performance_2019_quarter_4': '3.01', 'performance_2018_quarter_1': '4.02', 'performance_2018_quarter_2': '9.84', 'performance_2018_quarter_3': '9.95', 'performance_2018_quarter_4': '-13.13', 'performance_2017_quarter_1': '8.92', 'performance_2017_quarter_2': '0.53', 'performance_2017_quarter_3': '4.67', 'performance_2017_quarter_4': '7.88'}
```

### Funds contact

information about the funds and asset manager.

```python
from mstarpy import MS

ms = MS("disruptive technology")
print(ms.contact())

```

```{r, engine='python', count_lines}       
{'Name of Company': 'BNP Paribas Asset Management Luxembourg', 'Phone': '+352 2646 3017', 'Website': 'www.bnpparibas-am.com', 'Address': '10 rue Edward Steichen', '\xa0': 'Luxembourg', 'Domicile': 'Luxembourg', 'Legal Structure': 'SICAV', 'UCITS': 'Yes', 'Fund Manager': '1995', 'Manager Start Date': '13/09/2016', 'Career Start Year': '1994', 'Education': 'Pamela\xa0Hegarty', 'Biography': '13/09/2016'}
```

### Funds fees

fees of the funds.

```python
from mstarpy import MS

ms = MS("F00000270E", country="fr")  
print(ms.fees())

```

```{r, engine='python', count_lines}       
{'Frais de souscription max': '3,50%', 'Frais de rachat max.': 'n/a', 'Frais de conversion': '-', 'Frais de gestion annuels maximum': '1,93%', 'Frais courants': '1,94%'}
```

### Data points

Get any information of the funds.

```python
from mstarpy import MS

ms = MS("disruptive technology") 
print(ms.dataPoint(['largestSector', 'SharpeM36', 'ongoingCharge']))

```

```{r, engine='python', count_lines}       
[{'largestSector': 'SB_Technology', 'SharpeM36': 0.95, 'ongoingCharge': 1.98}]
```

## Contribute

You can download the open-source project on GitHub [mstarpy](https://github.com/Mael-J/mstarpy) and add your touch to make the package better.

## Disclaimer

mstarpy works as an API of MorningStar. It allows to get data from the site in an easy way. mstarpy is not affiliated with MorningStar and is completly independant.


