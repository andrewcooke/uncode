from argparse import ArgumentParser, RawTextHelpFormatter
from argparse import ArgumentParser
from logging import getLogger, StreamHandler
from re import compile
from string import ascii_uppercase, ascii_lowercase
from sys import stderr

from anneal import anneal
from guess import Guess
from ngrams import build_ngrams
from parser import STRING, HEX, BASE64, read_code

log = getLogger(__name__)

DEFAULT_DEGREE = 6
DEFAULT_INCLUDE = '[A-Za-z0-9 ]'
DEFAULT_STEPS = 100000
DEFAULT_HEAT = 1
DEFAULT_GAMMA = 0.5
DEFAULT_WEIGHT = 1
DEFAULT_EVERY = 100
DEFAULT_VERBOSITY = 4
DEFAULT_NEIGHBOURS = 10
DEFAULT_FORMAT = STRING


def main():
    parser = make_parser()
    args = parser.parse_args()
    # v is 1 to 5, level is 10 to 50
    getLogger().setLevel(60 - 10 * args.v)
    getLogger().addHandler(StreamHandler(stderr))
    check_lower(args)
    ngrams = build_ngrams(args.text, args.degree, args.lower, args.raw, compile(args.include))
    if args.dump:
        print(ngrams)
    code, fmt_code = read_code(args.code, args.format)
    guess = Guess(code, fmt_code, ngrams, args.neighbours, args.cutoff)
    if args.hist:
        print(f'plaintext:\n{ngrams.hist()}')
        print(f'ciphertext:\n{guess.hist()}')
    guess.best_guess()  # do this after the above since it may throw an error
    anneal(guess, ngrams, not args.no_words, args.steps, args.heat, args.gamma, args.weight, args.every)


def make_parser():
    parser = ArgumentParser('uncode', description='''
this measures the frequency of n-grams in the given text and then uses that 
information to try guess the substitution used for the ciphertext and so 
determine the underlying plaintext.

the most important parameters are the sample file, which should match the 
language and style used in the ciphertext, and the include pattern, which 
should select the characters used in the plaintext.

note that you can use -- to separate --text arguments from the code text:
  python uncode.py --text ~/Documents/* -- jidfsojifergergieojwqjiqwo
but then the code text must be the final argument.
''', formatter_class=RawTextHelpFormatter)
    parser.add_argument('--text', metavar='PATH', nargs='+', required=True,
                        help='a sample file for the target language')
    parser.add_argument('--degree', metavar='N', type=int, default=DEFAULT_DEGREE,
                        help=f'maximum length of n-grams (default {DEFAULT_DEGREE})')
    parser.add_argument('--lower', action='store_true',
                        help='force sample to lower case?')
    parser.add_argument('--raw', action='store_true',
                        help='use raw format (verbatim whitespace)?')
    parser.add_argument('--no-words', action='store_true',
                        help='don\'t score whole words (separately from ngrams)?')
    parser.add_argument('--cutoff', metavar='CHAR',
                        help='set excess cypher characters to this (default is error)')
    parser.add_argument('--neighbours', metavar='N', type=int, default=DEFAULT_NEIGHBOURS,
                        help=f'swap within this range in alphabet (default {DEFAULT_NEIGHBOURS})')
    parser.add_argument('--include', metavar='REGEX', default=DEFAULT_INCLUDE,
                        help=f'sample characters to include (default {DEFAULT_INCLUDE})')
    parser.add_argument('--dump', action='store_true',
                        help='print ngrams')
    parser.add_argument('--hist', action='store_true',
                        help='print histograms')
    parser.add_argument('--steps', '-n', metavar='N', type=int, default=DEFAULT_STEPS,
                        help=f'number of iterations (default {DEFAULT_STEPS})')
    parser.add_argument('--every', metavar='N', type=int, default=DEFAULT_EVERY,
                        help=f'print progress every N iterations (default {DEFAULT_EVERY})')
    parser.add_argument('--heat', metavar='N', type=float, default=DEFAULT_HEAT,
                        help=f'scale factor for starting temperature (default {DEFAULT_HEAT})')
    parser.add_argument('--gamma', metavar='N', type=float, default=DEFAULT_GAMMA,
                        help=f'cooling curve (default {DEFAULT_GAMMA})')
    parser.add_argument('--weight', metavar='N', type=float, default=DEFAULT_WEIGHT,
                        help=f'weight for higher degree (default {DEFAULT_WEIGHT})')
    parser.add_argument('--format', metavar='FMT', choices=(STRING, HEX, BASE64), default=STRING,
                        help=f'input format (default {STRING}, {HEX}, {BASE64})')
    parser.add_argument('-v', metavar='N', type=int, default=DEFAULT_VERBOSITY,
                        help=f'verbosity (1-5, default {DEFAULT_VERBOSITY})')
    parser.add_argument('code', help='text to uncode (- will read from stdin)')
    return parser


def check_lower(args):
    # actually this isn't a big deal because include simply won't see any caps
    # if args.lower and any(compile(args.include).match(cap) for cap in ascii_uppercase):
    #     log.warning(f'WARNING: --lower used, but ---include allows capitals')
    if not args.lower and not any(compile(args.include).match(cap) for cap in ascii_lowercase):
        log.warning(f'WARNING: ---include excludes lowercase (if you want monocase, use --lower)')


if __name__ == '__main__':
    main()
