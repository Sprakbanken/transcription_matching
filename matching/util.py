import re
from sprakbanken_normalizer.inverse_text_normalizer import inv_normalize

strip_right = re.compile(r'\W*$')
def clean_punctuation(t):
    return re.sub(strip_right, '', t)

def tokenize_reference(text, remove_punctuation = True):
    tokens = text.strip().split()
    match_tokens = map(lambda t: t.lower(), tokens)
    if remove_punctuation:
        match_tokens = map(clean_punctuation, match_tokens)
    return tokens, list(match_tokens)

def tokenize_segment(s, normalize_numbers = True):
    t = s.strip()
    if normalize_numbers:
        t = inv_normalize(t)
    return t.split()
