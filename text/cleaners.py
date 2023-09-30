""" from https://github.com/keithito/tacotron """

"""
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
"""

import re
from unidecode import unidecode
from phonemizer import phonemize
import num2words

# Regular expression matching whitespace:
_whitespace_re = re.compile(r"\s+")

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [
    (re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1])
    for x in [
        ("mrs", "misess"),
        ("mr", "mister"),
        ("dr", "doctor"),
        ("st", "saint"),
        ("co", "company"),
        ("jr", "junior"),
        ("maj", "major"),
        ("gen", "general"),
        ("drs", "doctors"),
        ("rev", "reverend"),
        ("lt", "lieutenant"),
        ("hon", "honorable"),
        ("sgt", "sergeant"),
        ("capt", "captain"),
        ("esq", "esquire"),
        ("ltd", "limited"),
        ("col", "colonel"),
        ("ft", "fort"),
    ]
]


def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text


def expand_numbers(text):
    return normalize_numbers(text)


def lowercase(text):
    return text.lower()


def collapse_whitespace(text):
    return re.sub(_whitespace_re, " ", text)


def convert_to_ascii(text):
    return unidecode(text)

def convert_num_to_words(utterance, language, to='cardinal', ordinal=False, **kwargs):
  match = re.findall(r'[\d./]+', utterance)
  if len(match) > 0:
    if len(re.findall(r'\d{28,}', utterance)) > 0:
      raise Exception("The number is too big! twenty seven numbers maximum")
    else:
      utterance = ' '.join([num2words.num2words(m, ordinal=ordinal, lang=language, to=to) if m.replace('.', '').replace('/', '').isdigit() else m for m in re.split(r'([\d./]+)', utterance)])
      if not utterance[0].isupper():
        utterance = utterance.capitalize()
  return utterance

def basic_cleaners(text):
    """Basic pipeline that lowercases and collapses whitespace without transliteration."""
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def transliteration_cleaners(text):
    """Pipeline for non-English text that transliterates to ASCII."""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def english_cleaners(text):
    """Pipeline for English text, including abbreviation expansion."""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = expand_abbreviations(text)
    phonemes = phonemize(text, language="en-us", backend="espeak", strip=True)
    phonemes = collapse_whitespace(phonemes)
    return phonemes


def english_cleaners2(text):
    """Pipeline for English text, including abbreviation expansion. + punctuation + stress"""
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = expand_abbreviations(text)
    phonemes = phonemize(
        text,
        language="en-us",
        backend="espeak",
        strip=True,
        preserve_punctuation=True,
        with_stress=True,
    )
    phonemes = collapse_whitespace(phonemes)
    return phonemes

def spanish_cleaners(text):
    '''Pipeline for Spanish text (using phonemes)'''
    text  = convert_num_to_words(text, language="es")
    phonemes = phonemize(
        text,
        language='es',
        backend='espeak',
        strip=True,
        preserve_punctuation=True,
        with_stress=True,
        punctuation_marks = ';:,.!?¡¿—…"«»“”()',
        language_switch='remove-flags'
    )
    phonemes = collapse_whitespace(phonemes)
    phonemes = phonemes.strip()
    return phonemes

def spanish_cleaners2(text):
    '''As of newer versions of espeak-ng, Latin Spanish (es-419) is improved.'''
    text  = convert_num_to_words(text, language="es")
    phonemes = phonemize(
        text,
        language='es-419',
        backend='espeak',
        strip=True,
        preserve_punctuation=True,
        with_stress=True,
        punctuation_marks = ';:,.!?¡¿—…"«»“”()',
        language_switch='remove-flags'
    )
    phonemes = collapse_whitespace(phonemes)
    phonemes = phonemes.strip()
    return phonemes
