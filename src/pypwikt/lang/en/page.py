import re
import operator

import pypwikt as pw
from pypwikt import page
from pypwikt.word import EN_PART_OF_SPEECH, Meaning


__author__ = 'marigs'

class Page(page.Page):
    section_re = re.compile(r'^[=]+([\w ]+)[=]+$', re.M)

    non_used = ['anagrams', 'translations', 'synonyms', 'external links',
                'alternative forms', 'references', 'statistics', 'see also',
                'usage notes', 'quotations', 'interjection',
                'antonyms', 'related terms', 'hyponyms', 'etymology', 'letter', 'number',
                'symbol', 'abbreviation', 'abbreviations', 'proper noun', 'descendants',
                'coordinate terms', 'hypernyms', 'prefix', 'suffix', 'declension',
                'determiner', 'numeral', 'acronym', 'holonyms', 'initialism',
                'conjugation', 'meronyms', 'particle', 'troponyms', 'contraction',
                'prepositional phrase', 'inflection', 'gerund', 'expressions', 'locutions']

    non_used_starts = ['etymology', 'phrase', 'determiner', 'cardinal', 'proverb',
                        'derived']

    PART_OF_SPEECH = ['noun', 'verb', 'participle', 'article', 'pronoun', 'preposition', 'adverb', 'conjunction',
                      'adjective'] #TODO: copy of EN_PART_OF_SPEECH

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

    def is_non_used_section(self, section):
        return (section in self.non_used or
                reduce(operator.or_, map(lambda x: section.startswith(x), self.non_used_starts)))

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
