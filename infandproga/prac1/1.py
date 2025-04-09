"""
Имеется массив целых чисел numbers. 
Необходимо найти все такие тройки [numbers[i], numbers[j], numbers[k]], 
где i != j, j != k, k != i и 
сумма numbers[i] + numbers[j] + numbers[k] = 0

Пример: nums = [4,-1,7,0,1,2,-1,5], тройки: [[-1,-1,2],[-1,0,1]]
"""
nums = [4,-1,7,0,1,2,-1,5]
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        for k in range(j + 1, len(nums)):
            if (i != j and j != k and k != i) and (nums[i] + nums[j] + nums[k] == 0):
                print([nums[i], nums[j], nums[k]])
