import re
import operator

import pypwikt as pw
from pypwikt import page
from pypwikt.word import EN_PART_OF_SPEECH, Meaning


__author__ = 'marigs'

class Page(page.Page):
    section_re = re.compile(r'^[=]+([-\w ]+)[=]+$', re.M)

    PART_OF_SPEECH = EN_PART_OF_SPEECH

    def __init__(self, title, rev_id, rev_ts, text, orig_lang):
        self.orig_section_name = self._get_orig_section_name(orig_lang)
        page.Page.__init__(self, title, rev_id, rev_ts, text)

    def _get_orig_section_name(self, orig_lang):
        ret = {pw.Lang.ENGLISH: u'english',
                pw.Lang.POLISH: u'polish'}.get(orig_lang, None)
        if not ret:
            raise NotImplemented()

        return ret

    def section_level(self, txt):
        return txt.count('=')/2

    def get_en_part_of_speech(self, pos):
        if pos in self.PART_OF_SPEECH:
            return pos
        else:
            pass #TODO: what?

    def is_pronunce_section(self, section):
        return section  == 'pronunciation'

    def _parse_part_of_speech(self, content):
        ret = []
        meaning = None
        for line in content.split('\n'):
            if not line.startswith("#"):
                continue
            splited = line.split(None, 1)
            if len(splited) != 2:
                continue
            (mark, text) = splited
            text = text.strip()
            if '*' in mark:
                continue       # TODO: should I do sth with that?
            if ':' in mark and meaning is not None:
                meaning.add_example(text)
            else:
                if meaning is not None:
                    ret.append(meaning)
                meaning = Meaning(text)

        if meaning is not None:
            ret.append(meaning)

        return ret
