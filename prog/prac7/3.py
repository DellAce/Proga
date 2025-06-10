def subarray_sum(nums, k):

    cnt = {0: 1}
    s = 0
    ans = 0

    for n in nums:
        s += n
        ans += cnt.get(s - k, 0)
        cnt[s] = cnt.get(s, 0) + 1
    return ans


nums = [1, 1, 1]
k = 2
print(subarray_sum(nums, k))
