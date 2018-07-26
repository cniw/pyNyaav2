BASE_URL = 'https://nyaa.si/api'

UPLOAD_V2_URL = f'{BASE_URL}/v2/upload'
INFO_URL = f'{BASE_URL}/info'

class Nyaav2Exception(Exception):
    __module__ = Exception.__module__
