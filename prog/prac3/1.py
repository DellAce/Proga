def lcp(strs):
    if not strs:
        return ""
    for i, ch in enumerate(min(strs, key=len)):
        if any(s[i] != ch for s in strs):
            return strs[0][:i]
    return min(strs, key=len)


strs = ["flower", "flow", "flight"]
print(lcp(strs))
