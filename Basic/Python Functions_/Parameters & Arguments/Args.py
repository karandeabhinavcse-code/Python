# def add(*nums):
#     print(nums)
# add(10,20,30,40,50)


# def add(nums):
#     print(nums)
# add(10,20,30,40,50)

def add(*nums):
    total = 0
    for num in nums:
        total += num
    print(total)
add(10,20,30)