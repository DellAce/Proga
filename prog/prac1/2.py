"""
Имеется массив целых чисел numbers. 
Необходимо найти все последовательности в массиве (подряд стоящие числа), 
сумма которых равна заданному числу S.
Пример: nums = [4,-1,7,0,1,2,-1,5], S = 3, 
последовательности: [4, -1], [0, 1, 2], [1, 2]
"""
nums = [4,-1,7,0,1,2,-1,5]
S = 3
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if sum(nums[i:j]) == S:
            print(nums[i:j])