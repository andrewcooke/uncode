from collections import defaultdict
from logging import getLogger

from utils import overlapping_chunks

log = getLogger(__name__)


class Guess:

    def __init__(self, code, ngrams, encode=None, decode=None):
        self.__code = code
        self.__encode = encode if encode else {}
        self.__decode = decode if decode else {}
        if ngrams:
            if encode or decode:
                raise Exception('ngrams given to clone')
            self.__best_guess(ngrams)

    def __best_guess(self, ngrams):
        counter = defaultdict(lambda: 0)
        for c in self.__code:
            counter[c] += 1
        enc = ''.join(kv[0] for kv in sorted(counter.items(), key=lambda kv: kv[1], reverse=True))
        plain = ''.join(kv[0] for kv in sorted(ngrams[1].items(), key=lambda kv: kv[1], reverse=True))
        for c in enc:
            p, plain = plain[0], plain[1:]
            log.debug(f'{p} -> {c}')
            self.__encode[p] = c
            self.__decode[c] = p

    def score(self, ngrams, weight):
        score = 0
        plain = ''.join(self.__decode[c] for c in self.__code)
        for degree in range(1, ngrams.degree+1):
            k = pow(weight, degree)
            for ngram in overlapping_chunks(plain, degree):
                score += k * ngrams[degree][ngram]
        return score / len(self.__code)

    def __str__(self):
        return ''.join(self.__decode[c] for c in self.__code)

    def swap(self, p1, p2):
        copy = Guess(self.__code, None, encode=self.__encode.copy(), decode=self.__decode.copy())
        c1 = self.__encode.get(p1)
        c2 = self.__encode.get(p2)
        # if p1 is used in decryption, replace it with p2
        # if it's not used then we can ignore p2
        if c1:
            copy.__encode[p2] = c1
            copy.__decode[c1] = p2
        # same with p2
        if c2:
            copy.__encode[p1] = c2
            copy.__decode[c2] = p1
        return copy


