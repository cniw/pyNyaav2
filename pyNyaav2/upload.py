from os.path import splitext, dirname
import requests
from .common import UPLOAD_V2_URL, Nyaav2Exception, CATEGORY_LIST
import json

def set_opts(username=None, password=None, torrent=None, category=1_2, name=None, information=None, description=None, anonymous=False, hidden=False, complete=False, remake=False, trusted=False):
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

    if username is None:
        raise Nyaav2Exception('set_opts: \'username\' cannot be empty')
    if password is None:
        raise Nyaav2Exception('set_opts: \'password\' cannot be empty')
    if torrent is None:
        raise Nyaav2Exception('set_opts: \'torrent\' cannot be empty')

    if name is None:
        name = torrent
        fulldir = dirname(torrent)
        name = name.replace(fulldir, '')[1:][:-8]
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
        category = CATEGORY_LIST(category)
    
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
    """
    Upload torrent to Nyaa.si using defined options before
    ##################################################
    options: dictionary of options from 'set_opts'
    """
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