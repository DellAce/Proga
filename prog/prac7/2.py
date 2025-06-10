def check_incl(s1, s2):

    def freq_dict(s):
        d = {}
        for ch in s:
            d[ch] = d.get(ch, 0) + 1
        return d

    need = freq_dict(s1)
    win = {}
    k = len(s1)

    for i, ch in enumerate(s2):
        win[ch] = win.get(ch, 0) + 1

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
