from mstarpy.security import Security

def test_security():
    security = Security("visa", exchange='NYSE')
    assert "Visa Inc Class A" == security.name
    assert "NYSE" == security.exchange
    assert "0P0000CPCP" == security.code