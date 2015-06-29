
import operator

__author__ = 'marigs'

EN_PART_OF_SPEECH = ['noun', 'verb', 'participle', 'article', 'pronoun',
                     'preposition', 'adverb', 'conjunction', 'adjective']

class Meaning(object):
    def __init__(self, meaning):
        self.meaning = meaning
        self.examples = []

    def add_example(self, example):
        self.examples.append(example)

    def __unicode__(self):
        return self.str_with_prefix('')

    def str_with_prefix(self, prefix):
        txt = prefix + "MN: " + self.meaning + '\n'
        for example in self.examples:
            txt += prefix + '\t' + example + '\n'
        return txt

class Word(object):
    def __init__(self, word):
        self.pronunciation = None
        self.audio = None
        self.word = word
        for part in EN_PART_OF_SPEECH:
            setattr(self, part, None)

    def has_meanings(self):
        return reduce(operator.or_,
                [bool(getattr(self, part)) for part in EN_PART_OF_SPEECH], False)

    def __unicode__(self):
        txt = self.word + "\n"
        if self.pronunciation is not None:
            txt += "\tPRONU: " + self.pronunciation + '\n'
        if self.audio is not None:
            txt += "\tAUDIO: " + self.audio + '\n'
        for part in EN_PART_OF_SPEECH:
            part_att = getattr(self, part)
            if part_att is not None:
                txt += u'\t' + part.upper() + u':\n'
                txt += self._str_meanings(part_att)
        return txt

    def _str_meanings(self, meanings):
        txt = u''
        for meaning in meanings:
            txt += meaning.str_with_prefix('\t\t')
        return txt

    def set_part_of_speech(self, part, meanings):
        att = getattr(self, part.lower())
        if att is None:
            setattr(self, part.lower(), meanings)

    def set_pronunciation(self, pronun):
        self.pronunciation = pronun

    def set_audio(self, audio):
        self.audio = audio
