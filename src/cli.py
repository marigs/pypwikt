#!/usr/bin/env python

import sys

from argparse import ArgumentParser

from wikitools import wiki
from wikitools import api

import pypwikt as pw
from pypwikt import wiktcfg

def main():
    parser = ArgumentParser()
    parser.add_argument("-w", "--word", required=True, type=str)
    parser.add_argument("-l", "--lang", required=True, type=str)
    parser.add_argument("-o", "--orig", required=True, type=str)
    args = parser.parse_args()

    parser = wiktcfg.WiktionaryCfg(args.lang, args.orig)

    site = wiki.Wiki(parser.get_url_wikt())
    params = {'action':'query', 'titles': args.word,
            'rvprop': 'content|ids|timestamp',
            'prop': 'revisions'}
    # params = {'action':'query', 'revids':'332675', 'rvprop': 'content',
    #         'prop': 'revisions'}
    request = api.APIRequest(site, params)
    result = request.queryGen()

    res = result.next()
    p = res['query']['pages'].values()[0]
    rev_id = p['revisions'][0]['revid']
    rev_ts = p['revisions'][0]['timestamp']
    text = p['revisions'][0]['*']


    page = parser.get_page(unicode(args.word, 'utf-8'), rev_id, rev_ts, text)

    w = page.get_word()
    if w.has_meanings():
        print unicode(w)

if __name__ == "__main__":
    main()
