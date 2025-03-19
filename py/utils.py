from re import split
from sys import stdin


def keys_sorted_by_values(dict, reverse=False):
    yield from (kv[0] for kv in sorted(dict.items(), key=lambda kv: kv[1], reverse=reverse))


def overlapping_chunks(text, length):
    while len(text) >= length:
        yield text[:length]
        text = text[1:]


def words_in_line(line, cutoff=None):
    sep = f'[{cutoff}\\W]+' if cutoff else r'\W+'
    return (word for word in split(sep, line) if word.strip())


def degrees(degree):
    # annoyingly, this is a 1 to inclusive kind of thing
    return range(1, degree + 1)


def possibly_stdin(code):
    if code == '-':
        return ''.join(stdin)
    else:
        return code


def fmt_hist(counts):
    max_count = max(counts.values())
    scale_counts = {key: counts[key] * 80 / max_count for key in counts.keys()}
    return '\n'.join(f'{key}: {"#" * int(scale_counts[key])}'
                     for key in keys_sorted_by_values(scale_counts, reverse=True))
