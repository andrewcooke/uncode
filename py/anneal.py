from logging import getLogger

from guess import Guess

log = getLogger(__name__)


def anneal(old_guess, ngrams, words, steps, heat, gamma, weight, every):

    def estimate_max_temp(guess):
        max_temp, base = 0, guess.score(ngrams, words, weight)
        for _ in range(100):
            max_temp = max(max_temp, abs(base - guess.swap().score(ngrams, words, weight)))
        return max_temp * heat

    def dump(score, guess, temp, i, swaps):
        log.info(f'score: {score:4.2f}  temp: {temp:5.3f}  countdown: {i}/{steps}  swaps: {swaps}')
        log.debug(f'{ngrams.alphabet}')
        log.debug(f'{guess.fmt_code}')
        log.warning(f'{guess}\n')

    old_score = old_guess.score(ngrams, words, weight)
    max_temp = estimate_max_temp(old_guess)

    swaps = 0
    for i in range(steps, 0, -1):
        temp = max_temp * pow(i / steps, gamma)
        new_guess = old_guess.swap()
        new_score = new_guess.score(ngrams, words, weight)
        # if new_score > old_score this is -ve and always selected
        if temp > (old_score - new_score):
            swaps += 1
            old_guess = new_guess
            old_score = new_score
        if i % every == 0:
            dump(old_score, old_guess, temp, i, swaps)
    dump(old_score, old_guess, 0.0, 0, swaps)
    log.error(f'{old_guess}')


