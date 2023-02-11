BASE_APIURL = 'https://nyaa.si/api'
BASE_URL = 'https://nyaa.si'
BASE_SUKEBEIAPI = 'https://sukebei.nyaa.si/api'
BASE_SUKEBEI = 'https://sukebei.nyaa.si'

UPLOAD_V2_URL = f'{BASE_APIURL}/v2/upload'
INFO_URL = f'{BASE_APIURL}/info'
UPLOAD_V2_URL_SUKEBEI = f'{BASE_SUKEBEIAPI}/v2/upload'
INFO_URL_SUKEBEI = f'{BASE_SUKEBEIAPI}/v2/upload'

class Nyaav2Exception(Exception):
    __module__ = Exception.__module__

def CATEGORY_LIST(category, mode):
    mode = mode.lower()
    if mode != 'nyaa' and mode != 'sukebei':
        raise Nyaav2Exception('common: CATEGORY_LIST: mode can only be \'nyaa\' or \'sukebei\'')
    if mode == 'nyaa':
        category_type = {
            'all': '0_0',

            'anime': '1_0',
            'amv': '1_1',
            'anime_eng': '1_2',
            'anime_non-eng': '1_3',
            'anime_raw': '1_4',

            'audio': '2_0',
            'audio_lossless': '2_1',
            'audio_lossy': '2_2',

            'books': '3_0',
            'books_eng': '3_1',
            'books_non-eng': '3_2',
            'books_raw': '3_3',
            
            'live_action': '4_0',
            'la_eng': '4_1',
            'la_idolpv': '4_2',
            'la_non-eng': '4_3',
            'la_raw': '4_4',

            'pictures': '5_0',
            'pics_graphics': '5_1',
            'pics_photos': '5_2',

            'software': '6_0',
            'sw_apps': '6_1',
            'sw_games': '6_2'
        }
    elif mode == 'sukebei':
        category_type = {
            'all': '0_0',

            'art': '1_0',
            'art_anime': '1_1',
            'art_doujinshi': '1_2',
            'art_games': '1_3',
            'art_manga': '1_4',
            'art_pics': '1_5',

            'real_life': '2_0',
            'real_pics': '2_1',
            'real_videos': '2_2'
        }
    return category_type[category]

def SEARCH_URL_NYAA(query, category=CATEGORY_LIST('all', 'nyaa'), page=1):
    query = query.replace(' ', '+')
    SEARCH_URL = f'{BASE_URL}/?f=0&c={category}&q={query}&p={str(page)}'
    return SEARCH_URL

def SEARCH_URL_SUKEBEI(query, category=CATEGORY_LIST('all', 'sukebei'), page=1):
    query = query.replace(' ', '+')
    SEARCH_URL = f'{BASE_SUKEBEI}/?f=0&c={category}&q={query}&p={str(page)}'
    return SEARCH_URL

