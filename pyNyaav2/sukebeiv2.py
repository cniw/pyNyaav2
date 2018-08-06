#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from .common import INFO_URL_SUKEBEI, Nyaav2Exception, SEARCH_URL_SUKEBEI, CATEGORY_LIST, UPLOAD_V2_URL_SUKEBEI
from os.path import splitext, dirname
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import json

def SearchSukebeiTorrent(username=None, password=None, keyword=None, category='all', page=1):
    """
    Search and parse info from Sukebei.nyaa.si
    ##################################################
    username: Your username
    password: Your password
    keyword: search keyword
    category: torrent category (default: all)
    page: page to look (default: 1)
    """
    if username is None:
        raise Nyaav2Exception('SearchTorrent: \'username\' cannot be empty')
    if password is None:
        raise Nyaav2Exception('SearchTorrent: \'password\' cannot be empty')
    if keyword is None:
        raise Nyaav2Exception('SearchTorrent: \'keyword\' cannot be empty')
    if not isinstance(page, int):
        raise Nyaav2Exception('SearchTorrent: page must be an integer')

    if isinstance(category, str):
        cat = CATEGORY_LIST(category, 'sukebei')
    elif isinstance(category, int):
        cat = str(category)[:1] + '_' + str(category)[1:]
    r = requests.get(SEARCH_URL_SUKEBEI(keyword, cat, page))
    parse = BeautifulSoup(r.text, 'html.parser')
    queryList = parse.select('table tr')
    
    newQuery = parse_querylist(queryList)

    torrents = []

    for query in newQuery:
        tor_id = query['id']
        dl_link = query['download_link']
        
        r2 = requests.get(f'https://nyaa.si/api/info/{tor_id}', auth=HTTPBasicAuth(username, password))
        r2j = json.loads(r2.text)
        if r2.status_code != 200:
            if r2.status_code == 403:
                raise Nyaav2Exception('SearchTorrent: Bad authentication, please fix it.')
            elif r2.status_code == 400:
                print(r2.text)
                raise Nyaav2Exception('SearchTorrent: Something went wrong\n{}'.format(r2j['errors']))
        
        name = r2j['name']
        create_date = r2j['creation_date']
        description = r2j['description']
        information = r2j['information']
        submitter = r2j['submitter']
        url = r2j['url']
        magnet = r2j['magnet']

        filesize = str(r2j['filesize']/1024/1024)[:5]+' MiB'
        torhash = r2j['hash_hex']
        is_trusted = r2j['is_trusted']
        is_remake = r2j['is_remake']

        categoryN = '{} - {}'.format(r2j['main_category'], r2j['sub_category'])
        categoryID = '{}_{}'.format(r2j['main_category_id'], r2j['sub_category_id'])

        seeds = r2j['stats']['seeders']
        leechs = r2j['stats']['leechers']
        downs = r2j['stats']['downloads']

        querryCollect = {
            'id': tor_id,
            'name': name,
            'information': information,
            'description': description,
            'submitter': submitter,
            'creation': create_date,
            'filesize': filesize,
            'hash': torhash,
            'category': categoryN,
            'category_id': categoryID,
            'seeders': seeds,
            'leechers': leechs,
            'completed': downs,
            'download_link': dl_link,
            'magnet_link': magnet,
            'url': url,
            'is_trusted': is_trusted,
            'is_remake': is_remake
        }
        torrents.append(querryCollect)

    return torrents

def parse_querylist(querylist):
    """
    querylist: <table tr> from SearchTorrent

    #Stolen from NyaaPy
    """
    maximum = len(querylist)
    torrentslist = []

    for query in querylist[:maximum]:
        temp = []

        for td in query.find_all('td'):
            if td.find_all('a'):
                for link in td.find_all('a'):
                    if link.get('href')[-9:] != '#comments':
                        temp.append(link.get('href'))
                        if link.text.rstrip():
                            temp.append(link.text)
            if td.text.rstrip():
                temp.append(td.text.strip())

        try:
            tordata = {
                'id': temp[1].replace("/view/", ""),
                'download_link': temp[4],
            }
            torrentslist.append(tordata)
        except IndexError:
            pass
    
    return torrentslist

def set_opts_sukebei(username=None, password=None, torrent=None, category=1_2, name=None, information=None, description=None, anonymous=False, hidden=False, complete=False, remake=False, trusted=False):
    """
    Set options before uploading to Sukebei.nyaa.si
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
        fulldir = dirname(name)
        if fulldir == '':
            name = name[:-8]
        elif fulldir != '':
            name = name.replace(fulldir, '')[1:][:-8]
    information = 'Uploaded using pyNyaav2' if information is None else information
    description = '' if description is None else description

    if not isinstance(anonymous, bool):
        raise Nyaav2Exception("sukebei: set_opts: anonymous must be a bool ('True' or 'False')")
    if not isinstance(hidden, bool):
        raise Nyaav2Exception("sukebei: set_opts: hidden must be a bool ('True' or 'False')")
    if not isinstance(remake, bool):
        raise Nyaav2Exception("sukebei: set_opts: remake must be a bool ('True' or 'False')")
    if not isinstance(trusted, bool):
        raise Nyaav2Exception("sukebei: set_opts: trusted must be a bool ('True' or 'False')")

    if isinstance(category, str):
        category = CATEGORY_LIST(category, 'sukebei')
    
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

def UploadSukebeiTorrent(options=None):
    """
    Upload torrent to Sukebei.nyaa.si using defined options before
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

        r = requests.post(UPLOAD_V2_URL_SUKEBEI, files=torbit, data=payload, auth=(cred['username'], cred['password']))
        if r.status_code != 200:
            if r.status_code == 403:
                raise Nyaav2Exception('UploadTorrent: Bad authentication, please fix it.')
            elif r.status_code == 400:
                print(r.text)
                raise Nyaav2Exception('UploadTorrent: Something wrong with the data info')

        return r.text