from collections import defaultdict


def group_anagrams(strs):
    d = defaultdict(list)
    for s in strs:
        d["".join(sorted(s))].append(s)
    return list(d.values())


strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams(strs))
