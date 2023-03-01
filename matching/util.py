import re

strip_right = re.compile(r'\W*$')
def clean_punctuation(t):
    return re.sub(strip_right, '', t.lower())

def tokenize(text):
    tokens = text.strip().split()
    return tokens, list(map(clean_punctuation, tokens))
