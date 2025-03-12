from logging import getLogger

from guess import Guess

log = getLogger(__name__)


def anneal(code, fmt, ngrams, words, neighbours, steps, heat, gamma, weight, every):

    def estimate_max_temp(guess):
        max_temp, base = 0, guess.score(ngrams, words, weight)
        for _ in range(100):
            max_temp = max(max_temp, abs(base - guess.swap().score(ngrams, words, weight)))
        return max_temp * heat

    def dump(old_score, old_guess, temp, i):
        log.info(f'\nscore: {old_score:4.2f}  temp: {temp:5.3f}  countdown: {i}/{steps}')
        log.info(f'{fmt(code)}')
        log.info(f'{old_guess}')

    old_guess = Guess(code, ngrams, neighbours)
    old_score = old_guess.score(ngrams, words, weight)

    max_temp = estimate_max_temp(old_guess)

    count_swap = 0
    for i in range(steps, 0, -1):
        temp = max_temp * pow(i / steps, gamma)
        new_guess = old_guess.swap()
        new_score = new_guess.score(ngrams, words, weight)
        # if new_score > old_score this is -ve and always selected
        if temp > (old_score - new_score):
            count_swap += 1
            old_guess = new_guess
            old_score = new_score
        if i % every == 0:
            dump(old_score, old_guess, temp, i)
    dump(old_score, old_guess, 0.0, 0)


