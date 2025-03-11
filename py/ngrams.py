from collections import defaultdict
from logging import getLogger
from re import sub
from math import log as ln

from utils import keys_sorted_by_values

log = getLogger(__name__)


def build_ngrams(path, degree, lower, raw, include):
    counts = count_ngrams(path, degree, lower, raw, include)
    log_probs = counts_to_log_probs(counts)
    return NGrams(degree, log_probs)


def count_ngrams(path, degree, lower, raw, include):
    counts = defaultdict(lambda: defaultdict(lambda: 0))
    with open(path) as source:
        acc, nline, nchar = '', 0, 0
        for line in source:
            nline += 1
            if lower: line = line.lower()
            if not raw:
                line = sub(r'\s+', ' ', line)
                line = sub(r'^ ', '', line)
            line = ''.join(c for c in line if include.fullmatch(c))
            acc += line
            nchar += len(line)
            while len(acc) >= degree:
                for n in range(1, degree+1):
                    counts[n][acc[:n]] += 1
                acc = acc[1:]
        log.debug(f'read {nline} lines ({nchar} chars) from {path}')
        return counts


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
{'\n'.join(self.__str_degree(n) for n in range(1, self.degree+1))}
'''

    def __str_degree(self, n):
        return f'''
degree {n}:
{'\n'.join(self.__str_score(n, s) for s in sorted(set(self[n].values()), reverse=True) if s > 0)}
'''

    def __str_score(self, n, s):
        return f'''{s:.3f}: {','.join(sorted(k for k,v in self[n].items() if v == s))}'''
