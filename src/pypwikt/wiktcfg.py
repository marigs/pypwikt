
__author__ = 'marigs'

import pypwikt as pw
import lang.en.page

_iso2lcode_enum = {'en': pw.Lang.ENGLISH,
                   'pl': pw.Lang.POLISH}

_enum_iso2lcode = {y:x for x,y in _iso2lcode_enum.iteritems()}

class WiktionaryCfg(object):
    def __init__(self, wiktdict, orig_lang):
        self.wiktdict = _iso2lcode_enum[wiktdict]
        self.orig_lang = _iso2lcode_enum[orig_lang]

    def get_url_wikt(self):
        return "http://%s.wiktionary.org/w/api.php" \
                    % _enum_iso2lcode[self.wiktdict]

    def get_page(self, title, rev_id, rev_ts, text):
        if self.wiktdict == pw.Lang.ENGLISH:
            return lang.en.page.Page(title, rev_id, rev_ts, text, self.orig_lang)
        raise NotImplemented()
