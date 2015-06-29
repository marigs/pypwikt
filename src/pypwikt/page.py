import re

from word import Word

__author__ = 'marigs'


class Page(object):

    def __init__(self, title, rev_id, rev_ts, text):
        self.title = title
        self.rev_id = rev_id
        self.rev_ts = rev_ts
        self.text = text

    def __str__(self):
        return self.title + '(' + self.rev_id + ', ' + self.rev_ts + ')\n' + self.text

    def get_sections(self):
        ret = []
        text_start = 0
        section_name = ''
        section_text = ''
        for i in self.section_re.finditer(self.text):
            if text_start != 0:
                text = self.text[text_start:i.start()].strip()
                ret.append((self.section_level(section_text), section_name, text))
            text_start = i.end()
            f = lambda a, b: a if a is not None else b
            section_name = reduce(f, i.groups()).lower().strip()
            section_text = i.group()
        text = self.text[text_start:].strip()
        ret.append((self.section_level(section_text), section_name, text))
        return ret

    def is_partos_section(self, section):
        return section in self.PART_OF_SPEECH

    def get_word(self):
        sections = self.get_sections()
        false = False
        from_section_level = -1
        word = Word(self.title)
        for section in sections:
            if section[1] == self.orig_section_name:
                from_section_level = section[0]
                continue
            elif from_section_level >= 0 and section[0] <= from_section_level:
                from_section_level = -1

            if from_section_level >= 0:
                if self.is_pronunce_section(section[1]):
                    ipa, audio = self._parse_pronunciation(section[2])
                    word.set_pronunciation(ipa)
                    word.set_audio(audio)
                elif self.is_partos_section(section[1]):
                    try:
                        meanings = self._parse_part_of_speech(section[2])
                    except:
                        print self.title, "!!!!!!", section[2]
                        raise
                    en_part_of_speach = self.get_en_part_of_speech(section[1])
                    word.set_part_of_speech(en_part_of_speach, meanings)
                elif self.is_non_used_section(section[1]):
                    pass
                else:
                    raise KeyError("Unknown section: \"" + section[1] + '\" (' + word.word + ')')
        return word

    @staticmethod
    def _parse_pronunciation(content):
        pronunciation_re = re.compile(r'^[^{]+'
                                      r'({{a(\|\w+)*(\|UK)(\|\w+)*}})?'
                                      r'\s*'
                                      r'({{enPR\|[^}]+}},)?'
                                      r'\s*'
                                      r'{{IPA\|(?P<ipa>[^|]+)(\|\[[^\]]+\])*\|lang=en}}',
                                      re.VERBOSE + re.MULTILINE)
        audio_re = re.compile(r'{{audio\|(?P<audiof>[a-zA-Z0-9_\-.]+)\|Audio \((US|UK)\)\|lang=en}}', re.MULTILINE) #TODO: prefere UK
        #print "C", content
        m = pronunciation_re.search(content)
        ipa = None
        audio = None
        if m is not None:
            ipa = m.group('ipa')
        m = audio_re.search(content)
        if m is not None:
            audio = m.group('audiof')

        return ipa, audio
