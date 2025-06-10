def restore_ip(s):
    res = []

    def back(pos, parts, cur):
        if parts == 4:
            if pos == len(s):
                res.append(".".join(cur))
                return
        for l in range(1, 4):
            if pos + l > len(s):
                break
            seg = s[pos : pos + l]
            if (seg[0] == "0" and l > 1) or int(seg) > 255:
                continue
            back(pos + l, parts + 1, cur + [seg])

    back(0, 0, [])
    return res


s = "25525511135"
print(restore_ip(s))
