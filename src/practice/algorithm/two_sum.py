"""
1. 两数之和
"""
def twoSum(nums:list[int], target:int):
    #哈希的查找是并列的而不是嵌套，所以时间复杂度是O(n)而不是O(n^2)   
    dic={}
    for i,num in enumerate(nums):
        if target-num in dic:
            return [dic[target-num],i]
        dic[num]=i
    return []
