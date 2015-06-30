# -*- coding: utf-8 -*-

import re

import pypwikt as pw
from pypwikt import page

from pypwikt.word import Meaning

__author__ = 'marigs'

def check_startswith(list, word):
    for i in list:
        if i in word:
            return i
    return None

class Page(page.Page):
    section_re = re.compile(r'^[=]+[\w ]+\({{([\w ]+)}}\)\s[=]+$'
                            r'|'
                            r'^{{([\w ]+)}}$'
                            r'|'
                            r'^\'\'([,\w ]+)\'\'$',
                            re.MULTILINE + re.VERBOSE + re.UNICODE)

    MAPPING_PART_OF_SPEECH = {u'czasownik': u'verb', u'rzeczownik': u'noun', u'przyimek': u'preposition',
                              u'zaimek': u'pronoun', u'przedimek': u'article',
                              u'przysłówek': u'adverb', u'imiesłów': u'participle',
                              u'przymiotnik': u'adjective', u'spójnik': u'conjunction'}

    PART_OF_SPEECH = MAPPING_PART_OF_SPEECH.keys()

    def __init__(self, title, rev_id, rev_ts, text, orig_lang):
        self.orig_section_name = self._get_orig_section_name(orig_lang)
        page.Page.__init__(self, title, rev_id, rev_ts, text)

    def _get_orig_section_name(self, orig_lang):
        ret = {pw.Lang.ENGLISH: u'język angielski',
               pw.Lang.POLISH: u'język polski'}.get(orig_lang, None)
        if not ret:
            raise NotImplementedError()
        return ret

    def section_level(self, txt):
        ec = txt.count('=')/2
        if ec != 0:
            return ec
        if txt.startswith('{'):
            return 4
        if txt.startswith('\''):
            return 5

    def get_en_part_of_speech(self, pos):
        if pos in self.MAPPING_PART_OF_SPEECH:
            return self.MAPPING_PART_OF_SPEECH[pos]
        k = check_startswith(self.MAPPING_PART_OF_SPEECH.keys(), pos)
        if k:
            return self.MAPPING_PART_OF_SPEECH[k]
        return None

    def is_partos_section(self, section):
        return bool(self.get_en_part_of_speech(section))

    def is_pronunce_section(self, section):
        return section == 'wymowa'

    def _parse_part_of_speech(self, content):
        ret = []
        meaning = None
        for line in content.split('\n'):
            if not line.startswith(':'):
                continue
            mark, text = line.split(None, 1)
            meaning = Meaning(text)
            ret.append(meaning)

        return ret
