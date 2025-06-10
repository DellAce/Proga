detect_cap = (
    lambda w: w.isupper() or w.islower() or (w[0].isupper() and w[1:].islower())
)
word = "GandR"
print(detect_cap(word))
