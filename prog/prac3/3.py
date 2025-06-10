def group_anagrams(strs):
    groups = {}
    for s in strs:
        key = "".join(sorted(s))  # сортировка даёт одинаковый «отпечаток»
        if key not in groups:  # создаём список при первом появлении
            groups[key] = []
        groups[key].append(s)
    return list(groups.values())
