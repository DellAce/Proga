def concat_words(words):
    word_set = set(words)
    res = []
    from functools import lru_cache

    @lru_cache(None)
    def ok(w):
        return any(
            w[:i] in word_set and (w[i:] in word_set or ok(w[i:]))
            for i in range(1, len(w))
        )

    for w in words:
        word_set.remove(w)
        if ok(w):
            res.append(w)
        word_set.add(w)
    return res


words = [
    "cat",
    "cats",
    "catsdogcats",
    "dog",
    "dogcatsdog",
    "hippopotamuses",
    "rat",
    "ratcatdogcat",
]

print(concat_words(words))  # Output: ['catsdogcats', 'dogcatsdog', 'ratcatdogcat']
