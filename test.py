nums = [0]
qtd = [0]
for i in range(1,10000):
    curr_nums = []
    for j in range(1,11):
        if i%j==0:
            curr_nums.append(j)
    nums.append(curr_nums)
    qtd.append(len(curr_nums))

for i in range(1,10000):
    if qtd[i]>9:
        print(i, nums[i])
        print()
        
        
        


