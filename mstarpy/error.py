def not_200_response(url,response):
    """
    This function raise a ConnectionError if the status code a requests is not 200.

    """
    if not response.status_code == 200:
        raise ConnectionError(f"Error {response.status_code} for the api {url}. Message : {response.reason}.")


def no_site_error(code, name, country, site):
    """ 
    This function raise a ValueError if the selected country is "us" or a site is not selected.
    
    """
    
        
    if not site or country == 'us':
        if country:
            raise ValueError(f"The funds of the country {country} cannot be scraped.")
        else:
            raise ValueError(f"The funds {name} ({code}) cannot be scraped.")



    