from collections import defaultdict
from copy import copy
from logging import getLogger
from random import randrange

from ngrams import WORDS
from utils import overlapping_chunks, keys_sorted_by_values, words_in_line, degrees, fmt_hist

log = getLogger(__name__)


class Guess:

    def __init__(self, code, fmt_code, ngrams, neighbours):
        self.fmt_code = fmt_code
        self.__code = code
        self.__ngrams = ngrams
        self.__neighbours = min(len(ngrams.alphabet) - 1, max(1, neighbours))
        self.__encode = {}
        self.__decode = {}
        self.__best_guess()

    def __best_guess(self):
        counter = self.__count()
        plain = ''.join(keys_sorted_by_values(self.__ngrams[1], reverse=True))
        mapping = 'best guess: '
        for c in keys_sorted_by_values(counter, reverse=True):
            if not plain:
                log.debug(mapping)
                raise Exception(f'insufficient alphabet for input')
            p, plain = plain[0], plain[1:]
            mapping += f'{c}->{p} '
            self.__encode[p] = c
            self.__decode[c] = p
        log.debug(mapping)

    def __count(self):
        counter = defaultdict(lambda: 0)
        for c in self.__code:
            counter[c] += 1
        return counter

    def score(self, ngrams, words, weight):
        score = 0
        plain = ''.join(self.__decode[c] for c in self.__code)
        for degree in degrees(ngrams.degree):
            k = pow(weight, degree)
            for ngram in overlapping_chunks(plain, degree):
                score += k * ngrams[degree][ngram]
        if words:
            for word in words_in_line(plain):
                score += ngrams[WORDS][word.lower()]
        return score / len(self.__code)

    def __str__(self):
        return ''.join(self.__decode[c] for c in self.__code)

    def __copy(self):
        new_guess = copy(self)  # shallow copy
        # deep copy the two things we will mutate
        new_guess.__encode = self.__encode.copy()
        new_guess.__decode = self.__decode.copy()
        return new_guess

    def swap(self):
        new_guess = self.__copy()
        p1, p2 = self.nearby_neighbours()
        c1 = self.__encode.get(p1)
        c2 = self.__encode.get(p2)
        # if p1 is used in decryption, replace it with p2
        # if it's not used then we can ignore p2
        if c1:
            new_guess.__encode[p2] = c1
            new_guess.__decode[c1] = p2
        # same with p2
        if c2:
            new_guess.__encode[p1] = c2
            new_guess.__decode[c2] = p1
        return new_guess

    def random_neighbours(self):
        p1 = self.__ngrams.alphabet[randrange(0, len(self.__ngrams.alphabet))]
        p2 = self.__ngrams.alphabet[randrange(0, len(self.__ngrams.alphabet))]
        return p1, p2

    def nearby_neighbours(self):
        # largely equivalent to random_neighbours for large self.__neighbours
        i1 = randrange(0, len(self.__ngrams.alphabet))
        while True:
            i2 = i1 + randrange(-self.__neighbours, self.__neighbours + 1)
            if 0 <= i2 < len(self.__ngrams.alphabet) and i1 != i2:
                return self.__ngrams.alphabet[i1], self.__ngrams.alphabet[i2]

    def hist(self):
        return fmt_hist(self.__count())
