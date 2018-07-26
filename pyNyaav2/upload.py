from os.path import splitext, dirname
import requests
from pyNyaav2.common import UPLOAD_V2_URL, Nyaav2Exception
import json

def set_opts(username, password, torrent, category=1_2, name=None, information=None, description=None, anonymous=False, hidden=False, complete=False, remake=False, trusted=False):
    """
    Set options before uploading to Nyaa.si
    ##################################################
    username: Your very secret username
    password: Your very secret password
    torrent: torrent file
    category: Your torrent category (refer here: https://gist.github.com/noaione/2a74eb362588dcc4edc8684e9c270a8c)
    name: Torrent file name (auto-fetch from files if you're lazy)
    information: Torrent information (like web or irc) (default: 'Uploaded using pyNyaav2')
    description: Torrent description (Markdown Supported!)
    anonymous (True/False): Use Anon mode
    hidden (True/False): Hide your torrent
    remake (True/False): Set as remake torrent
    trusted (True/False): Use trusted, if you're account trusted (it will return error if you're not).
    """
    # Parse if it none
    if name is None:
        name = torrent
        fulldir = dirname(torrent)
        name = name.replace(fulldir, '')[1:]
    information = 'Uploaded using pyNyaav2' if information is None else information
    description = '' if description is None else description

    if not isinstance(anonymous, bool):
        raise Nyaav2Exception("set_opts: anonymous must be a bool ('True' or 'False')")
    if not isinstance(hidden, bool):
        raise Nyaav2Exception("set_opts: hidden must be a bool ('True' or 'False')")
    if not isinstance(remake, bool):
        raise Nyaav2Exception("set_opts: remake must be a bool ('True' or 'False')")
    if not isinstance(trusted, bool):
        raise Nyaav2Exception("set_opts: trusted must be a bool ('True' or 'False')")

    if isinstance(category, str):
        category_type = {
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
        category = category_type[category]
    
    elif isinstance(category, int):
        category = str(category)
        category = category[:1] + '_' + category[1:]

    optsBuild = {
        'credentials': {
            'username': username,
            'password': password,
        },
        'torrent': torrent,
        'category': category,

        'name': name,
        'information': information,
        'description': description,
        'anonymous': anonymous,
        'hidden': hidden,
        'complete': complete,
        'remake': remake,
        'trusted': trusted
    }
    return optsBuild

def UploadTorrent(options=None):
    if options is None:
        raise Nyaav2Exception('UploadTorrent: Options are not Specified')

    with open(options['torrent'], 'rb') as tor:
        payload = {
            'torrent_data': json.dumps({
                'name': options['name'],
                'category': options['category'],
                'information': options['information'],
                'description': options['description'],
                'anonymous': options['anonymous'],
                'hidden': options['hidden'],
                'complete': options['complete'],
                'trusted': options['trusted'],
            })
        }

        cred = options['credentials']

        torbit = {'torrent': tor}

        r = requests.post(UPLOAD_V2_URL, files=torbit, data=payload, auth=(cred['username'], cred['password']))
        if r.status_code != 200:
            if r.status_code == 403:
                raise Nyaav2Exception('UploadTorrent: Bad authentication, please fix it.')
            elif r.status_code == 400:
                print(r.text)
                raise Nyaav2Exception('UploadTorrent: Something wrong with the data info')

        return r.text