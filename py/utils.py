

def keys_sorted_by_values(dict, reverse=False):
    yield from (kv[0] for kv in sorted(dict.items(), key=lambda kv: kv[1], reverse=reverse))


def overlapping_chunks(text, length):
    while len(text) >= length:
        yield text[:length]
        text = text[1:]
