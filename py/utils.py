from re import split


def keys_sorted_by_values(dict, reverse=False):
    yield from (kv[0] for kv in sorted(dict.items(), key=lambda kv: kv[1], reverse=reverse))


def overlapping_chunks(text, length):
    while len(text) >= length:
        yield text[:length]
        text = text[1:]


def words_in_line(line):
    # be consistent on how we split words
    return (word for word in split(r'\W+', line) if word)


def degrees(degree):
    # annoyingly, this is a 1 to inclusive kind of thing
    return range(1, degree + 1)
