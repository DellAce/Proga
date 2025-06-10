def max_sub_sum(nums):
    best = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        best = max(best, cur)
    return best


nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_sub_sum(nums))
