BASE_APIURL = 'https://nyaa.si/api'
BASE_URL = 'https://nyaa.si'

UPLOAD_V2_URL = f'{BASE_URL}/v2/upload'
INFO_URL = f'{BASE_URL}/info'

def CATEGORY_LIST(category):
    category_type = {
        'all': '0_0',
        'amv': '1_1',
        'anime_eng': '1_2',
        'anime_non-eng': '1_3',
        'anime_raw': '1_4',

        'audio_lossless': '2_1',
        'audio_lossy': '2_2',

        'books_eng': '3_1',
        'books_non-eng': '3_2',
        'books_raw': '3_3',
        
        'la_eng': '4_1',
        'la_idolpv': '4_2',
        'la_non-eng': '4_3',
        'la_raw': '4_4',

        'pics_graphics': '5_1',
        'pics_photos': '5_2',

        'sw_apps': '6_1',
        'sw_games': '6_2'
    }
    return category_type[category]

def SEARCH_URL(query, category=CATEGORY_LIST('all'), page=1):
    query = query.replace(' ', '+')
    SEARCH_URL = f'{BASE_URL}/?f=0&c={category}&q={query}&p={str(page)}'
    return SEARCH_URL

class Nyaav2Exception(Exception):
    __module__ = Exception.__module__
