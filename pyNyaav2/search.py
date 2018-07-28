from .common import INFO_URL, Nyaav2Exception, SEARCH_URL, CATEGORY_LIST
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import json

def SearchTorrent(username=None, password=None, keyword=None, category='all', page=1):

    if username is None:
        raise Nyaav2Exception('SearchTorrent: \'username\' cannot be empty')
    if password is None:
        raise Nyaav2Exception('SearchTorrent: \'password\' cannot be empty')
    if keyword is None:
        raise Nyaav2Exception('SearchTorrent: \'keyword\' cannot be empty')

    if isinstance(category, str):
        cat = CATEGORY_LIST(category)
    elif isinstance(category, int):
        cat = str(category)[:1] + '_' + str(category)[1:]
    r = requests.get(SEARCH_URL(keyword, cat, page))
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
                print(r.text)
                raise Nyaav2Exception('SearchTorrent: Something went wrong\n{}'.format(r2j['errors'][0]))
        
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