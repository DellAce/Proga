from collections import Counter


def check_incl(s1, s2):
    need = Counter(s1)
    win = Counter()
    k = len(s1)
    for i, ch in enumerate(s2):
        win[ch] += 1
        if i >= k:
            left = s2[i - k]
            win[left] -= 1
            if win[left] == 0:
                del win[left]
        if win == need:
            return True
    return False


s1 = "ab"
s2 = "eidbaooo"
print(check_incl(s1, s2))
