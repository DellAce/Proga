def find132(nums):
    st = []
    third = -float("inf")
    for n in nums[::-1]:
        if n < third:
            return True
        while st and n > st[-1]:
            third = st.pop()
        st.append(n)
    return False


nums = [-1, 3, 2, 0]
print(find132(nums))
