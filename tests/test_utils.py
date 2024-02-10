from mstarpy.utils import FILTER_FUND, FILTER_STOCK, EXCHANGE


def test_parameters_in_filter():
    assert 'AdministratorCompanyId' in FILTER_FUND