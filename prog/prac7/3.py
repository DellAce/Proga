from collections import defaultdict


def subarray_sum(nums, k):
    cnt = defaultdict(int)
    cnt[0] = 1
    s = ans = 0
    for n in nums:
        s += n
        ans += cnt[s - k]
        cnt[s] += 1
    return ans


nums = [1, 1, 1]
k = 2
print(subarray_sum(nums, k))
