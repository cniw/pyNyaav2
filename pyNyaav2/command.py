#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import os
import json

from pyNyaav2.common import Nyaav2Exception
from pyNyaav2.nyaav2 import SearchTorrent, UploadTorrent, set_opts
from pyNyaav2.sukebeiv2 import SearchSukebeiTorrent, UploadSukebeiTorrent, set_opts_sukebei

def main():
    parser = argparse.ArgumentParser(prog='nyaav2')
    parser.add_argument('--mode', '-m', required=True, default='search', const='search', nargs='?', choices=['search', 'upload'])
    parser.add_argument('--sukebei', '-nsfw', dest='sukebei', required=False, action='store_true', help='Search or upload to sukebei')
    parser.add_argument('--username', '-U' , required=True, dest='user',help='Your username')
    parser.add_argument('--password', '-P', required=True, dest='passw', help='Your password')
    parser.add_argument('--input', '-i', dest='torkey', required=True, action='store', default=None, help='Keyword to be search')
    parser.add_argument('--category', dest='cname', choices=['all', 'anime', 'amv', 'anime_eng', 'anime_non-eng', 'anime_raw', 'audio', 'audio_lossless', 'audio_lossy', 'books', 'books_eng', 'books_non-eng', 'books_raw', 'live_action', 'la_eng', 'la_idolpv', 'la_non-eng', 'la_raw', 'pictures', 'pics_graphics', 'pics_photos', 'software', 'sw_apps', 'sw_games', 'art', 'art_anime', 'art_doujinshi', 'art_gamees', 'art_manga', 'art_pics', 'real_life', 'real_pics', 'real_videos'], required=False, action='store', default=None, help='Torrent category (sukebei start with \'art\' choices)')

    uploadmode = parser.add_argument_group('Upload Arguments')
    uploadmode.add_argument('--name', dest='name', required=False, action='store', default=None, help='Torrent name')
    uploadmode.add_argument('--information', dest='info', required=False, action='store', default=None, help='Torrent information (website, etc)')
    uploadmode.add_argument('--description', dest='desc', required=False, action='store', default=None, help='Torrent description (can be a file too)')
    uploadmode.add_argument('--anonymous', '-anon', dest='is_anon', action='store_true', required=False, default=False, help='Set torrent as an anonymous torrent')
    uploadmode.add_argument('--hidden', dest='is_hidden', action='store_true', required=False, default=False, help='Set torrent to hidden')
    uploadmode.add_argument('--remake', dest='is_remake', action='store_true', required=False, default=False, help='Set torrent as remake torrent')
    uploadmode.add_argument('--trusted', dest='is_trusted', action='store_true', required=False, default=False, help='Set torrent as trusted torrent')

    args = parser.parse_args()
    if args.cname != 'all':
        if args.sukebei:
            categorylist = ['art', 'art_anime', 'art_doujinshi', 'art_games', 'art_manga', 'art_pics', 'real_life', 'real_pics', 'real_videos']
            if not args.cname in categorylist:
                raise Nyaav2Exception('main: you use sukebei mode but not using sukebei only categories')
            else:
                pass
        else:
            categorylist = ['anime', 'amv', 'anime_eng', 'anime_non-eng', 'anime_raw', 'audio', 'audio_lossless', 'audio_lossy', 'books', 'books_eng', 'books_non-eng', 'books_raw', 'live_action', 'la_eng', 'la_idolpv', 'la_non-eng', 'la_raw', 'pictures', 'pics_graphics', 'pics_photos', 'software', 'sw_apps', 'sw_games']
            if not args.cname in categorylist:
                raise Nyaav2Exception('main: you use non-sukebei mode but not using non-sukebei only categories')

    if args.mode == 'search':
        print('@@ Searching torrent\n')
        if args.sukebei:
            search = SearchSukebeiTorrent(username=args.user, password=args.passw, keyword=args.torkey, category=args.cname)
        else:
            search = SearchTorrent(username=args.user, password=args.passw, keyword=args.torkey, category=args.cname)
        print('@@ Torrent searced, now parsing\n@@ Total Match: {}'.format(str(len(search))))
        print('## Will be showing until 5 torrent only')
        limit = 0
        parsedQuery = []
        while True:
            if limit < 5:
                break
            for query in search:
                NAME = query['name']
                ID = query['id']
                SUBMIT = query['submitter']
                if SUBMIT is None:
                    SUBMIT = 'Anonymous'
                else:
                    pass
                CREADATE = query['creation']
                SIZE = query['filesize']
                CATEG = query['category'] + ' (' + query['category_id'] + ')'
                STATS = 'Seeders: {} || Leechers: {} || Completed: {}'.format(query['seeders'], query['leechers'], query['completed'])
                if not args.sukebei:
                    DLLINK = 'https://nyaa.si{}'.format(query['download_link'])
                else:
                    DLLINK = 'https://sukebei.nyaa.si{}'.format(query['download_link'])
                TORURL = query['url']
                TORHASH = query['hash']

                temptext = '@ Name: {}\n@ ID: {}\n@ Size: {}\n@ Submitter: {}\n@ Category: {}\n@ Stats: {}\n@ Download Link: {}\n@ URL: {}\n@ Torrent hash: {}\n@ Creation Date: {}\n'.format(NAME, ID, SIZE, SUBMIT, CATEG, STATS, DLLINK, TORURL, TORHASH, CREADATE)
                parsedQuery.append(temptext)
                limit += 1
        print('@@ Torrent parsed:\n')

        text = '\n'.join(parsedQuery)
        print(text)
    elif args.mode == 'upload':
        if os.path.splitext(args.torkey)[1] != '.torrent':
            raise Nyaav2Exception('Upload mode choosen but input argument not a torrent files')

        if args.desc is not None:
            if os.path.isfile(args.desc):
                with open(args.desc, 'rb') as fdesc:
                    descr = str(fdesc.read())
            else:
                descr = args.desc

        print('@@ Creating options')
        if not args.sukebei:
            OPTS_UP = set_opts(username=args.user, password=args.passw, torrent=args.torkey, category=args.cname, name=args.name, information=args.info, description=descr, anonymous=args.is_anon, hidden=args.is_hidden, remake=args.is_remake, trusted=args.is_trusted)
        else:
            OPTS_UP = set_opts_sukebei(username=args.user, password=args.passw, torrent=args.torkey, category=args.cname, name=args.name, information=args.info, description=descr, anonymous=args.is_anon, hidden=args.is_hidden, remake=args.is_remake, trusted=args.is_trusted)
        
        print('@@ Uploading torrents')
        if not args.sukebei:
            re = json.loads(UploadTorrent(options=OPTS_UP))
        else:
            re = json.loads(UploadSukebeiTorrent(options=OPTS_UP))

        hashhex = re['hash']
        torid = re['id']
        name = re['name']
        url = re['url']

        text = f'!! Torrent Successfully Uploaded\n@ Name: {name}\n@ ID: {torid}\n@ URL: {url}\n@ Torrent hash: {hashhex}'
        print(text)
        

if __name__=='__main__':
    main()
