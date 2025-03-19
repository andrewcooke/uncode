from collections import defaultdict
from logging import getLogger
from re import sub, fullmatch, split
from math import log as ln

from utils import keys_sorted_by_values, words_in_line, degrees, fmt_hist

log = getLogger(__name__)

WORDS = 'words'


def build_ngrams(path, degree, lower, raw, include):
    counts = count_ngrams(path, degree, lower, raw, include)
    log_probs = counts_to_log_probs(counts)
    return NGrams(degree, log_probs)


def count_ngrams(path, max_degree, lower, raw, include):
    counts = defaultdict(lambda: defaultdict(lambda: 0))
    with open(path) as source:
        acc, nline, nchar = '', 0, 0
        for line in source:
            nline += 1
            line = clean_line(line, lower, raw, include)
            if ' ' in line:  # words not used if spaces not in alphabet
                for word in words_in_line(line):
                    counts[WORDS][word.lower()] += 1
            acc += line
            nchar += len(line)
            while len(acc) >= max_degree:
                for degree in degrees(max_degree):
                    counts[degree][acc[:degree]] += 1
                acc = acc[1:]
        log.debug(f'read {nline} lines ({nchar} chars) from {path}')
        return counts


def clean_line(line, lower, raw, include):
    if lower: line = line.lower()
    if not raw:
        # line will have a trailing space after this because of the final \n
        line = sub(r'\s+', ' ', line)
        line = sub(r'^ ', '', line)
    return ''.join(c for c in line if include.fullmatch(c))


def counts_to_log_probs(counts):
    log_probs = {}
    for degree, dcounts in counts.items():
        min_count = sorted(dcounts.values())[0]
        log_probs[degree] = defaultdict(lambda: ln(min_count))
        for ngram in dcounts.keys():
            log_probs[degree][ngram] = ln(dcounts[ngram])
    return log_probs


class NGrams:

    def __init__(self, degree, log_probs):
        self.degree = degree
        self.alphabet = ''.join(keys_sorted_by_values(log_probs[1], reverse=True))
        self.__log_probs = log_probs

    def __getitem__(self, n):
        return self.__log_probs[n]

    def __str__(self):
        return f'''alphabet: {self.alphabet}
{'\n'.join(self.__str_degree(n) for n in degrees(self.degree))}
{self.__str_degree(WORDS) if WORDS in self.__log_probs else ''}
'''

    def __str_degree(self, n):
        return f'''
degree {n}:
{'\n'.join(self.__str_score(n, s) for s in sorted(set(self[n].values()), reverse=True) if s > 0)}
'''

    def __str_score(self, n, s):
        return f'''{s:.3f}: {','.join(sorted(k for k,v in self[n].items() if v == s))}'''

    def hist(self):
        return fmt_hist(self[1])
