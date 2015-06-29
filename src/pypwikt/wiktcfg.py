
__author__ = 'marigs'

import pypwikt as pw
import lang.en.page


class WiktionaryCfg(object):
    def __init__(self, wiktdict, orig_lang):
        self.wiktdict = wiktdict
        self.orig_lang = orig_lang

    def get_page(self, *args):
        if self.wiktdict == pw.Lang.ENGLISH:
            return lang.en.page.Page(*args)
        raise NotImplemented()
