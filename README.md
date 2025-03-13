# uncode

automated decryption of simple substitution ciphers (aka as caesar ciphers).

## example (taken from reddit/r/codes)

```
andrew@hostv6:~/project/uncode$ python py/uncode.py --include "[A-Za-z.,' ]" --text ~/Documents/color-purple.txt PGQ2Z1G4HUUHGKPLBGPGOH1LGMLLSPUNGZHKCG4O6GJV2SKUE1GPGQ2Z1GILGHG4VTHUDGNVKBGPGKVUE1GRUV4G4OH1G6V2GOH3LGPUGZ1VYLGMVYGTLBGI21GPGKVUE1GRUV4GPMGPGJHUGJHYY6GVUGSPRLG1OPZCCC 

score: 66.77  temp: 3.351  countdown: 100000/100000
PGQ2Z1G4HUUHGKPLBGPGOH1LGMLLSPUNGZHKCG4O6GJV2SKUE1GPGQ2Z1GILGHG4VTHUDGNVKBGPGKVUE1GRUV4G4OH1G6V2GOH3LGPUGZ1VYLGMVYGTLBGI21GPGKVUE1GRUV4GPMGPGJHUGJHYY6GVUGSPRLG1OPZCCC
e krla ihtth send e .han mnngetb lhsu i.w corgstfa e krla pn h ioIhtv bosd e sotfa ,toi i.ha wor .hSn et laoyn moy Ind pra e sotfa ,toi em e cht chyyw ot ge,n a.eluuu

...

score: 137.98  temp: 0.000  countdown: 0/100000
PGQ2Z1G4HUUHGKPLBGPGOH1LGMLLSPUNGZHKCG4O6GJV2SKUE1GPGQ2Z1GILGHG4VTHUDGNVKBGPGKVUE1GRUV4G4OH1G6V2GOH3LGPUGZ1VYLGMVYGTLBGI21GPGKVUE1GRUV4GPMGPGJHUGJHYY6GVUGSPRLG1OPZCCC
I quit wanna dIe, I hate seelInG iadP why couldn't I quit be a woman. God, I don't know what you have In itore sor me, but I don't know Is I can carry on lIke thIiPPP
```

it's not perfect, but it gets close.

## getting started

clone the repo and use python3 to run `uncode.py`.  give the `-h` argument to see available
options.

## how it works

### preparing n-grams

* the number of occurrences of the different n-grams are read from the reference text. a 1-gram is just a 
  single letter, so that counts different letters. a 2-gram is a pair of letters, so that counts the 
  numbers of different pairs, and so on up to `--degree`.

* note that the reference text is processed to simplify spaces (unless `--raw` is given) and to select
  a restricted range of characters (via `--include`).

* if `--words` is given, entire words are counted too.

* the counts are converted to log weights (this makes the score, described below, scale roughly as a
  probability).

* you can see the n-grams by specifying `--dump`.

### annealing guesses

* an initial guess is made at decoding by replacing the most common symbol in the ciphertext with the 
  most common letter (ie most common 1-gram) in the reference text, the second most common symbol with 
  the second most common letter, etc.

* the "score" of the guess is calculated by adding together the log weights of the different n-grams
  it contains (this is a value roughly proportional to the probability that the plaintext comes from 
  the same source as the reference text).

* the score may also include whole words (if `--words` is given) and may weight different degrees
  of n-grams differently (`--weight`).

* two characters (ie two 1-grams) are chosen at random and swapped, to give a new guess, and the score
  for the new guess calculated.

* by repeating this process several times we get an idea of how much the score changes on average.
  this value is then modified by `--heat` and used as an upper limit.

* we then try swapping characters many times, looking at the changing scores, always keeping guesses
  that improve (increase) the score and *sometimes* keeping guesses that decrease the score (ie if the 
  increase is less than the upper limit).

* as time goes on we lower the upper limit, becoming more strict about only accepting improvements 
  (the exact manner in which we lower the limit is controlled by `--gamma`; a value of 2, say, will
  lower it more quickly at the start, while a value like 0.5 will keep it higher at first and lower
  it more quickly near the end of the process).

* the guess will converge to a final value, when the upper limit reaches zero, which is our translation 
  to plaintext.

### summary

the above process (repeated guessing, trying to increase the score) is called "simulated annealing";
the upper limit on the acceptable change in score is the "temperature"; the entire process is 
designed to optimize (maximize) the probability that the plaintext is consistent with the input.

in other words, we try to find the most probable substitutions, where "most probable" means that
the plaintext resembles the reference text in the relative frequency of letters, pairs of letters,
etc.
