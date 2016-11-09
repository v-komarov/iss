import re
import requests

ISS_GET_URL = 'http://10.6.3.7/address_text.php?ip={ip}'
ISS_ATTEMPTS = 10


def get_iss_location(ip):
    """ Get device location by IP from ISS DB.
    :param ip: Device IP address.
    :type ip: str
    :return: Device location
    :type: str
    """
    uri = ISS_GET_URL.format(ip=ip)
    counter = 0
    while True:
        try:
            counter += 1
            response = requests.get(uri)
        except requests.ConnectionError as e:
            if counter >= ISS_ATTEMPTS:
                raise e
        else:
            raw_location = response.text.replace('/', '-')
            location_regexp = re.compile(r'[A-Z][\w\- ]+(,[^,]+){2}')
            m_obj = location_regexp.search(raw_location)
            if m_obj:
                location = m_obj.group()
                return '/' + location.strip().replace(', ', '/')
            else:
                return None
