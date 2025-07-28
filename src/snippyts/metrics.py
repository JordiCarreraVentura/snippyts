
from difflib import SequenceMatcher
from statistics import mean

from unidecode import unidecode
from nltk import wordpunct_tokenize as tokenizer


def average_token_similarity(s1: str, s2: str) -> float:
    if not (isinstance(s1, str) and isinstance(s2, str)):
        return 0
    tokens_0 = [unidecode(token.strip().lower()) for token in tokenizer(s1)]
    tokens_1 = [unidecode(token.strip().lower()) for token in tokenizer(s2)]
    tokens_0 = sorted(tokens_0, key=lambda x: len(x), reverse=True)
    tokens_1 = sorted(tokens_1, key=lambda x: len(x), reverse=True)
    
    if len(tokens_0) < len(tokens_1):
        smaller_set = tokens_0
        larger_set = tokens_1
    else:
        smaller_set = tokens_1
        larger_set = tokens_0

    sims = []
    while smaller_set:
        token_0 = smaller_set.pop()
        _sims = []
        for idx, token_1 in enumerate(larger_set):
            sim = SequenceMatcher(None, token_0, token_1).ratio()
            _sims.append((sim, idx))
        _sims.sort()
        sim, idx = _sims.pop()
        sims.append(sim)
        larger_set.pop(idx)

    for token_1 in larger_set:
        sims.append(0.0)

    return round(mean(sims), 4)
