from collections import defaultdict
from logging import getLogger
from random import randrange
from re import split

from ngrams import WORDS
from utils import overlapping_chunks

log = getLogger(__name__)


class Guess:

    def __init__(self, code, ngrams, neighbours, encode=None, decode=None):
        self.__code = code
        self.__ngrams = ngrams
        self.__neighbours = min(len(ngrams.alphabet) - 1, max(1, neighbours))
        self.__encode = encode if encode else {}
        self.__decode = decode if decode else {}
        if not decode and not encode:
            self.__best_guess()

    def __best_guess(self):
        counter = defaultdict(lambda: 0)
        for c in self.__code:
            counter[c] += 1
        enc = ''.join(kv[0] for kv in sorted(counter.items(), key=lambda kv: kv[1], reverse=True))
        plain = ''.join(kv[0] for kv in sorted(self.__ngrams[1].items(), key=lambda kv: kv[1], reverse=True))
        for c in enc:
            p, plain = plain[0], plain[1:]
            log.debug(f'{p} -> {c}')
            self.__encode[p] = c
            self.__decode[c] = p

    def score(self, ngrams, words, weight):
        score = 0
        plain = ''.join(self.__decode[c] for c in self.__code)
        for degree in range(1, ngrams.degree+1):
            k = pow(weight, degree)
            for ngram in overlapping_chunks(plain, degree):
                score += k * ngrams[degree][ngram]
        if words:
            for word in split(r'\W+', plain):
                if word:
                    score += ngrams[WORDS][word.lower()]
        return score / len(self.__code)

    def __str__(self):
        return ''.join(self.__decode[c] for c in self.__code)

    def swap(self):
        p1, p2 = self.nearby_neighbours()
        c1 = self.__encode.get(p1)
        c2 = self.__encode.get(p2)
        copy = Guess(self.__code, self.__ngrams, self.__neighbours,
                     encode=self.__encode.copy(), decode=self.__decode.copy())
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

    def random_neighbours(self):
        p1 = self.__ngrams.alphabet[randrange(0, len(self.__ngrams.alphabet))]
        p2 = self.__ngrams.alphabet[randrange(0, len(self.__ngrams.alphabet))]
        return p1, p2

    def nearby_neighbours(self):
        # largely equivalent to random for large neighbours
        i1 = randrange(0, len(self.__ngrams.alphabet))
        while True:
            i2 = i1 + randrange(-self.__neighbours, self.__neighbours + 1)
            if 0 <= i2 < len(self.__ngrams.alphabet) and i1 != i2:
                return self.__ngrams.alphabet[i1], self.__ngrams.alphabet[i2]
